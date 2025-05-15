import logging
import pytesseract
from PIL import Image
import io
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# مسیر tesseract را تنظیم کن (مثلاً اگر در این مسیر نصب شده)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# توکن ربات را اینجا بگذار
BOT_TOKEN = "7829054927:AAEdh4zeYyWnRd0NOTWzgFGty8-3JPiL_Tc"

# فعال کردن لاگ برای دیباگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# دکمه ارسال عکس
keyboard = [["ارسال عکس"]]
reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لطفاً یکی از گزینه‌ها رو انتخاب کن:", reply_markup=reply_markup)

# دریافت عکس و پردازش OCR
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("در حال پردازش عکس...")

    photo = await update.message.photo[-1].get_file()
    photo_bytes = await photo.download_as_bytearray()

    try:
        image = Image.open(io.BytesIO(photo_bytes))
        text = pytesseract.image_to_string(image, lang='eng+fas')
    except Exception as e:
        await update.message.reply_text(f"خطا در پردازش عکس: {str(e)}")
        return

    if text.strip():
        await update.message.reply_text(f"متن داخل عکس:\n{text}")
    else:
        await update.message.reply_text("متنی داخل عکس پیدا نشد.")

# اجرای ربات
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()
