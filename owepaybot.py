import logging
from datetime import datetime, timedelta
import os
import sys

from HELPME.bot_sql_integration import *
from HELPME.helperFunctions import *

from uuid import uuid4, uuid1
from telegram.utils.helpers import escape_markdown
from telegram.ext import InlineQueryHandler, Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, MessageHandler
from telegram import Bot, InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Update, message, replymarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = os.environ["API_TOKEN"]
PORT = int(os.environ.get('PORT', '8443'))

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
        "with a simple click of a button.\n\n" +
        "Simply register your group with us by pressing the button below!",
        reply_markup=reply_markup,
    )

def startPrivate(update, context):
    """Send the welcome message when the command /start is issued via PM"""
    keyboard = [
        [
            InlineKeyboardButton("Register", callback_data='userRegister'),
        ],
        [
            InlineKeyboardButton("Don't Register", callback_data='userDontRegister')
        ],
    ]
    # Sets up the InlineKeyboardMarkup as the reply_markup to be used in the message.
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        "Hi! Thank you for choosing O$P$, your one stop debt chaser!\n\n" +
        "Simply register with us by clicking pressing the button below!",
        reply_markup=reply_markup,
    )

def getDebtors(update, context):
    
    userID = update.effective_chat.id
    
    if not userAlreadyAdded(userID):
        context.bot.send_message(
            chat_id=userID,
            text=
            "Please register with us first by using /start!"
        )
    
    unsettledTransactions = getUnsettledTransactionsForCreditor(userID)

    
    # user already added
    



def help(update, context):
    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        "List of commands:\n\n" +
        "/start Initialise and register with us.\n" +
        "/help For the confused souls.\n" +
        "\nSplit bills with us by simply typing @OwePay_bot followed by the amount to be split!"
    )

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def inline(update, context):
    query = update.inline_query.query
    if query == "":
        return
    results = inlineQueryHelper(update)
    update.inline_query.answer(results)

def button(update, context):
    """Handles the button presses for Inline Keyboard Callbacks"""
    query = update.callback_query
    choice = query.data
    query.answer()

    if choice == 'groupRegister':
        groupRegister(update, context)
        return query

    if choice == 'groupDontRegister':
        groupDontRegister(update, context)
        return query

    if choice == 'userRegister':
        userRegister(update, context)
        return query

    if choice == 'userDontRegister':
        userDontRegister(update, context)
        return query

    if choice == 'debtorPaid':
        debtorPaid(update, context)
        return query

    if choice == 'debtorUnpaid':
        debtorUnpaid(update, context)
        return query

    if choice == 'splitSomeEvenlyFinalise':
        splitSomeEvenly(update, context)
        return query

    if userAlreadyAdded(choice): #split some
        editMessageForSplitSome(update, context)
        return query

    

def editMessageForSplitSome(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    userID = query.from_user.id
    text = query.message.text

    if not (userIsCreditorForMessage(message_id, chat_id, userID)):
        return
        
    debtorID = query.data
    debtorUsername = getUsername(debtorID)

    if debtorUsername in text:
        text = removeUsernameFromDebtMessage(debtorUsername, text)
    else:
        text = addUsernameToDebtMessage(debtorUsername, text)
    
    context.bot.editMessageText(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=splitSomeEvenlyKeyboardMarkup(chat_id),
    )

    
def debtorPaid(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    username = query.from_user.username
    debtorID = query.from_user.id
    text = query.message.text
    textAfterRemove = removeUsernameFromDebtMessage(username, text)
    orderID = getOrderIDFromMessageAndGroupID(message_id, chat_id)
    creditorID = getCreditorIDFromMessageAndGroupID(message_id, chat_id)
    bot = Bot(TOKEN)

    if textAfterRemove != text:
        markTransactionAsSettled(creditorID, debtorID, orderID)
        bot.editMessageText(
            chat_id=chat_id,
            message_id=message_id,
            text=textAfterRemove,
            reply_markup=splitAllEvenlyKeyboardMarkup()
        )
    
    return None

def debtorUnpaid(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    username = query.from_user.username
    debtorID = query.from_user.id
    text = query.message.text
    textAfterAdd = addUsernameToDebtMessage(username, text)
    orderID = getOrderIDFromMessageAndGroupID(message_id, chat_id)
    creditorID = getCreditorIDFromMessageAndGroupID(message_id, chat_id)
    bot = Bot(TOKEN)

    if textAfterAdd != text:
        markTransactionAsUnsettled(creditorID, debtorID, orderID)
        bot.editMessageText(
            chat_id=chat_id,
            message_id=message_id,
            text=textAfterAdd,
            reply_markup=splitAllEvenlyKeyboardMarkup()
        )

    return None
    

def groupRegister(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    groupname = query.message.chat.title
    message_id = query.message.message_id
    group = (chat_id, groupname)
    if (groupAlreadyAdded(chat_id)):
        context.bot.editMessageText(
            chat_id=chat_id,
            message_id=message_id,
            text="Your group has already been registered with us."
        )
    else:
        addGroup(group)
        context.bot.editMessageText(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Your group is now registered!",
        )

def splitAllEvenly(update, context, userID, groupID):
    order = catchOrderFromUpdate(update)
    usersAndSplit = createTransactionBetweenAllUsers(order)
    userIDList = usersAndSplit.users
    splitAmount =  usersAndSplit.splitAmount

    setUserStateInactive(userID, groupID)
    resetUserTempAmount(userID, groupID)
        
    listOfUsernames = getUsernameListFromUserIDList(userIDList)
    usernameListString = formatListOfUsernames(listOfUsernames)
    orderName = order.orderName

    creditorUsername = '@' + getUsername(userID)
    text = "Please return %s $%s each for %s" % (creditorUsername, splitAmount, orderName)
    orderMessage = context.bot.send_message(
        chat_id=update.effective_chat.id,
            text=text + usernameListString,
            reply_markup=splitAllEvenlyKeyboardMarkup(),
    )
    messageID = orderMessage.message_id
    orderID = order.orderID
    # print(orderID)
    # print(orderMessage)
    addMessageIDToOrder(str(orderID), messageID)

def splitSomeEvenly(update, context):
    query = update.callback_query
    groupID = query.message.chat_id
    message_id = query.message.message_id
    userID = query.from_user.id
    text = query.message.text
    date = query.message.date + timedelta(hours=8)

    if not (userIsCreditorForMessage(message_id, groupID, userID)):
        return

    totalAmount = getUserTempAmount(userID, groupID)
    listOfUsers = tuple(text.replace("People who have your cash money:\n", "", 1).replace("\n",",",text.count("\n")).split(','))
    numberOfUsers = len(listOfUsers)

    if numberOfUsers == 0:
        return
    
    splitAmount = totalAmount / numberOfUsers
    orderID = getOrderIDFromUserIDAndGroupID(userID, groupID)
    orderName = getOrderNameFromOrderID(orderID)
    creditorUsername = getUsername(userID)
    
    listOfUserID = getUserIDListFromUsernameList(listOfUsers)

    if len(listOfUserID) < 1:
        return
    
    setUserStateInactive(userID, groupID)
    resetUserTempAmount(userID, groupID)
    resetUserTempOrderID(userID, groupID)

    

    messageText = "Please return @%s $%s each for %s" % (creditorUsername, splitAmount, orderName)
    for username in listOfUsers:
        messageText = messageText + '\n' + username

    if "\n@" + creditorUsername in messageText:
        messageText =  messageText.replace("\n@" + creditorUsername, "", 1)

    orderMessage = context.bot.editMessageText(
        chat_id=update.effective_chat.id,
        message_id=message_id,
        text=messageText,
        reply_markup=splitAllEvenlyKeyboardMarkup(),
    )
    order = Order(orderID, groupID, orderName, splitAmount, userID, date)
    messageID = orderMessage.message_id
    addMessageIDToOrder(str(orderID), messageID)
    createTransactionBetweenSomeUsers(order, listOfUserID)
    
def getTotalAmountFromMessage(update, context):
    chat_message=update.message.text
    value = int(''.join(filter(str.isdigit, chat_message)))
    total_amount = float(value/100)
    return total_amount


#############################
# when split among us is called this will update register the userid and the
# amount of money
##############

def messageContainsSplitAllEvenly(update, context):
    if "Split among everyone evenly" in update.message.text:
        total_amount = getTotalAmountFromMessage(update,context)
        user_id = update.message.from_user.id
        GroupID = update.message.chat_id
        updateUserStateSplitAllEvenly(user_id, GroupID)
        updateUserTempAmount(user_id,GroupID, total_amount)
        print("updated temp amount and state")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=
            "Hi Please send the name of the order!",
    )

def messageContainsSplitSomeEvenly(update, context):
    if "Split among some only" in update.message.text:
        total_amount = getTotalAmountFromMessage(update,context)
        user_id = update.message.from_user.id
        GroupID = update.message.chat_id
        updateUserStateSplitSomeEvenly(user_id, GroupID)
        updateUserTempAmount(user_id,GroupID, total_amount)
        print("updated temp amount and state")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=
            "Hi Please send the name of the order!",
    )

def catchOrderFromUpdate(update):
    print("caught request")
    order_id = str(uuid1())
    user_id = update.message.from_user.id
    group_id = update.message.chat_id
    order_name = update.message.text
    order_amount= getUserTempAmount(user_id,group_id)
    date = update.message.date + timedelta(hours=8)
    addOrder((order_id, group_id, order_name, order_amount, user_id, date))
    print("order added")
    return Order(order_id, group_id, order_name, order_amount, user_id, date)


def waitingForSomeNames(update, context, user_id, group_id):
    order = catchOrderFromUpdate(update)
    orderID = order.orderID

    updateUserStateWaitingForSomeNames(user_id, group_id)
    updateOrderIDToUserGroupRelational(user_id, group_id, orderID)
    # context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text=
    #         'Please send the name of the people in the following format:\n\n@user1\n@user2\netc'
    message = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='People who have your cash money:',
        reply_markup=splitSomeEvenlyKeyboardMarkup(update.effective_chat.id)
    )
    messageID = message.message_id
    addMessageIDToOrder(orderID, messageID)
        

def createTransactionBetweenAllUsers(order):
    #get all users involved
    creditorID= order.creditorID
    groupID = order.groupID
    users = getAllUsersExceptCreditor(creditorID, groupID)
    orderID = order.orderID
    date = order.date
    order_amount = order.orderAmount
    total_users = getNumberOfUsersExceptCreditor(creditorID, groupID) + 1
    splitAmount = order_amount / total_users

    for userID in users:
        transaction_id= str(uuid1())
        addTransaction((transaction_id, orderID, splitAmount, creditorID, userID, date))

    return UsersAndSplitAmount(users, splitAmount)

def createTransactionBetweenSomeUsers(order, userIDList):
    creditorID = order.creditorID
    orderID = order.orderID
    users = userIDList
    splitAmount = order.orderAmount
    date = order.date

    for userID in users:
        if str(userID) == str(creditorID):
            None
        else:
            transaction_id = str(uuid1())
            addTransaction((transaction_id, orderID, splitAmount, creditorID, userID, date))

    return UsersAndSplitAmount(users, splitAmount)



#order123 = ("b62aa85b-cb98-11eb-baef-d0509938caba",-524344128,'thai food',123.45,339096917)
#createTransactionbetweenallusers(order123)

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
    chat_id = query.message.chat_id
    username = query.message.chat.username
    message_id = query.message.message_id
    firstname = query.message.chat.first_name
    user = (chat_id, username, 1, firstname)
    if (userAlreadyAdded(chat_id)):
        if not(isNotifiable(chat_id)):
            makeNotifiable(chat_id)
            context.bot.editMessageText(
                chat_id=chat_id,
                message_id=message_id,
                text="You are now registered!",
            )
        else:
            context.bot.editMessageText(
                chat_id=chat_id,
                message_id=message_id,
                text="You have already been registered with us.",
            )
    else:
        addUser(user)
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
#############################
# checks if msg is sent from a bot
##############
def viabot_check(update, context):
    return (update.message.via_bot!=None)

# def echo(update: Update, _: CallbackContext) -> None:
def echo(update, context):
    """Echo the update for debugging purposes."""
    print(update)

def groupMemberScanner(update, context):
    """"Constantly monitors group chat to check if members are counted in the group or not"""
    group_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    firstname = update.message.from_user.first_name

    if not(groupAlreadyAdded(group_id)):
        return

    if not(userAlreadyAdded(user_id)):
        user = (user_id, username, 0, firstname)
        addUser(user)

    if not(userInGroup(user_id, group_id)):
        increaseGroupMemberCount(group_id)
        addUserToGroup(user_id, group_id)

    if userStateSplitAllEvenly(user_id, group_id):
        splitAllEvenly(update, context, user_id, group_id)
        
    if userStateSplitSomeEvenly(user_id, group_id):
        waitingForSomeNames(update, context, user_id, group_id)

    if viabot_check(update, context):
        messageContainsSplitAllEvenly(update, context)
        messageContainsSplitSomeEvenly(update, context)

def main():
    """Start the bot."""
    updater = Updater(
        TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", startGroup, Filters.chat_type.groups))
    dp.add_handler(CommandHandler("start", startPrivate, Filters.chat_type.private))
    # dp.add_handler(CommandHandler("whoowesme", getDebtors, Filters.chat_type.private))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(InlineQueryHandler(inline))
    #dp.add_handler(MessageHandler(Filters.chat_type.groups, echo))
    dp.add_handler(MessageHandler(Filters.chat_type.groups, groupMemberScanner))

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
