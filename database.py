import logging

import aiosqlite
from config import DATABASE_NAME

logger = logging.getLogger(__name__)


async def create_database():
    async with aiosqlite.connect(DATABASE_NAME) as db:

        # العملاء
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            full_name TEXT,
            language TEXT DEFAULT 'ar',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # الدول
        await db.execute("""
        CREATE TABLE IF NOT EXISTS countries(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            emoji TEXT,
            active INTEGER DEFAULT 1
        )
        """)

        # الباقات
        await db.execute("""
        CREATE TABLE IF NOT EXISTS packages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_id INTEGER,
            title TEXT,
            days INTEGER,
            price REAL,
            active INTEGER DEFAULT 1,
            FOREIGN KEY(country_id) REFERENCES countries(id)
        )
        """)

        # الطلبات
        await db.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            package_id INTEGER,
            status TEXT DEFAULT 'waiting_payment',
            payment_image TEXT,
            qr_image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(package_id) REFERENCES packages(id)
        )
        """)

        await db.commit()

    logger.info("Database %s ready", DATABASE_NAME)


async def add_user(
    telegram_id,
    username,
    full_name
):

    async with aiosqlite.connect(DATABASE_NAME) as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO users
            (telegram_id,username,full_name)

            VALUES (?,?,?)
            """,
            (
                telegram_id,
                username,
                full_name
            )
        )

        await db.commit()

    logger.debug("User %s stored", telegram_id)
