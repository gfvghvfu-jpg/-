from telegram import (
    Update,
    ReplyKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import BOT_TOKEN, STORE_NAME
from database import create_database


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

    text = f"""
🌍 أهلاً بك في {STORE_NAME}

مرحباً بك في متجر الشرائح الإلكترونية.

اختر الخدمة التي تريدها من القائمة بالأسفل.
"""

    await update.message.reply_text(
        text,
        reply_markup=main_keyboard
    )


async def main():

    # إنشاء قاعدة البيانات
    await create_database()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("================================")
    print(" Fluxo Store Started ")
    print("================================")

    await app.run_polling()


if __name__ == "__main__":

    import asyncio

    asyncio.run(main())
