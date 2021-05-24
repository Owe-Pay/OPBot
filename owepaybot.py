import logging
import os

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))

TOKEN = os.environ["API_TOKEN"]

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def inlineKeyboardTest(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def main():
    """Start the bot."""
    updater = Updater(
        TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram

    dp.add_handler(CommandHandler("testInline", inlineKeyboardTest))    

    # log all errors
    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url="https://owepaybot.herokuapp.com/" + TOKEN)
    # updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

