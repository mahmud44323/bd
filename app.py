import cv2
import numpy as np
from telegram import Update, InputFile, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Function to apply cartoon effect
def apply_cartoon_effect(image_path: str) -> str:
    # Read the image
    image = cv2.imread(image_path)
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur
    blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    # Detect edges
    detect_edge = cv2.adaptiveThreshold(blur_image, 255,
                                        cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY, 9, 9)
    # Bitwise AND to create cartoon effect
    color_image = cv2.bilateralFilter(image, 9, 300, 300)
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=detect_edge)
    
    # Save the output image
    output_path = "cartoon_effect.png"
    cv2.imwrite(output_path, cartoon_image)
    
    return output_path

# Start command handler
def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("Upload Image")],
        [KeyboardButton("Help")],
        [KeyboardButton("Cancel")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Welcome to the Cartoon Effect Bot! Please select an option:", reply_markup=reply_markup)

# Help command handler
def help_command(update: Update, context: CallbackContext):
    help_text = (
        "This bot applies a cartoon effect to images. "
        "You can upload an image by clicking the 'Upload Image' button. "
        "To start over, click 'Start'. "
        "To cancel at any time, click 'Cancel'."
    )
    update.message.reply_text(help_text)

# Cancel command handler
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("You have canceled the current operation. Click 'Start' to begin again.")
    start(update, context)  # Show the main menu again

# Handler for receiving photos
def handle_photo(update: Update, context: CallbackContext):
    # Get the photo from the message
    photo_file = update.message.photo[-1].get_file()
    photo_file.download("uploaded_image.png")
    
    # Apply the cartoon effect
    output_image_path = apply_cartoon_effect("uploaded_image.png")
    
    # Send back the cartoon image
    with open(output_image_path, 'rb') as img:
        update.message.reply_photo(photo=InputFile(img, filename='cartoon_effect.png'))
    
    # Return to the main menu
    start(update, context)

# Handler for text messages
def handle_text(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Upload Image":
        update.message.reply_text("Please send me an image to apply the cartoon effect.")
    elif text == "Help":
        help_command(update, context)
    elif text == "Cancel":
        cancel(update, context)
    else:
        update.message.reply_text("Please select a valid option or type /start to begin.")

def main():
    # Replace 'YOUR_TOKEN' with your actual Telegram bot token
    updater = Updater("7615742646:AAFhMMzt978vsaL64Zcr1Fh06WYz1TJM9V4", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command and message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    # Start the Bot
    updater.start_polling()
    
    # Run the bot until you send a signal to stop (Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()
