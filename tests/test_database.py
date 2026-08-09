import aiosqlite
import pytest

import database


@pytest.fixture
def db_path(tmp_path, monkeypatch):
    path = str(tmp_path / "test.db")
    monkeypatch.setattr(database, "DATABASE_NAME", path)
    return path


async def table_names(path):
    async with aiosqlite.connect(path) as db:
        async with db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ) as cursor:
            return {row[0] for row in await cursor.fetchall()}


async def test_create_database_creates_all_tables(db_path):
    await database.create_database()

    assert {"users", "countries", "packages", "orders"} <= await table_names(db_path)


async def test_create_database_is_idempotent(db_path):
    await database.create_database()
    await database.add_user(1, "user", "User One")

    await database.create_database()

    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            assert (await cursor.fetchone())[0] == 1


async def test_users_table_defaults(db_path):
    await database.create_database()
    await database.add_user(555, "someone", "Some One")

    async with aiosqlite.connect(db_path) as db:
        async with db.execute(
            "SELECT language, created_at FROM users WHERE telegram_id=?", (555,)
        ) as cursor:
            language, created_at = await cursor.fetchone()

    assert language == "ar"
    assert created_at is not None


async def test_add_user_stores_given_values(db_path):
    await database.create_database()

    await database.add_user(1001, "fluxo", "Fluxo Client")

    async with aiosqlite.connect(db_path) as db:
        async with db.execute(
            "SELECT telegram_id, username, full_name FROM users"
        ) as cursor:
            rows = await cursor.fetchall()

    assert rows == [(1001, "fluxo", "Fluxo Client")]


async def test_add_user_ignores_duplicate_telegram_id(db_path):
    await database.create_database()

    await database.add_user(7, "first", "First Name")
    await database.add_user(7, "second", "Second Name")

    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT username, full_name FROM users") as cursor:
            rows = await cursor.fetchall()

    assert rows == [("first", "First Name")]


async def test_add_user_accepts_missing_username(db_path):
    await database.create_database()

    await database.add_user(8, None, "No Username")

    async with aiosqlite.connect(db_path) as db:
        async with db.execute(
            "SELECT username FROM users WHERE telegram_id=?", (8,)
        ) as cursor:
            assert (await cursor.fetchone())[0] is None


async def test_add_user_requires_existing_tables(db_path):
    with pytest.raises(Exception):
        await database.add_user(9, "nobody", "No Tables")
