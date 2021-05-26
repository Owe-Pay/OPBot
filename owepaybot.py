import logging
import os

from uuid import uuid4
from telegram.utils.helpers import escape_markdown
from telegram.ext import InlineQueryHandler, Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, MessageHandler
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Update

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))

TOKEN = os.environ["API_TOKEN"]

def start(update, context): 
    """Depending if start was issued in a Group or via PM, it will execute the
    respective /start command."""
    if update.message.chat.type == 'group':
        startGroup(update, context)

    if update.message.chat.type == 'private':
        startPrivate(update, context)

def help(update, context):
    update.message.reply_text(
        "List of commands:\n\n" +
        "/start Initialise and register with us.\n" +
        "/help For the confused souls.\n" +
        "\nSplit bills with us by simply typing @OwePay_bot followed by the amount to be split!"
        )

def startGroup(update, context):
    """Send the welcome message when the command /start is issued in a group."""
    # The registration keyboard used to register groups into our Group Database.
    keyboard = [
        [
            InlineKeyboardButton("Register", callback_data='groupRegister'),
        ],
        [
            InlineKeyboardButton("Don't Register", callback_data='groupDontRegister')  
        ],
    ]

    ## This section is to send a logo before the registration process!
    # context.bot.send_photo(
    #     chat_id=update.effective_chat.id, 
    #     photo='https://res.cloudinary.com/jianoway/image/upload/v1621939877/O%24P%24_Logo.png',
    # )

    # Sets up the InlineKeyboardMarkup as the reply_markup to be used in the message.
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Sends the welcome message for the group.
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        "Hello this is O$P$, your personal Telegram loan chaser and debt tracker!\n\n" +
        "We aim to make the process of tracking which of your 'friends' still owe you " +
        "and reminding them as impersonal as possible so you won't feel the paiseh!"
        "Along with that, you can now also notify people who you've returned money to" +
        "with a simple click of a  button.\n\n" +
        "Simply register your group with us by pressing the button below!",
        reply_markup=reply_markup,
    )

def startPrivate(update, context):
    """Send the welcome message when the command /start is issued via PM"""
    # Logic check to be implemented:
    # 1. If user is not registered in our database
    # Registers the user as notifiable.
    #
    # 2. If user is already registered in our database BUT not notifiable:
    # Will register them as notifiable.
    #
    # 3. If user is already registered in our database and is also notifiable:
    # Will inform the user that his profile is already setup.
    #
    # Until we setup our database, the following boilerplate code will be executed.

    # The registration keyboard used to register groups into our User Database.
    keyboard = [
        [
            InlineKeyboardButton("Register", callback_data='userRegister'),
        ],
        [
            InlineKeyboardButton("Don't Register", callback_data='userDontRegister')  
        ],
    ]

    ## This section is to send a logo before the registration process!
    # context.bot.send_photo(
    #     chat_id=update.effective_chat.id, 
    #     photo='https://res.cloudinary.com/jianoway/image/upload/v1621939877/O%24P%24_Logo.png',
    # )

    # Sets up the InlineKeyboardMarkup as the reply_markup to be used in the message.
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        "Hi! Thank you for choosing O$P$, your one stop debt chaser!\n\n" +
        "Simply register with us by clicking pressing the button below!",
        reply_markup=reply_markup,
    )

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def inline(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    
    if query == "":
        return

    # print(query)

    # update.inline_query.from_user.send_message(query)
    results = inlineQueryHelper(update)

    update.inline_query.answer(results)

def inlineQueryHelper(update):
    query = update.inline_query.query
    if query.replace('$','',1).isdigit():
        query = query.replace('$','',1)
        return [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Split $" + str(query) + ".00 among everyone",
                input_message_content=InputTextMessageContent("Split among everyone: $" + query + ".00"),
                thumb_url='https://res.cloudinary.com/jianoway/image/upload/b_rgb:ffffff/v1621962373/icons8-user-groups-100_nxolfi.png',
            ),
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Split $" + str(query) + ".00 among some only",
                input_message_content=InputTextMessageContent("Split among some only: $" + query + ".00"),
                thumb_url='https://res.cloudinary.com/jianoway/image/upload/b_rgb:ffffff/v1621962386/icons8-user-groups-64_d9uktr.png'
            ),
        ]
    
    if query.replace('.', '', 1).replace('$','',1).isnumeric():
        query = query.replace('$', '', 1) + "00"
        queryfloat = float(query)
        formatted_query = "{:.2f}".format(queryfloat)
        return [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Split $" + formatted_query + " among everyone",
                input_message_content=InputTextMessageContent("Split among everyone: $" + formatted_query),
                thumb_url='https://res.cloudinary.com/jianoway/image/upload/b_rgb:ffffff/v1621962373/icons8-user-groups-100_nxolfi.png',

            ),
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Split $" + formatted_query + " among some only",
                input_message_content=InputTextMessageContent("Split among some only: $" + formatted_query),
                thumb_url='https://res.cloudinary.com/jianoway/image/upload/b_rgb:ffffff/v1621962386/icons8-user-groups-64_d9uktr.png'
            ),
        ]
    
    if isinstance(query, str):
        return [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=query + " is not a valid amount.",
                input_message_content=InputTextMessageContent(
                    "Trying to split invalid amount: \n" + query + "\n\nPlease key in a valid amount to split!"
                ),
                thumb_url='https://res.cloudinary.com/jianoway/image/upload/b_rgb:ffffff/v1621962567/icons8-cross-mark-96_zrk1p9.png',
            ),
        ]

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    choice = query.data

    if choice == 'groupRegister':
        groupRegister(update, context)

    if choice == 'groupDontRegister':
        groupDontRegister(update, context)

    if choice == 'userRegister':
        userRegister(update, context)

    if choice == 'userDontRegister':
        userDontRegister(update, context)

def groupRegister(update, context):
    query = update.callback_query
    context.bot.editMessageText(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id, 
        text="Your group is now registered!",
    )

def groupDontRegister(update, context):
    query = update.callback_query
    context.bot.editMessageText(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=
        "Thank you for your interest in our bot! We hope to see you soon!\n\n" +
        "If you ever feel like registering your Group with our bot in the future," +
        " simply run /start to get started!",
    )

def userRegister(update, context):
    query = update.callback_query
    context.bot.editMessageText(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id, 
        text="You are now registered!",
    )

def userDontRegister(update, context):
    query = update.callback_query
    context.bot.editMessageText(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=
        "Thank you for your interest in our bot! We hope to see you soon!\n\n" +
        "If you ever feel like registering with our bot in the future, simply run /start" +
        " to get started!",
    )

def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message for debugging purposes."""
    print(update)

def main():
    """Start the bot."""
    updater = Updater(
        TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CommandHandler("help", help))
    
    dp.add_handler(CallbackQueryHandler(button))

    dp.add_handler(InlineQueryHandler(inline))

    dp.add_handler(MessageHandler(Filters.text, echo))
    
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