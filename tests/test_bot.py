from unittest.mock import AsyncMock, MagicMock

import pytest
from telegram.ext import CommandHandler

import bot


@pytest.fixture
def update():
    update = MagicMock()
    update.effective_user.id = 12345
    update.effective_user.username = "fluxo_user"
    update.effective_user.full_name = "Fluxo User"
    update.message.reply_text = AsyncMock()
    return update


def test_main_keyboard_layout():
    rows = [
        [button.text for button in row] for row in bot.main_keyboard.keyboard
    ]

    assert rows == [
        ["🌍 شراء شريحة"],
        ["📦 طلباتي", "❤️ المفضلة"],
        ["🎁 كوبون خصم"],
        ["💬 الدعم", "👤 حسابي"],
    ]
    assert bot.main_keyboard.resize_keyboard is True


async def test_start_registers_the_user(monkeypatch, update):
    add_user = AsyncMock()
    monkeypatch.setattr(bot, "add_user", add_user)

    await bot.start(update, MagicMock())

    add_user.assert_awaited_once_with(12345, "fluxo_user", "Fluxo User")


async def test_start_replies_with_store_name_and_keyboard(monkeypatch, update):
    monkeypatch.setattr(bot, "add_user", AsyncMock())
    monkeypatch.setattr(bot, "STORE_NAME", "Fluxo Store")

    await bot.start(update, MagicMock())

    update.message.reply_text.assert_awaited_once()
    text, kwargs = (
        update.message.reply_text.await_args.args[0],
        update.message.reply_text.await_args.kwargs,
    )
    assert "Fluxo Store" in text
    assert kwargs["reply_markup"] is bot.main_keyboard


async def test_start_fails_when_user_cannot_be_stored(monkeypatch, update):
    monkeypatch.setattr(bot, "add_user", AsyncMock(side_effect=RuntimeError("boom")))

    with pytest.raises(RuntimeError):
        await bot.start(update, MagicMock())

    update.message.reply_text.assert_not_awaited()


async def test_main_creates_database_and_starts_polling(monkeypatch):
    create_database = AsyncMock()
    app = MagicMock()
    app.run_polling = AsyncMock()
    builder = MagicMock()
    builder.token.return_value.build.return_value = app

    monkeypatch.setattr(bot, "create_database", create_database)
    monkeypatch.setattr(bot, "BOT_TOKEN", "token-123")
    monkeypatch.setattr(bot.Application, "builder", MagicMock(return_value=builder))

    await bot.main()

    create_database.assert_awaited_once()
    builder.token.assert_called_once_with("token-123")
    app.run_polling.assert_awaited_once()

    handler = app.add_handler.call_args.args[0]
    assert isinstance(handler, CommandHandler)
    assert handler.commands == frozenset({"start"})
