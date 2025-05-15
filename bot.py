from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# جایگزین کن با توکن ربات خودت و API key سایت ocr.space
BOT_TOKEN = '7829054927:AAEdh4zeYyWnRd0NOTWzgFGty8-3JPiL_Tc'
OCR_API_KEY = 'K89209186988957'

keyboard = [['ارسال عکس']]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'سلام! لطفاً یک عکس بفرست تا متن داخلش رو برات بخونم.',
        reply_markup=markup
    )

# هندل عکس‌ها
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        file_path = await file.download_to_drive()

        with open(file_path, 'rb') as img_file:
            response = requests.post(
                'https://api.ocr.space/parse/image',
                files={'filename': img_file},
                data={'apikey': OCR_API_KEY, 'language': 'eng'}
            )

        result = response.json()
        text = result['ParsedResults'][0]['ParsedText'] if result['IsErroredOnProcessing'] == False else 'متأسفم، نتونستم متن رو استخراج کنم.'

        await update.message.reply_text(f'متن شناسایی‌شده:\n{text}')

    except Exception as e:
        await update.message.reply_text(f'خطا در پردازش تصویر: {str(e)}')

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
