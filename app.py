import cv2
from telegram import Update, InputFile, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters  # Correctly import filters

def apply_cartoon_effect(image_path):
    image = cv2.imread(image_path)
    Gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    Blur_image = cv2.GaussianBlur(Gray_image, (3, 3), 0)
    detect_edge = cv2.adaptiveThreshold(Blur_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)
    
    output = cv2.bitwise_and(image, image, mask=detect_edge)
    output_image_path = 'cartoon_effect.png'
    cv2.imwrite(output_image_path, output)
    return output_image_path

def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("Upload Image")],
        [KeyboardButton("Help")],
        [KeyboardButton("Cancel")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Welcome to the Cartoon Effect Bot! Please select an option:", reply_markup=reply_markup)

def handle_photo(update: Update, context: CallbackContext):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download("uploaded_image.png")
    output_image_path = apply_cartoon_effect("uploaded_image.png")
    
    with open(output_image_path, 'rb') as img:
        update.message.reply_photo(photo=InputFile(img, filename='cartoon_effect.png'))
    
    start(update, context)

def handle_text(update: Update, context: CallbackContext):
    update.message.reply_text("Please upload an image or use one of the buttons.")

def main():
    # Replace 'YOUR_TOKEN' with your actual Telegram bot token
    updater = Updater("7615742646:AAFhMMzt978vsaL64Zcr1Fh06WYz1TJM9V4", use_context=True)
    dp = updater.dispatcher

    # Register command and message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.PHOTO, handle_photo))  # Updated Filters usage
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))  # Updated Filters usage

    # Start the Bot
    updater.start_polling()
    
    # Run the bot until you send a signal to stop (Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()
