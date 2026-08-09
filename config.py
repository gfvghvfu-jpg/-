import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()


def _required(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"متغير البيئة {name} غير موجود أو فارغ — أضفه إلى ملف .env"
        )
    return value


def _int_env(name, default):
    raw = os.getenv(name, default)
    try:
        return int(raw)
    except (TypeError, ValueError) as exc:
        raise RuntimeError(
            f"متغير البيئة {name} يجب أن يكون رقماً صحيحاً (القيمة الحالية: {raw!r})"
        ) from exc


# معلومات البوت
BOT_TOKEN = _required("BOT_TOKEN")
STORE_NAME = os.getenv("STORE_NAME", "Fluxo Store")

# بيانات الدفع
BINANCE_ID = os.getenv("BINANCE_ID")

# قاعدة البيانات
DATABASE_NAME = os.getenv("DATABASE_NAME", "fluxo.db")

# معرف المالك
OWNER_ID = _int_env("OWNER_ID", "0")
