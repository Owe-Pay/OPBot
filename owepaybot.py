import logging
# from datetime import *
from datetime import datetime, timedelta
import time
import os
import sys
import pytz
import re

from HELPME.bot_sql_integration import *
from HELPME.helperFunctions import *

from uuid import uuid4, uuid1
from telegram.utils.helpers import escape_markdown
from telegram.ext import InlineQueryHandler, Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, MessageHandler
from telegram import Bot, InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Update, message, replymarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

tz = pytz.timezone('Asia/Singapore')
now = datetime.now(tz) # the current time in your local timezone

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
    chat_id = update.message.chat_id
    username = update.message.chat.username
    firstname = update.message.chat.first_name
    user = (chat_id, username, 1, firstname)
    if not userAlreadyAdded(chat_id):
        addUser(user)

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
    keyboardMarkup = formatTransactionsKeyboardMarkup(unsettledTransactions)

    if len(unsettledTransactions) < 1:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='No one owes you money! What great friends you have!!!'
        )
        return

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='The baddies who have your cash money! >:(',
        reply_markup=keyboardMarkup
    )

    
    # user already added
    
def cancel(update, context):
    groupID = update.effective_chat.id
    userID = update.message.from_user.id
    messageID = update.message.message_id
    setUserStateInactive(userID, groupID)
    context.bot.send_message(
        chat_id=groupID,
        reply_to_message_id=messageID,
        text="I've been cancelled!"
    )

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
    
    if 'settledebtcallbackdata' in choice:
        settleDebt(update, context)
    
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
        
def debtorUnevenlyPaid(update, context):
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
    date = datetime.now(tz)

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
                if 'w/ SVC' in itemWithoutPara:
                    newItem = itemWithoutPara.replace('w/ GST and ', 'w/ ', 1)
                else:
                    newItem = itemWithoutPara.replace(' w/ GST:', ':', 1)
            tempSplitList = itemWithoutPara.split('-')
            tempSplitItem = tempSplitList[len(tempSplitList) - 1]
            if len(tempSplitList) > 0 and tempSplitList[0] != '':
                currentAmount = re.sub("[^\d.]+", "", str(tempSplitItem))
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
                    newItem = itemWithoutPara.replace(':', ' w/ GST:')
            tempSplitList = itemWithoutPara.split('-')
            tempSplitItem = tempSplitList[len(tempSplitList) - 1]
            if len(tempSplitList) > 0 and tempSplitList[0] != '':
                currentAmount = re.sub("[^\d.]+", "", str(tempSplitItem))
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
                    newItem = itemWithoutPara.replace(' w/ SVC', ':', 1)
            tempSplitList = itemWithoutPara.split('-')
            tempSplitItem = tempSplitList[len(tempSplitList) - 1]
            if len(tempSplitList) > 0 and tempSplitList[0] != '':
                currentAmount = re.sub("[^\d.]+", "", str(tempSplitItem))
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
                currentAmount = re.sub("[^\d.]+", "", str(tempSplitItem))
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

    amountBeforeSplit = float(re.sub("[^\d.]+", "", itemToRemove))
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
                currentAmount = float(re.sub("[^\d.]+", "", tempSplitUser))

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
        nextItem = itemList.pop(numOfItemsLeft - 1)
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
            currentAmount = float(re.sub("[^\d.]+", "", tempSplitUser))
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
    
    text = text + ''.join(listOfUsersWithNameAndUsername)
    context.bot.editMessageText(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
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
        entry = '\n' + firstName + ' (@' + username + ')'
        if entry not in splitByPara:
            listOfUsersWithNameAndUsername.append(entry)
    
    text = text + ''.join(listOfUsersWithNameAndUsername)
    context.bot.editMessageText(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=query.message.reply_markup
    )

    # text = query.message.text



def notifyUserFromPrivateMessage(update, context):
    query = update.callback_query
    transactionID = query.data.replace('notifydebtorcallbackdata', '', 1)

    lastNotifiedTime = getLastNotifiedTimeFromTransactionID(transactionID)
    currentTime = datetime.now(tz)
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

    context.bot.send_message(
        chat_id=debtorID,
        text='Hi %s! Your friend %s (@%s) from the group %s is asking you to return them their $%s for %s %s.' % (debtorName, creditorName, creditorUsername,groupName, amountOwed, orderName, formattedDate)
    )
    context.bot.send_message(
        chat_id=creditorID,
        text='%s (@%s) has been notified to return $%s for %s in %s' % (debtorName, debtorUsername, amountOwed, orderName, groupName)
    )

def settleDebt(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    userID = query.from_user.id
    text = query.message.text

    transactionID = query.data.replace('settledebtcallbackdata', '', 1)
    updateTransactionAsSettledWithTransactionID(transactionID)

    unsettledTransactions = getUnsettledTransactionsForCreditor(userID)
    keyboardMarkup = formatTransactionsKeyboardMarkup(unsettledTransactions)
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
    textAfterRemove = removeUsernameFromDebtMessage(username, text)
    orderID = getOrderIDFromMessageAndGroupID(message_id, chat_id)
    creditorID = getCreditorIDFromMessageAndGroupID(message_id, chat_id)

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
        context.bot.editMessageText(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Your group is now registered!",
        )



def splitEvenly(update, context):
    query = update.callback_query
    groupID = query.message.chat_id
    message_id = query.message.message_id
    userID = query.from_user.id
    text = query.message.text
    date = datetime.now(tz)

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
        tempList.append(getFormattedAmountFromString(item[1]))
        itemList.append(tempList)

    firstItem = itemList.pop(0)
    firstItemString = firstItem[0] + ' ($' + firstItem[1] + ')'
    itemListString = itemListToString(itemList)
    last = len(itemList) < 1
    messageText = 'Current split for %s:\n\nItems left to split:%s\n\nPeople paying for %s:' % (orderName, itemListString, firstItemString)
    orderMessage = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messageText,
        reply_markup=splitUnevenlyKeyboardMarkup(groupID, False)
    )
    messageID = orderMessage.message_id
    addMessageIDToOrder(orderID, messageID)
    setUserStateInactive(userID, groupID)
    
def getTotalAmountFromMessage(update, context):
    chat_message=update.message.text
    value = int(''.join(filter(str.isdigit, chat_message)))
    total_amount = float(value/100)
    return total_amount


#############################
# when split among us is called this will update regisfter the userid and the
# amount of money
##############

def messageContainsSplitUnevenly(update, context):
    if "Split unevenly:" in update.message.text:
        user_id = update.message.from_user.id
        GroupID = update.message.chat_id
        updateUserStateSplitUnevenlyWaitingForName(user_id, GroupID)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=
            "Hi! Please send the name of the order!",
    )

def messageContainsSplitEvenly(update, context):
    if "Split evenly:" in update.message.text:
        total_amount = getTotalAmountFromMessage(update,context)
        user_id = update.message.from_user.id
        GroupID = update.message.chat_id
        updateUserStateSplitEvenly(user_id, GroupID)
        updateUserTempAmount(user_id,GroupID, total_amount)
        print("updated temp amount and state")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=
            "Hi! Please send the name of the order!",
    )

def catchOrderFromUpdate(update):
    print("caught request")
    order_id = str(uuid1())
    user_id = update.message.from_user.id
    group_id = update.message.chat_id
    order_name = update.message.text
    order_amount= getUserTempAmount(user_id,group_id)
    date = datetime.now(tz)
    addOrder((order_id, group_id, order_name, order_amount, user_id, date))
    print("order added")
    return Order(order_id, group_id, order_name, order_amount, user_id, date)


def waitingForSomeNames(update, context, user_id, group_id):
    order = catchOrderFromUpdate(update)
    orderID = order.orderID

    updateUserStateWaitingForSomeNames(user_id, group_id)
    updateOrderIDToUserGroupRelational(user_id, group_id, orderID)

    message = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='People who have your cash money:',
        reply_markup=splitEvenlyKeyboardMarkup(update.effective_chat.id)
    )
    messageID = message.message_id
    addMessageIDToOrder(orderID, messageID)

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
    return (update.message.via_bot!=None and str(update.message.via_bot.id) == str(BOT_ID))

# def echo(update: Update, _: CallbackContext) -> None:
def echo(update, context):
    """Echo the update for debugging purposes."""
    print(update)

def splitUnevenlyOrderNameCatcher(update, context, userID, groupID):
    order = catchOrderFromUpdate(update)
    orderID = order.orderID
    messageID = update.message.message_id

    updateOrderIDToUserGroupRelational(userID, groupID, orderID)
    setOrderDifferentAmountsFromOrderID(orderID)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=messageID,
        text='Please send in the items in the following format:\nItem Name - Price\n\nFor example:\nChicken Rice - 5\nCurry Chicken - 5.50\nNasi Lemak - 4'
    )
    updateUserStateSplitUnevenly(userID, groupID)



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
        
    if userStateSplitEvenly(user_id, group_id):
        waitingForSomeNames(update, context, user_id, group_id)


    if userStateSplitUnevenly(user_id, group_id):
        splitDifferentAmounts(update, context, user_id, group_id)

    if userStateSplitUnevenlyWaitingForName(user_id, group_id):
        splitUnevenlyOrderNameCatcher(update, context, user_id, group_id)

    if viabot_check(update, context):
        messageContainsSplitEvenly(update, context)
        messageContainsSplitUnevenly(update, context)

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
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("cancel", cancel, Filters.chat_type.groups))
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
