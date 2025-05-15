import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

API_KEY_OCR = 'K89209186988957'
TELEGRAM_TOKEN = '7829054927:AAEdh4zeYyWnRd0NOTWzgFGty8-3JPiL_Tc'

def ocr_space_file(filename, api_key):
    with open(filename, 'rb') as f:
        r = requests.post(
            'https://api.ocr.space/parse/image',
            files={filename: f},
            data={'apikey': api_key}
        )
    result = r.json()
    if result.get("ParsedResults"):
        return result["ParsedResults"][0].get("ParsedText", "متنی یافت نشد.")
    else:
        return "خطا در استخراج متن."

def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("ارسال عکس")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('سلام! لطفاً عکس خود را ارسال کنید تا متن آن استخراج شود.', reply_markup=reply_markup)

def handle_photo(update: Update, context: CallbackContext):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('photo.jpg')

    text = ocr_space_file('photo.jpg', API_KEY_OCR)
    update.message.reply_text(f"متن استخراج شده:\n{text}")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
