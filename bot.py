import asyncio
import html
import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.error import TelegramError
from telegram.ext import Application, CommandHandler, ContextTypes

from config import BOT_TOKEN, OWNER_ID, STORE_NAME
from database import create_database, add_user

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# القائمة الرئيسية
main_keyboard = ReplyKeyboardMarkup(
    [
        ["🌍 شراء شريحة"],
        ["📦 طلباتي", "❤️ المفضلة"],
        ["🎁 كوبون خصم"],
        ["💬 الدعم", "👤 حسابي"]
    ],
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    message = update.effective_message

    if user is None or message is None:
        logger.warning("Ignoring /start update without user or message: %s", update)
        return

    try:
        await add_user(
            user.id,
            user.username,
            user.full_name
        )
    except Exception:
        # لا نمنع المستخدم من استخدام المتجر، لكن يجب ألا يمرّ الخطأ بصمت
        logger.exception("Failed to store user %s", user.id)

    text = f"""
🌍 أهلاً بك في {STORE_NAME}

مرحباً بك في متجر الشرائح الإلكترونية.

اختر الخدمة التي تريدها من القائمة بالأسفل.
"""

    await message.reply_text(
        text,
        reply_markup=main_keyboard
    )


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE):
    """يسجّل أي خطأ غير متوقع ويُبلغ المستخدم والمالك بدلاً من تجاهله."""

    logger.exception("Unhandled error while processing update", exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "⚠️ حدث خطأ غير متوقع. حاول مرة أخرى أو تواصل مع الدعم."
            )
        except TelegramError:
            logger.exception("Failed to notify user about the error")

    if OWNER_ID:
        try:
            await context.bot.send_message(
                OWNER_ID,
                f"⚠️ خطأ في البوت:\n<code>{html.escape(repr(context.error))}</code>",
                parse_mode="HTML"
            )
        except TelegramError:
            logger.exception("Failed to notify owner about the error")


def main():

    asyncio.run(create_database())

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_error_handler(on_error)

    logger.info("%s started", STORE_NAME)

    app.run_polling()


if __name__ == "__main__":

    main()
