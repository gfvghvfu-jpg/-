import importlib

import pytest

import config


@pytest.fixture(autouse=True)
def restore_config():
    yield
    importlib.reload(config)


def test_values_are_read_from_environment(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "123:abc")
    monkeypatch.setenv("STORE_NAME", "Fluxo")
    monkeypatch.setenv("BINANCE_ID", "999")
    monkeypatch.setenv("DATABASE_NAME", "custom.db")
    monkeypatch.setenv("OWNER_ID", "42")

    module = importlib.reload(config)

    assert module.BOT_TOKEN == "123:abc"
    assert module.STORE_NAME == "Fluxo"
    assert module.BINANCE_ID == "999"
    assert module.DATABASE_NAME == "custom.db"
    assert module.OWNER_ID == 42


def test_database_name_falls_back_to_default(monkeypatch):
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)
    monkeypatch.delenv("DATABASE_NAME", raising=False)

    module = importlib.reload(config)

    assert module.DATABASE_NAME == "fluxo.db"


def test_owner_id_defaults_to_zero(monkeypatch):
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)
    monkeypatch.delenv("OWNER_ID", raising=False)

    module = importlib.reload(config)

    assert module.OWNER_ID == 0


def test_missing_optional_values_are_none(monkeypatch):
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)
    monkeypatch.delenv("BOT_TOKEN", raising=False)
    monkeypatch.delenv("STORE_NAME", raising=False)
    monkeypatch.delenv("BINANCE_ID", raising=False)

    module = importlib.reload(config)

    assert module.BOT_TOKEN is None
    assert module.STORE_NAME is None
    assert module.BINANCE_ID is None


def test_owner_id_must_be_numeric(monkeypatch):
    monkeypatch.setenv("OWNER_ID", "not-a-number")

    with pytest.raises(ValueError):
        importlib.reload(config)
