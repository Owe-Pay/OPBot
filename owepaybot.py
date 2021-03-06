import logging
# from datetime import *
from datetime import datetime, timedelta
import time
import os
import sys
from tokenize import Token
import pytz
import re
import requests

from HELPME.bot_sql_integration import *
from HELPME.helperFunctions import *

from uuid import uuid4, uuid1
from telegram.utils.helpers import escape_markdown
from telegram.ext import InlineQueryHandler, Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, MessageHandler, ConversationHandler
from telegram import Bot, InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Update, message, replymarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

tz = pytz.timezone('Asia/Singapore')
now = datetime.now(tz).replace(microsecond=0) # the current time in your local timezone

logger = logging.getLogger(__name__)
TOKEN = os.environ["API_TOKEN"]
PORT = int(os.environ.get('PORT', '8443'))
BOT_ID = os.environ['BOT_ID']

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
    message = context.bot.send_message(
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
    return message

def startPrivate(update, context):
    """Send the welcome message when the command /start is issued via PM"""
    chat_id = update.message.chat_id
    username = update.message.chat.username
    firstname = update.message.chat.first_name
    user = (chat_id, username, 1, firstname)

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

    message = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        "Hi! Thank you for choosing O$P$, your one stop debt chaser!\n\n" +
        "Simply register with us by clicking pressing the button below!",
        reply_markup=reply_markup,
    )
    return message

def scanReceiptPrivateMessage(update, context):
    """Prompt the user to send their receipt."""
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text=
            "Please send in the receipt to be scanned! Alternatively, to cancel please type /cancelreceipt"
    )
    return "waitingonpicprivate"

def scanReceiptPrivatePicture(update, context):
    """Parses the image if possible, otherwise will prompt user to send a valid image."""
    photos = update.message.photo
    length = len(photos)
    if length == 0:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=
                "Please send in the receipt to be scanned! Alternatively, to cancel please type /cancelreceipt"
        )
        return "waitingonpicprivate"
    else:
        photo = photos[length - 1]
        fileID = photo.file_id
        filePathURL = "https://api.telegram.org/bot%s/getfile?file_id=%s" % (TOKEN, fileID)
        filePath = requests.get(filePathURL).json()["result"]["file_path"]
        fileURL = "https://api.telegram.org/file/bot%s/%s" % (TOKEN, filePath)
        text = receiptParser(fileURL)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text
        )
        return ConversationHandler.END

def cancelReceipt(update, context):
    """Cancels the receipt scanning procedure."""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
            "Your receipt scan has been cancelled!"
    )
    print('ok')
    return ConversationHandler.END


def getDebtors(update, context):
    """Sends the user the message in response to the /whoowesme command."""
    userID = update.effective_chat.id
    if not isNotifiable(userID):
        message = context.bot.send_message(
            chat_id=userID,
            text=
            "Please register with us first by using /start!"
        )
        return message
        
    
    unsettledTransactions = getUnsettledTransactionsForCreditor(userID)
    keyboardMarkup = formatTransactionsForCreditorKeyboardMarkup(unsettledTransactions)

    if len(unsettledTransactions) < 1:
        message = context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='No one owes you money! What great friends you have!!!'
        )
        return message

    message = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='The baddies who have your cash money! >:(',
        reply_markup=keyboardMarkup
    )
    return message

def getCreditors(update, context):
    """Sends the user the message in response to the /whomeowes command."""
    userID = update.effective_chat.id
    if not isNotifiable(userID):
        message = context.bot.send_message(
            chat_id=userID,
            text=
            "Please register with us first by using /start!"
        )
        return message
    
    unsettledTransactions = getUnsettledTransactionsForDebtor(userID)
    keyboardMarkup = formatTransactionsForDebtorKeyboardMarkup(unsettledTransactions)

    if len(unsettledTransactions) < 1:
        message = context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Wow! Amazing! You don't owe anyone any money!"
        )
        return message
    message = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="The kind people who you've taken from:",
        reply_markup=keyboardMarkup
    )
    return message
    
def cancel(update, context):
    """Cancels any ongoing operation for the user in a group."""
    groupID = update.effective_chat.id
    userID = update.message.from_user.id
    messageID = update.message.message_id
    setUserStateInactive(userID, groupID)
    resetUserTempAmount(userID, groupID)
    resetUserTempOrderID(userID, groupID)
    resetUserTempMessageID(userID, groupID)
    context.bot.send_message(
        chat_id=groupID,
        reply_to_message_id=messageID,
        text="I've been cancelled!"
    )

def help(update, context):
    """Sends the user the help message."""
    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        "List of commands:\n\n" +
        "/start Initialise and register with us.\n" +
        "/help For the confused souls.\n" +
        "/whoowesme To see your debtors (only in private message).\n" +
        "/whomeowes To see your creditors (only in private message).\n"+
        "/cancel To cancel any creation of order.\n"
        "\nAfter running /start and registering in the group you wish to split bills in, you can start splitting your bills by simply typing @OwePay_bot followed by name of the order." +
        "\n\nDue to the nature of Telegram Bots, our bot will only be able to detect users if they have either sent a message in the group after I've been added or users added after me!" 
    )

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def inline(update, context):
    """Handles the Inline Queries sent by the user."""
    query = update.inline_query.query
    if query == "":
        return
    results = inlineQueryHelper(update)
    update.inline_query.answer(results)

def button(update, context):
    """Handles the button presses for Inline Keyboard Callbacks"""
    query = update.callback_query
    choice = query.data
    username = query.message.chat.username

    if username == None or not 'test,bot' in username: # this is safe because ',' is an invalid character for telegram usernames
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

    if choice == 'debtorEvenlyPaid':
        debtorEvenlyPaid(update, context)
        return query

    if choice == 'debtorEvenlyUnpaid':
        debtorEvenlyUnpaid(update, context)
        return query

    if choice == 'SplitEvenlyFinalise':
        splitEvenly(update, context)
        return query

    if 'splitevenlycallbackdata' in choice:
        user = choice.replace('splitevenlycallbackdata', '', 1)
        if userAlreadyAdded(user): #split some
            editMessageForSplitEvenly(update, context)
            return query
    
    if 'settledebtforcreditor' in choice:
        settleDebtForCreditor(update, context)

    if 'settledebtfordebtor' in choice:
        settleDebtForDebtor(update, context)
    
    if 'notifydebtorcallbackdata' in choice:
        notifyUserFromPrivateMessage(update, context)
     
    if 'splitunevenlycallbackdata' in choice:
        editUnevenlyMessageIndividual(update, context)

    if choice == 'splitevenlyaddeveryonecallbackdata':
        editSplitEvenlyAddEveryone(update, context)

    if choice == 'splitunevenlyaddeveryonecallbackdata':
        editSplitUnevenlyAddEveryone(update, context)


    if choice == 'splitunevenlynextitem':
        splitUnevenlyNextItem(update, context)
    
    if choice == 'goodservicetax':
        splitGST(update, context)
    
    if choice == 'servicechargecallbackdata':
        splitSVC(update, context)
    
    if choice == 'splitunevenlyfinalise':
        splitUnevenlyFinalise(update, context)
    
    if choice == 'debtorUnevenlyPaid':
        debtorUnevenlyPaid(update, context)

    if choice == 'debtorUnevenlyUnpaid':
        debtorUnevenlyUnpaid(update, context)

    if choice == 'newordersplitevenly':
        newOrderSplitEvenly(update, context)

    if choice == 'newordersplitunevenly':
        newOrderSplitUnevenly(update, context)

def newOrderSplitUnevenly(update, context):
    """Prompts the user to send in the list of items to be added to the order."""
    query = update.callback_query
    groupID = query.message.chat_id
    message_id = query.message.message_id
    userID = query.from_user.id

    if not userStateNewOrder(userID, groupID) and userIsMessageCreator(userID, groupID, message_id):
        return
    
    order = catchSplitUnevenlyOrder(userID, groupID)
    orderID = order.orderID
    updateOrderIDToUserGroupRelational(userID, groupID, orderID)
    setOrderDifferentAmountsFromOrderID(orderID)
    message = context.bot.editMessageText(
        chat_id=groupID,
        message_id=message_id,
        text='Please send in the items in the following format:\nItem Name - Price\n\nFor example:\nChicken Rice - 5\nCurry Chicken - 5.50\nNasi Lemak - 4'
    )
    updateUserStateSplitUnevenly(userID, groupID)
    return message


def newOrderSplitEvenly(update, context):
    """Prompts the user to send in the amount to be split in the order."""
    query = update.callback_query
    groupID = query.message.chat_id
    message_id = query.message.message_id
    userID = query.from_user.id

    if not userStateNewOrder(userID, groupID) and userIsMessageCreator(userID, groupID, message_id):
        return
    
    message = context.bot.editMessageText(
        chat_id=groupID,
        message_id=message_id,
        text='Please send in the amount to split!'
    )
    updateUserStateSplitEvenly(userID, groupID)
    return message
    

    
    
def debtorUnevenlyPaid(update, context):
    """"""
    query = update.callback_query
    groupID = query.message.chat_id
    message_id = query.message.message_id
    debtorID = query.from_user.id
    debtorUsername = getUsername(debtorID)
    text = query.message.text
    orderID = frOrderIDFromMessageAndGroupID(message_id, groupID)
    creditorID = getCreditorIDFromMessageAndGroupID(message_id, groupID)

    if str(creditorID) == str(debtorID):
        return

    transactionID = getTransactionIDFromOrderIDCreditorIDDebtorID(orderID, creditorID, debtorID)
    amountOwed = getAmountOwedFromTransactionID(transactionID)

    textList = text.split('\n')
    edited = False
    newTextList = []
    for item in textList:
        if not '(@' + debtorUsername + ')' in item:
            newTextList.append(item + '\n')
        else:
            edited = True
            markTransactionAsSettled(creditorID, debtorID, orderID)
    newText = ''.join(newTextList)
    if edited:
        context.bot.editMessageText(
            chat_id=groupID,
            message_id=message_id,
            text=newText,
            reply_markup=splitUnevenlyFinalisedKeyboardMarkup()
        )

def debtorUnevenlyUnpaid(update, context):
    query = update.callback_query
    groupID = query.message.chat_id
    message_id = query.message.message_id
    debtorID = query.from_user.id
    debtorUsername = getUsername(debtorID)
    text = query.message.text
    orderID = getOrderIDFromMessageAndGroupID(message_id, groupID)
    creditorID = getCreditorIDFromMessageAndGroupID(message_id, groupID)

    if str(creditorID) == str(debtorID):
        return

    transactionID = getTransactionIDFromOrderIDCreditorIDDebtorID(orderID, creditorID, debtorID)
    amountOwed = getAmountOwedFromTransactionID(transactionID)

    textList = text.split('\n')
    alreadyInside = False
    newTextList = []
    for item in textList:
        if '(@' + debtorUsername + ')' in item:
            newTextList.append(item + '\n')
            alreadyInside = True
        else:
            newTextList.append(item + '\n')

    if not alreadyInside:
        debtorName = getFirstName(debtorID)
        stringToAdd = '%s (@%s) - $%s\n' %(debtorName, debtorUsername, amountOwed)
        newTextList.append(stringToAdd)
        newText = ''.join(newTextList)
        context.bot.editMessageText(
            chat_id=groupID,
            message_id=message_id,
            text=newText,
            reply_markup=splitUnevenlyFinalisedKeyboardMarkup()
        )
    

def splitUnevenlyFinalise(update, context):
    query = update.callback_query
    groupID = query.message.chat_id
    message_id = query.message.message_id
    userID = query.from_user.id
    text = query.message.text
    date = datetime.now(tz).replace(microsecond=0)

    if not (userIsCreditorForMessage(message_id, groupID, userID)):
        return
    
    orderID = getOrderIDFromUserIDAndGroupID(userID, groupID)
    creditorUsername = getUsername(userID)
    textList = text.split('\n')
    userList = []
    debtList = []
    for item in textList:
        if '-' in item:
            if '(@' + creditorUsername + ')' in item: 
                continue
            debtList.append(item)
            noBrackets = item.replace('(', '`')
            noBracketsList = noBrackets.split('`')
            for noBrack in noBracketsList:
                user = ''
                if '@' in noBrack:
                    user = noBrack
                    
                if user != '':
                    user = user.split(') - $')
                    userList.append(user)

    for user in userList:
        username = user[0]
        debtorID = getUserIDFromUsername(username.replace('@', '', 1))
        if username.replace('@', '', 1) == creditorUsername:
            continue
        amountOwed = user[1]
        transactionID = str(uuid1())
        addTransaction((transactionID, orderID, amountOwed, userID, debtorID, date))
    
    newDebtorList = []
    for debtor in debtList:
        newDebtorList.append(debtor + '\n')
    debtorString = ''.join(newDebtorList)
    orderName = getOrderNameFromOrderID(orderID)
    messageText = "Please return %s their cash money for %s!\n\n%s" % ('@' + creditorUsername, orderName, debtorString)
    orderMessage = context.bot.editMessageText(
        chat_id=groupID,
        message_id=message_id,
        text=messageText,
        reply_markup=splitUnevenlyFinalisedKeyboardMarkup()
    )
    resetUserTempOrderID(userID, groupID)
    resetUserTempMessageID(userID, groupID)

        
def splitGST(update, context):
    query = update.callback_query
    userID = query.from_user.id
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    text = query.message.text
    textList = text.split('\n')
    newTextList = []
    if 'w/ GST' in text:
        for itemWithoutPara in textList:
            newItem = itemWithoutPara
            if 'People paying for ' in itemWithoutPara:
                if 'and SVC' in itemWithoutPara:
                    newItem = itemWithoutPara.replace('w/ GST and ', 'w/ ', 1)
                else:
                    newItem = itemWithoutPara.replace(' w/ GST:', ':', 1)
            tempSplitList = itemWithoutPara.split('-')
            tempSplitItem = tempSplitList[len(tempSplitList) - 1]
            if len(tempSplitList) > 0 and tempSplitList[0] != '':
                currentAmount = re.sub(r"[^\d.]+", "", str(tempSplitItem))
                if (isValidAmount(currentAmount)):
                    newAmount = getFormattedAmountFromString(float(currentAmount) / 1.07)
                    newItem = newItem.replace('$%s' % str(currentAmount), '$%s' % newAmount, 1)
            newTextList.append(newItem + '\n')
    else:
        for itemWithoutPara in textList:
            newItem = itemWithoutPara
            if 'People paying for ' in itemWithoutPara:
                if 'w/ SVC' in itemWithoutPara:
                    newItem = itemWithoutPara.replace('w/ ', 'w/ GST and ', 1)
                else:
                    newItem = itemWithoutPara.replace(':', ' w/ GST:', 1)
            tempSplitList = itemWithoutPara.split('-')
            tempSplitItem = tempSplitList[len(tempSplitList) - 1]
            if len(tempSplitList) > 0 and tempSplitList[0] != '':
                currentAmount = re.sub(r"[^\d.]+", "", str(tempSplitItem))
                if (isValidAmount(currentAmount)):
                    newAmount = getFormattedAmountFromString(float(currentAmount) * 1.07)
                    newItem = newItem.replace('$%s' % str(currentAmount), '$%s' % newAmount, 1)
            newTextList.append(newItem + '\n')
    
    newMessage = ''.join(newTextList)

    context.bot.editMessageText(
        chat_id=chat_id,
        message_id=message_id,
        text=newMessage,
        reply_markup=query.message.reply_markup
    )
        
            
def splitSVC(update, context):
    query = update.callback_query
    userID = query.from_user.id
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    text = query.message.text
    textList = text.split('\n')
    newTextList = []

    if not userIsCreditorForMessage(message_id, chat_id, userID):
        return

    if ' SVC:' in text:
        for itemWithoutPara in textList:
            newItem = itemWithoutPara
            if 'People paying for ' in itemWithoutPara:
                if 'w/ GST' in itemWithoutPara:
                    newItem = itemWithoutPara.replace(' and SVC:', ':', 1)
                else:
                    newItem = itemWithoutPara.replace(' w/ SVC:', ':', 1)
            tempSplitList = itemWithoutPara.split('-')
            tempSplitItem = tempSplitList[len(tempSplitList) - 1]
            if len(tempSplitList) > 0 and tempSplitList[0] != '':
                currentAmount = re.sub(r"[^\d.]+", "", str(tempSplitItem))
                if (isValidAmount(currentAmount)):
                    newAmount = getFormattedAmountFromString(float(currentAmount) / 1.1)
                    newItem = newItem.replace('$%s' % str(currentAmount), '$%s' % newAmount, 1)
            newTextList.append(newItem + '\n')
    else:
        for itemWithoutPara in textList:
            newItem = itemWithoutPara
            if 'People paying for ' in itemWithoutPara:
                if 'w/ GST:' in itemWithoutPara:
                    newItem = itemWithoutPara.replace(':', ' and SVC:', 1)
                else:
                    newItem = itemWithoutPara.replace(':', ' w/ SVC:')
            tempSplitList = itemWithoutPara.split('-')
            tempSplitItem = tempSplitList[len(tempSplitList) - 1]
            if len(tempSplitList) > 0 and tempSplitList[0] != '':
                currentAmount = re.sub(r"[^\d.]+", "", str(tempSplitItem))
                if (isValidAmount(currentAmount)):
                    newAmount = getFormattedAmountFromString(float(currentAmount) * 1.1)
                    newItem = newItem.replace('$%s' % str(currentAmount), '$%s' % newAmount, 1)
            newTextList.append(newItem + '\n')
        
    newMessage = ''.join(newTextList)

    context.bot.editMessageText(
        chat_id=chat_id,
        message_id=message_id,
        text=newMessage,
        reply_markup=query.message.reply_markup
    )
            

def splitUnevenlyNextItem(update, context):
    query = update.callback_query
    userID = query.from_user.id
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if not (userIsCreditorForMessage(message_id, chat_id, userID)):
        return
    orderID = getOrderIDFromUserIDAndGroupID(userID, chat_id)
    orderName = getOrderNameFromOrderID(orderID)
    text = query.message.text
    textList = text.split('\n')
    itemToRemove = ''
    for item in textList:
        if 'People paying for ' in item:
            itemToRemove = item
    
    itemToRemovePosition = textList.index(itemToRemove)
    itemsLeftToSplitTitlePosition = textList.index('Items left to split:')
    count = -1
    userListToAdd = []
    for item in textList:
        count += 1
        if count <= itemToRemovePosition:
            continue
        else:
            userListToAdd.append(item)

    numOfUsersToAdd = len(userListToAdd)
    if numOfUsersToAdd < 1:
        return
    
    currentSplitList = []
    cleanAmountList = itemToRemove.split('(')
    cleanAmount = cleanAmountList[len(cleanAmountList) - 1]
    amountBeforeSplit = float(re.sub(r"[^\d.]+", "", cleanAmount))
    amountAfterSplit = amountBeforeSplit / numOfUsersToAdd

    count = -1
    for item in textList:
        count += 1
        if count < itemsLeftToSplitTitlePosition and count != 0 and item != '':
            currentSplitList.append(item)
        else:
            continue
    for userToAdd in userListToAdd:
        inside = False
        for splitUser in currentSplitList:
            if userToAdd in splitUser:
                splitUserPosition = currentSplitList.index(splitUser)
                inside = True
                splitUserList = splitUser.split('-')
                tempSplitUser = splitUserList[len(splitUserList) - 1]
                currentAmount = float(re.sub(r"[^\d.]+", "", tempSplitUser))

                newAmount = getFormattedAmountFromString(currentAmount + amountAfterSplit)
                print(newAmount)
                currentSplitList[splitUserPosition] = userToAdd + ' - $' + newAmount
        if not inside:
            currentSplitList.append(userToAdd + ' - $' + getFormattedAmountFromString(amountAfterSplit))
    itemList = []
    count = -1
    for item in textList:
        count += 1
        if count > itemsLeftToSplitTitlePosition and count < itemToRemovePosition and item != '':
            itemList.append(item)
    numOfItemsLeft = len(itemList)
    last = numOfItemsLeft < 1
    
    
    if not last:
        nextItem = itemList.pop(0)
        newItemList = []
        for item in itemList:
            newItemList.append(item + '\n')
        itemListString = ''.join(newItemList)
        newSplitUserList = []
        for splitUser in currentSplitList:
            newSplitUserList.append(splitUser + '\n')
        splitUserString = ''.join(newSplitUserList)
        messageText = 'Current split for %s:\n%s\nItems left to split:\n%s\nPeople paying for %s:' % (orderName, splitUserString, itemListString, nextItem)
        context.bot.editMessageText(
            chat_id=chat_id,
            message_id=message_id,
            text=messageText,
            reply_markup=splitUnevenlyKeyboardMarkup(chat_id, last)
        )
    else:
        newSplitUserList = []
        totalAmount = float(0)
        for splitUser in currentSplitList:
            newSplitUserList.append(splitUser + '\n')
            tempSplitUserList = splitUser.split('-')
            tempSplitUser = tempSplitUserList[len(tempSplitUserList) - 1]
            currentAmount = float(re.sub(r"[^\d.]+", "", tempSplitUser))
            totalAmount += currentAmount
        formattedTotal = getFormattedAmountFromString(totalAmount)
        splitUserString = ''.join(newSplitUserList)
        messageText = 'People paying for %s:\n%s\nTotal: $%s' % (orderName, splitUserString, formattedTotal)
        context.bot.editMessageText(
            chat_id=chat_id,
            text=messageText,
            message_id=message_id,
            reply_markup=splitUnevenlyKeyboardMarkup(chat_id, last),
        )


def editUnevenlyMessageIndividual(update, context):
    query = update.callback_query
    debtorID = query.data.replace('splitunevenlycallbackdata', '', 1)
    userID = query.from_user.id
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    
    if not (userIsCreditorForMessage(message_id, chat_id, userID)):
        return
    
    text = query.message.text
    textList = text.split('\n')
    debtorName = getFirstName(debtorID)
    debtorUsername = getUsername(debtorID)
    debtorToAdd = debtorName + ' (@' + debtorUsername + ')'
    if debtorToAdd in textList:
        textList.remove(debtorToAdd)
    else:
        textList.append(debtorToAdd)
    newTextList = []
    for text in textList:
        newTextList.append(text + '\n')

    newText = ''.join(newTextList)

    context.bot.editMessageText(
        chat_id=chat_id,
        message_id=message_id,
        text=newText,
        reply_markup=query.message.reply_markup
    )

def editSplitEvenlyAddEveryone(update, context):
    query = update.callback_query
    userID = query.from_user.id
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    text = query.message.text
    if not (userIsCreditorForMessage(message_id, chat_id, userID)):
        return
    
    userList = getAllUsersFromGroup(chat_id)
    listOfUsersWithNameAndUsername = []
    
    for user in userList:
        username = getUsername(user)
        firstName = getFirstName(user)
        entry = '\n' + firstName + ' (@' + username + ')'
        if entry not in text:
            listOfUsersWithNameAndUsername.append(entry)
    
    newText = text + ''.join(listOfUsersWithNameAndUsername)
    
    if newText == text:
        return

    context.bot.editMessageText(
        chat_id=chat_id,
        message_id=message_id,
        text=newText,
        reply_markup=query.message.reply_markup
    )

def editSplitUnevenlyAddEveryone(update, context):
    query = update.callback_query
    userID = query.from_user.id
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    text = query.message.text
    if not (userIsCreditorForMessage(message_id, chat_id, userID)):
        return
    
    # relevantHalf = text.split('People paying for ')[1]
    userList = getAllUsersFromGroup(chat_id)
    listOfUsersWithNameAndUsername = []
    
    splitByPara = text.split('\n')

    for user in userList:
        username = getUsername(user)
        firstName = getFirstName(user)
        entry = firstName + ' (@' + username + ')'
        if entry not in splitByPara:
            listOfUsersWithNameAndUsername.append('\n' + entry)
    
    newText = text + ''.join(listOfUsersWithNameAndUsername)

    if text == newText:
        return

    context.bot.editMessageText(
        chat_id=chat_id,
        message_id=message_id,
        text=newText,
        reply_markup=query.message.reply_markup
    )

    # text = query.message.text



def notifyUserFromPrivateMessage(update, context):
    query = update.callback_query
    transactionID = query.data.replace('notifydebtorcallbackdata', '', 1)

    lastNotifiedTime = getLastNotifiedTimeFromTransactionID(transactionID)
    currentTime = datetime.now(tz).replace(microsecond=0)
    to_add = timedelta(minutes=60)
    thresholdTime = lastNotifiedTime + to_add    

    debtorID = getDebtorIDFromTransactionID(transactionID)
    creditorID = getCreditorIDFromTransactionID(transactionID)
    debtorName = getFirstName(debtorID)
    debtorUsername = getUsername(debtorID)
    orderID = getOrderIDFromTransactionID(transactionID)
    orderName = getOrderNameFromOrderID(orderID)
    orderDate = getOrderDateFromOrderID(orderID)
    formattedDate = orderDate.strftime("%d %B %Y")
    groupID = getGroupIDFromOrder(orderID)
    groupName = getGroupNameFromGroupID(groupID)
    
    if not isNotifiable(debtorID):
        context.bot.send_message(
            chat_id=creditorID,
            text = '%s (@%s) is not notifiable.' % (debtorName, debtorUsername)
        )
        return

    if currentTime.replace(tzinfo=None) < thresholdTime.replace(tzinfo=None):
        timediff = currentTime.replace(tzinfo=None) - lastNotifiedTime.replace(tzinfo=None)
        timeTillNextSend = 60 - int(timediff.total_seconds()/60)
        context.bot.send_message(
            chat_id=creditorID,
            text = 'You have notified %s (@%s) too recently for %s on %s in %s. Please try again in %s minutes!' % (debtorName, debtorUsername, orderName, formattedDate, groupName, timeTillNextSend)
        )  
        return 
    updateLastNotifiedTimeWithTransactionID(transactionID, currentTime)

    creditorName = getFirstName(creditorID)
    creditorUsername = getUsername(creditorID)
    amountOwed = getAmountOwedFromTransactionID(transactionID)
    formattedAmount = getFormattedAmountFromString(amountOwed)

    context.bot.send_message(
        chat_id=debtorID,
        text='Hi %s! Your friend %s (@%s) from the group %s is asking you to return them their $%s for %s %s.' % (debtorName, creditorName, creditorUsername,groupName, formattedAmount, orderName, formattedDate)
    )
    context.bot.send_message(
        chat_id=creditorID,
        text='%s (@%s) has been notified to return $%s for %s in %s' % (debtorName, debtorUsername, formattedAmount, orderName, groupName)
    )

def updateOrderMessageAsSettledWhenTransactionSettled(transactionID):
    if transactionAlreadySettled(transactionID):
        return
    bot = Bot(TOKEN)
    orderID = getOrderIDFromTransactionID(transactionID)
    debtorID = getDebtorIDFromTransactionID(transactionID)
    messageID = getMessageIDFromOrder(orderID)
    groupID = getGroupIDFromOrder(orderID)
    
    debtorName = getFirstName(debtorID)
    debtorUsername = getUsername(debtorID)
    entry = '%s (@%s)' % (debtorName, debtorUsername)

    isEven = orderIsEvenlySplit(orderID)

    placeholderGroupMessage = bot.forward_message(
        chat_id = -528685244,
        from_chat_id=groupID,
        message_id=messageID,
    )
    text = placeholderGroupMessage.text

    textList = text.split('\n')

    newTextList =[]
    for item in textList:
        if entry in item:
            continue
        else:
            newTextList.append(item + '\n')

    newText = ''.join(newTextList)

    reply_markup = ''

    if isEven:
        reply_markup = splitEvenlyFinalisedKeyboardMarkup()
    else:
        reply_markup = splitUnevenlyFinalisedKeyboardMarkup()
    
    bot.editMessageText(
        chat_id=groupID,
        message_id=messageID,
        text=newText,
        reply_markup=reply_markup,
    )
        

def settleDebtForCreditor(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    userID = query.from_user.id
    text = query.message.text

    transactionID = query.data.replace('settledebtforcreditor', '', 1)
    updateTransactionAsSettledWithTransactionID(transactionID)
    updateOrderMessageAsSettledWhenTransactionSettled(transactionID)

    unsettledTransactions = getUnsettledTransactionsForCreditor(userID)
    keyboardMarkup = formatTransactionsForCreditorKeyboardMarkup(unsettledTransactions)
    if (keyboardMarkup!=None):
        context.bot.editMessageText(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup = keyboardMarkup
        )
    else:
        context.bot.editMessageText(
            chat_id=chat_id,
            message_id=message_id,
            text='All debts settled! You have such responsible friends... Unlike me ):'
        )

def settleDebtForDebtor(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    userID = query.from_user.id
    text = query.message.text

    transactionID = query.data.replace('settledebtfordebtor', '', 1)
    try:
        updateTransactionAsSettledWithTransactionID(transactionID)
        updateOrderMessageAsSettledWhenTransactionSettled(transactionID)
    finally:
        unsettledTransactions = getUnsettledTransactionsForDebtor(userID)
        keyboardMarkup = formatTransactionsForDebtorKeyboardMarkup(unsettledTransactions)

        if (keyboardMarkup!=None):
            context.bot.editMessageText(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=keyboardMarkup
            )
        else:
            context.bot.editMessageText(
                chat_id=chat_id,
                message_id=message_id,
                text='All debts settled! How responsible of you...'
            )
    

def editMessageForSplitEvenly(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    userID = query.from_user.id
    text = query.message.text

    if not (userIsCreditorForMessage(message_id, chat_id, userID)):
        return
        
    debtorID = query.data.replace('splitevenlycallbackdata', '', 1)
    debtorUsername = getUsername(debtorID)
    debtorName = getFirstName(debtorID)
    entry = debtorName + ' (@' + debtorUsername + ')'
    
    if entry in text:
        text = text.replace('\n' + entry, '', 1)
    else:
        text = text + '\n' + entry
    
    context.bot.editMessageText(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=query.message.reply_markup,
    )

    
def debtorEvenlyPaid(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    username = query.from_user.username
    debtorID = query.from_user.id
    text = query.message.text
    debtorName = getFirstName(debtorID)
    entry = '%s (@%s)' % (debtorName, username)
    textList = text.split('\n')
    newTextList = []

    creditorID = getCreditorIDFromMessageAndGroupID(message_id, chat_id)

    if str(creditorID) == str(debtorID):
        return

    for item in textList:
        if entry in item:
            continue
        else:
            newTextList.append(item + '\n')

    textAfterRemove = ''.join(newTextList)

    orderID = getOrderIDFromMessageAndGroupID(message_id, chat_id)
    

    if textAfterRemove != text:
        markTransactionAsSettled(creditorID, debtorID, orderID)
        context.bot.editMessageText(
            chat_id=chat_id,
            message_id=message_id,
            text=textAfterRemove,
            reply_markup=query.message.reply_markup
        )
    
    return None

def debtorEvenlyUnpaid(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    username = query.from_user.username
    debtorID = query.from_user.id
    debtorName = getFirstName(debtorID)
    text = query.message.text
    creditorID = getCreditorIDFromMessageAndGroupID(message_id, chat_id)

    if str(creditorID) == str(debtorID):
        return
    entry = '%s (@%s)' % (debtorName, username)
    textList = text.split('\n')
    newTextList = []
    for item in textList:
        if entry in item:
            return
        else:
            newTextList.append(item + '\n')

    newTextList.append(entry + '\n')
    textAfterAdd = ''.join(newTextList)

    orderID = getOrderIDFromMessageAndGroupID(message_id, chat_id)
    creditorID = getCreditorIDFromMessageAndGroupID(message_id, chat_id)

    if textAfterAdd != text:
        markTransactionAsUnsettled(creditorID, debtorID, orderID)
        context.bot.editMessageText(
            chat_id=chat_id,
            message_id=message_id,
            text=textAfterAdd,
            reply_markup=query.message.reply_markup
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
        print('donkey')
        context.bot.editMessageText(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Your group is now registered!\n\nBegin splitting bills by sending a message starting with @OwePay_bot followed by the name of the bill. For example:\n\n@OwePay_bot Assorted Sausages\n\nDue to the nature of Telegram Bots, our bot will only be able to detect users if they have either sent a message in the group after I've been added or users added after me!",
        )



def splitEvenly(update, context):
    query = update.callback_query
    groupID = query.message.chat_id
    message_id = query.message.message_id
    userID = query.from_user.id
    text = query.message.text
    date = datetime.now(tz).replace(microsecond=0)

    if not (userIsCreditorForMessage(message_id, groupID, userID)):
        return
    
    totalAmount = getUserTempAmount(userID, groupID)
    listOfUsers = tuple(text.replace("People who have your cash money:\n", "", 1).replace("\n",",",text.count("\n")).split(','))
    numberOfUsers = len(listOfUsers)

    if numberOfUsers == 0:
        return
    
    listOfUsernames = []
    for user in listOfUsers:
        tempList = []
        tempList.append(user.split('@')[1])
        for tempItem in tempList:
            listOfUsernames.append(tempItem.split(')')[0])
    

    splitAmount = totalAmount / numberOfUsers
    orderID = getOrderIDFromUserIDAndGroupID(userID, groupID)
    orderName = getOrderNameFromOrderID(orderID)
    creditorUsername = getUsername(userID)
    creditorName = getFirstName(userID)
    
    listOfUserID = getUserIDListFromUsernameList(listOfUsernames)

    if len(listOfUserID) < 1:
        return
    
    setUserStateInactive(userID, groupID)
    resetUserTempAmount(userID, groupID)
    resetUserTempOrderID(userID, groupID)
    resetUserTempMessageID(userID, groupID)

    messageText = "Please return @%s $%s each for %s" % (creditorUsername, getFormattedAmountFromString(splitAmount), orderName)
    for username in listOfUsers:
        messageText = messageText + '\n' + username

    if "%s (@%s)" % (creditorName, creditorUsername) in messageText:
        messageText =  messageText.replace("\n%s (@%s)" % (creditorName, creditorUsername), "", 1)

    orderMessage = context.bot.editMessageText(
        chat_id=update.effective_chat.id,
        message_id=message_id,
        text=messageText,
        reply_markup=splitEvenlyFinalisedKeyboardMarkup(),
    )
    order = Order(orderID, groupID, orderName, splitAmount, userID, date)
    messageID = orderMessage.message_id
    addMessageIDToOrder(str(orderID), messageID)
    createTransactionBetweenSomeUsers(order, listOfUserID)


def splitDifferentAmounts(update, context, userID, groupID):
    textString = update.message.text
    textStringWithoutParagraphs = textString.split('\n')
    textListSeparated = []
    messageID = update.message.message_id
    itemList = []
    orderID = getOrderIDFromUserIDAndGroupID(userID, groupID)
    orderName = getOrderNameFromOrderID(orderID)
    for text in textStringWithoutParagraphs:
        tempText = text.split ('-')
        tempList = []
        for t in tempText:
            tempList.append(removeCrustFromString(t))
        textListSeparated.append(tempList)
    for item in textListSeparated:
        tempList = []
        if len(item) != 2 or not isValidAmount(item[1]):
            context.bot.send_message(
                chat_id=groupID,
                reply_to_message_id=messageID,
                text='Please send your order in a valid format!'
            )
            return
        tempList.append(item[0])
        if (isValidAmount(item[1])):
            tempList.append(getFormattedAmountFromString(item[1]))
        else:
            context.bot.send_message(
                chat_id=groupID,
                reply_to_message_id=messageID,
                text='%s is not a valid amount' % (item[1])
            )
        itemList.append(tempList)

    firstItem = itemList.pop(0)
    firstItemString = firstItem[0] + ' ($' + firstItem[1] + ')'
    itemListString = itemListToString(itemList)
    messageText = 'Current split for %s:\n\nItems left to split:%s\n\nPeople paying for %s:' % (orderName, itemListString, firstItemString)
    orderMessage = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messageText,
        reply_markup=splitUnevenlyKeyboardMarkup(groupID, False)
    )
    print(splitUnevenlyKeyboardMarkup(groupID, False))
    messageID = orderMessage.message_id
    addMessageIDToOrder(orderID, messageID)
    setUserStateInactive(userID, groupID)
    return orderMessage
    
def getTotalAmountFromMessage(update, context):
    chat_message=update.message.text
    value = int(''.join(filter(str.isdigit, chat_message)))
    total_amount = float(value/100)
    return total_amount


#############################
# when split among us is called this will update regisfter the userid and the
# amount of money
##############


def getOrderNameFromMessage(update):
    text = update.message.text
    return str(text.split('New Order: ')[1])

def messageContainsNewOrder(update, context):
    if "New Order:" in update.message.text:   
        orderName = getOrderNameFromMessage(update)
        user_id = update.message.from_user.id
        GroupID = update.message.chat_id
        updateUserStateNewOrder(user_id, GroupID)
        updateOrderIDToUserGroupRelational(user_id, GroupID, orderName)
        message = context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=
            "Please choose if you wish to split %s evenly or unevenly" % orderName,
            reply_markup=waitingForUserToChooseSplitKeyboardMarkup()
        )
        updateMessageIDToUserGroupRelational(user_id, GroupID, message.message_id)
        return message

def catchSplitEvenlyOrderFromUpdate(update):
    order_id = str(uuid1())
    user_id = update.message.from_user.id
    group_id = update.message.chat_id
    order_amount= update.message.text.replace('$', '', 1)
    date = datetime.now(tz).replace(microsecond=0)
    order_name = getOrderIDFromUserIDAndGroupID(user_id, group_id)
    addOrder((order_id, group_id, order_name, order_amount, user_id, date))
    return Order(order_id, group_id, order_name, order_amount, user_id, date)

def catchSplitUnevenlyOrder(user_id, group_id):
    order_id = str(uuid1())
    order_amount = 0
    date = datetime.now(tz).replace(microsecond=0)
    order_name = getOrderIDFromUserIDAndGroupID(user_id, group_id)
    addOrder((order_id, group_id, order_name, order_amount, user_id, date))
    return Order(order_id, group_id, order_name, order_amount, user_id, date)


def waitingForSomeNames(update, context, user_id, group_id):
    order = catchSplitEvenlyOrderFromUpdate(update)
    orderID = order.orderID
    orderAmount = order.orderAmount
    updateUserTempAmount(user_id, group_id, orderAmount)
    updateUserStateWaitingForSomeNames(user_id, group_id)
    updateOrderIDToUserGroupRelational(user_id, group_id, orderID)

    message = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='People who have your cash money:',
        reply_markup=splitEvenlyKeyboardMarkup(update.effective_chat.id)
    )
    messageID = message.message_id
    addMessageIDToOrder(orderID, messageID)
    return message

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
                text="You are now registered!\n\nAdd this bot to your telegram groups to split bills among your friends! Bills can be split by sending a message starting with @OwePay_bot followed by the name of the order after registering the bot in the group with the /start command. For example:\n\n@OwePay_bot Assorted Meats\n\nDue to the nature of Telegram Bots, our bot will only be able to detect users if they have either sent a message in the group after I've been added or users added after me!",
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
            text="You are now registered!\n\nAdd this bot to your telegram groups to split bills among your friends! Bills can be split by sending a message starting with @OwePay_bot followed by the name of the order after registering the bot in the group with the /start command. For example:\n\n@OwePay_bot Assorted Meats\n\nDue to the nature of Telegram Bots, our bot will only be able to detect users if they have either sent a message in the group after I've been added or users added after me!",
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
    return (update.message.via_bot!=None and str(update.message.via_bot.id) == str(BOT_ID))

# def echo(update: Update, _: CallbackContext) -> None:
def echo(update, context):
    """Echo the update for debugging purposes."""
    print(update)

def askUserToSendValidAmount(update, context):
    group_id = update.message.chat_id
    user_id = update.message.from_user.id
    text = update.message.text
    message = context.bot.send_message(
        chat_id=group_id,
        text="%s is not a valid amount.\n\nPlease key in a valid amount e.g $123, 123, 123.10 or /cancel to stop the creation of the order." % text
    )
    return message

def groupMemberScanner(update, context):
    """"Constantly monitors group chat to check if members are counted in the group or not"""
    group_id = update.message.chat_id
    message_id = update.message.message_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    firstname = update.message.from_user.first_name
    
    if len(update.message.new_chat_members) > 0:
        for newMember in update.message.new_chat_members:
            if newMember.is_bot:
                continue
            newUserID = newMember.id
            addUserToGroup(newUserID, group_id)
            if not userAlreadyAdded(newUserID):
                newUsername = newMember.username
                newFirstname = newMember.first_name
                user = (newUserID, newUsername, 0, newFirstname)
                addUser(user)
    
    if update.message.left_chat_member != None:
        print(update.message.left_chat_member.id)
        leftMember = update.message.left_chat_member
        leftMemberID = leftMember.id
        if userInGroup(leftMemberID, group_id):
            deleteUserFromGroup(leftMemberID, group_id)
        if not userAlreadyAdded(leftMemberID):
            leftUsername = leftMember.username
            leftFirstname = leftMember.first_name
            user = (leftMemberID, leftUsername, 0, leftFirstname)
            addUser(user)

    if not(userAlreadyAdded(user_id)):
        user = (user_id, username, 0, firstname)
        addUser(user)


    if not(userInGroup(user_id, group_id)):
        increaseGroupMemberCount(group_id)
        addUserToGroup(user_id, group_id)
    

    if not(groupAlreadyAdded(group_id)):
        return 'Group with id %s not added' % group_id
        
    if userStateSplitEvenly(user_id, group_id):
        text = update.message.text
        if isValidAmount(text):
            waitingForSomeNames(update, context, user_id, group_id)
            return "User %s has state 'splitevenly'" % user_id
        else:
            askUserToSendValidAmount(update, context)
            return "User %s sending invalid amount" % user_id

    if userStateSplitUnevenly(user_id, group_id):
        splitDifferentAmounts(update, context, user_id, group_id)
        return "User %s has state 'splitunevenly'" % user_id

    if viabot_check(update, context):
        bot = update.message.via_bot.id
        messageContainsNewOrder(update, context)
        return "Bot found %s" % bot



def main():
    """Start the bot."""
    updater = Updater(
        TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", startGroup, Filters.chat_type.groups))
    dp.add_handler(CommandHandler("start", startPrivate, Filters.chat_type.private))
    dp.add_handler(CommandHandler("whoowesme", getDebtors, Filters.chat_type.private))
    dp.add_handler(CommandHandler("whomeowes", getCreditors, Filters.chat_type.private))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("cancel", cancel, Filters.chat_type.groups))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(InlineQueryHandler(inline))
    #dp.add_handler(MessageHandler(Filters.chat_type.groups, echo))
    dp.add_handler(MessageHandler(Filters.chat_type.groups, groupMemberScanner))
    dp.add_handler(ConversationHandler(
        [
            CommandHandler("scanreceipt", scanReceiptPrivateMessage)
        ], 
        {
            "waitingonpicprivate": [CommandHandler("cancelreceipt", cancelReceipt), MessageHandler(Filters.chat_type.private, scanReceiptPrivatePicture)],

        }, 
        [
            CommandHandler("cancelreceipt", cancelReceipt)
        ],
        allow_reentry=True
    ))

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
