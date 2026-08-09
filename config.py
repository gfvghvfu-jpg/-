import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# معلومات البوت
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set. Copy .env.example to .env and set it there."
    )

STORE_NAME = os.getenv("STORE_NAME", "Store")

# بيانات الدفع
BINANCE_ID = os.getenv("BINANCE_ID")

# قاعدة البيانات
DATABASE_NAME = os.getenv("DATABASE_NAME", "fluxo.db")

# معرف المالك
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
