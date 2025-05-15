import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# جایگزین کن با API KEY سایت OCR.space
OCR_API_KEY = 'K89209186988957'

# جایگزین کن با توکن ربات تلگرام خودت
BOT_TOKEN = '7829054927:AAEdh4zeYyWnRd0NOTWzgFGty8-3JPiL_Tc'

# تابع استخراج متن از تصویر با استفاده از OCR.space
def ocr_space_image(file_path, api_key):
    with open(file_path, 'rb') as f:
        response = requests.post(
            'https://api.ocr.space/parse/image',
            files={'filename': f},
            data={'apikey': api_key, 'language': 'fas'}
        )
    result = response.json()
    try:
        return result['ParsedResults'][0]['ParsedText']
    except:
        return "خطا در پردازش تصویر."

# فرمان /start و کیبورد
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("ارسال عکس")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("سلام! لطفاً روی دکمه زیر کلیک کنید و یک عکس ارسال کنید.", reply_markup=reply_markup)

# هندل عکس
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_path = "received_image.jpg"
    await file.download_to_drive(file_path)

    await update.message.reply_text("در حال پردازش تصویر...")

    text = ocr_space_image(file_path, OCR_API_KEY)
    await update.message.reply_text(f"متن استخراج‌شده:\n{text}")

# تابع اصلی اجرای ربات
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()

if name == "main":
    main()
