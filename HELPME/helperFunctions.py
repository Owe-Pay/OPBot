from email.mime import text
from datetime import *
import pytz
import logging
import os
from tokenize import group

from uuid import uuid4
from telegram.utils.helpers import escape_markdown
from telegram.ext import InlineQueryHandler, Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, MessageHandler
from telegram import Chat, Message, Bot, InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Update, replymarkup

from .bot_sql_integration import *


TOKEN = os.environ['API_TOKEN']

tz = pytz.timezone('Asia/Singapore')
now = datetime.now(tz) # the current time in your local timezone

def inlineQueryHelper(update):
    """Helps to provide the display text for the inline query pop-up"""
    query =removeCrustFromString(update.inline_query.query)

    if len(query) > 44:
        return [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=query + " is too long for an order name.",
                input_message_content=InputTextMessageContent(
                    "Trying to create order with invalid name: " + query + "\n\nPlease key in a valid order name to start splitting!"
                ),
                thumb_url='https://res.cloudinary.com/jianoway/image/upload/b_rgb:ffffff/v1621962567/icons8-cross-mark-96_zrk1p9.png',
            ),
        ]

    if '\n' in query or 'New Order:' in query:
        return [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=query + " is not a valid order name.",
                input_message_content=InputTextMessageContent(
                    "Trying to create order with invalid name: " + query + "\n\nPlease key in a valid order name to start splitting!"
                ),
                thumb_url='https://res.cloudinary.com/jianoway/image/upload/b_rgb:ffffff/v1621962567/icons8-cross-mark-96_zrk1p9.png',
            ),
        ]

    return [
        InlineQueryResultArticle(
            id = str(uuid4()),
            title = "Create new order: " + query,
            input_message_content=InputTextMessageContent(
                "New Order: " + query
            ),
            thumb_url='https://res.cloudinary.com/jianoway/image/upload/b_rgb:ffffff/v1621962373/icons8-user-groups-100_nxolfi.png',
        )
    ]

def formatListOfUsernames(usernameList):
    str = ''
    for username in usernameList:
        str += '\n@' + username
    return str

def waitingForUserToChooseSplitKeyboardMarkup():
    keyboard = [
        [
            InlineKeyboardButton("Unevenly", callback_data="newordersplitunevenly"),
            InlineKeyboardButton("Evenly", callback_data="newordersplitevenly")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def splitEvenlyFinalisedKeyboardMarkup():
    keyboard = [
        [
            InlineKeyboardButton("I've paid!", callback_data='debtorEvenlyPaid'),
            InlineKeyboardButton("I've not paid!", callback_data='debtorEvenlyUnpaid')
        ],
        # [
        #     InlineKeyboardButton("Mark as settled", callback_data='markAsSettled')
        # ]
    ]
    return InlineKeyboardMarkup(keyboard)

def splitUnevenlyFinalisedKeyboardMarkup():
    keyboard = [
        [
            InlineKeyboardButton("I've paid!", callback_data='debtorUnevenlyPaid'),
            InlineKeyboardButton("I've not paid!", callback_data='debtorUnevenlyUnpaid')
        ],
        # [
        #     InlineKeyboardButton("Mark as settled", callback_data='markAsSettled')
        # ]
    ]
    return InlineKeyboardMarkup(keyboard)

def splitUnevenlyKeyboardMarkup(groupID, last):
    keyboardHolder = []
    buttonToFinalise = None

    if last:
        serviceChargeButton = InlineKeyboardButton("Service Charge?", callback_data="servicechargecallbackdata")
        GSTButton = InlineKeyboardButton("GST?", callback_data="goodservicetax")
        keyboardHolder.append([serviceChargeButton, GSTButton])
        buttonToFinalise = InlineKeyboardButton("Create Order", callback_data='splitunevenlyfinalise')
    else:
        users = getAllUsersFromGroup(groupID)
        for user in users:
            firstname = getFirstName(user)
            username = getUsername(user)
            firstNameWithUsername = firstname + " (@" + username + ")"
            callback_data = 'splitunevenlycallbackdata' + '%s' % user 
            keyboardHolder.append([InlineKeyboardButton(firstNameWithUsername, callback_data=callback_data)])
        addEveryone = InlineKeyboardButton("Add Everyone!", callback_data='splitunevenlyaddeveryonecallbackdata')
        
        keyboardHolder.append([addEveryone])
        buttonToFinalise = InlineKeyboardButton("Next Item", callback_data='splitunevenlynextitem')
    
    keyboardHolder.append([buttonToFinalise])
    return InlineKeyboardMarkup(keyboardHolder)


def splitEvenlyKeyboardMarkup(groupID):
    keyboardHolder = []

    users = getAllUsersFromGroup(groupID)

    for user in users:
        firstname = getFirstName(user)
        username = getUsername(user)
        firstNameWithUsername = firstname + " (@" + username + ")"
        callback_data = 'splitevenlycallbackdata' + '%s' % user
        keyboardHolder.append([InlineKeyboardButton(firstNameWithUsername, callback_data=callback_data)])

    addEveryone = InlineKeyboardButton("Add Everyone!", callback_data='splitevenlyaddeveryonecallbackdata')
    buttonToFinalise = InlineKeyboardButton("Create Order", callback_data='SplitEvenlyFinalise')
    keyboardHolder.append([addEveryone])
    keyboardHolder.append([buttonToFinalise])

    return InlineKeyboardMarkup(keyboardHolder)
        

def removeUUIDDashes(uuid):
    return "".join(str(uuid).split("-"))

def removeUsernameFromDebtMessage(username, text):
    usernameWithTag = '@' + str(username)
    text = text
    if usernameWithTag in text:
        text = text.replace('\n' + usernameWithTag, '', 1)
    return text

def addUsernameToDebtMessage(username, text):
    usernameWithTag = '@' + str(username)
    text = text
    if usernameWithTag not in text:
        text += '\n' + usernameWithTag
    return text

def takeSecond(element):
    return element[1]

def formatTransactionsForCreditorKeyboardMarkup(transactions):
    if len(transactions) < 1:
        return
    
    firstTransaction = transactions[0]
    currentOrderID = firstTransaction[1]
    date = getOrderDateFromOrderID(currentOrderID)
    formattedDate = date.strftime("%d %B %Y")
    currentOrderName = getOrderNameFromOrderID(currentOrderID)
    currentGroupID = getGroupIDFromOrder(currentOrderID)
    currentGroupName = getGroupNameFromGroupID(currentGroupID)
    keyboardHolder = []
    keyboardHolder.append([InlineKeyboardButton('Order: %s %s (%s)' % (currentOrderName, formattedDate, currentGroupName), callback_data='null')])

    for transaction in transactions:
        transactionID = transaction[0]
        transactionOrderID = transaction[1]
        if transactionOrderID != currentOrderID:
            currentOrderID = transactionOrderID
            currentGroupID = getGroupIDFromOrder(currentOrderID)
            currentGroupName = getGroupNameFromGroupID(currentGroupID)
            date = getOrderDateFromOrderID(currentOrderID)
            formattedDate = date.strftime("%d %B %Y")
            currentOrderName = getOrderNameFromOrderID(currentOrderID)
            keyboardHolder.append([InlineKeyboardButton('Order: %s %s (%s)' % (currentOrderName, formattedDate, currentGroupName), callback_data='null')])
        
        debtorID = transaction[2]
        amountOwed = getFormattedAmountFromString(transaction[3])
        debtorUsername = getUsername(debtorID)
        debtorName = getFirstName(debtorID)
        tempKeyboard = [
            InlineKeyboardButton('%s' % debtorName, callback_data='null'),
            InlineKeyboardButton('@%s' % debtorUsername, callback_data='null'),
            InlineKeyboardButton('$%s' % amountOwed, callback_data='null'),
            InlineKeyboardButton('Notify', callback_data="notifydebtorcallbackdata%s" % transactionID),
            InlineKeyboardButton('Settle', callback_data="settledebtforcreditor%s" % transactionID)
        ]
        keyboardHolder.append(tempKeyboard)
    
    return InlineKeyboardMarkup(keyboardHolder)

def formatTransactionsForDebtorKeyboardMarkup(transactions):
    
    if len(transactions) < 1:
        return
    
    firstTransaction = transactions[0]
    currentOrderID = firstTransaction[1]
    date = getOrderDateFromOrderID(currentOrderID)
    formattedDate = date.strftime("%d %B %Y")
    currentOrderName = getOrderNameFromOrderID(currentOrderID)
    currentGroupID = getGroupIDFromOrder(currentOrderID)
    currentGroupName = getGroupNameFromGroupID(currentGroupID)
    keyboardHolder = []
    keyboardHolder.append([InlineKeyboardButton('Order: %s %s (%s)' % (currentOrderName, formattedDate, currentGroupName), callback_data='null')])
    for transaction in transactions:
        transactionID = transaction[0]
        transactionOrderID = transaction[1]
        if transactionOrderID != currentOrderID:
            currentOrderID = transactionOrderID
            currentGroupID = getGroupIDFromOrder(currentOrderID)
            currentGroupName = getGroupNameFromGroupID(currentGroupID)
            date = getOrderDateFromOrderID(currentOrderID)
            formattedDate = date.strftime("%d %B %Y")
            currentOrderName = getOrderNameFromOrderID(currentOrderID)
            keyboardHolder.append([InlineKeyboardButton('Order: %s %s (%s)' % (currentOrderName, formattedDate, currentGroupName), callback_data='null')])
        
        creditorID = transaction[2]
        amountOwed = getFormattedAmountFromString(transaction[3])
        creditorUsername = getUsername(creditorID)
        creditorName = getFirstName(creditorID)
        tempKeyboard = [
            InlineKeyboardButton('%s' % creditorName, callback_data='null'),
            InlineKeyboardButton('@%s' % creditorUsername, callback_data='null'),
            InlineKeyboardButton('$%s' % amountOwed, callback_data='null'),
            InlineKeyboardButton('Settle', callback_data="settledebtfordebtorcallbackdata%s" % transactionID)
        ]
        keyboardHolder.append(tempKeyboard)
    
    return InlineKeyboardMarkup(keyboardHolder)

def removeCrustFromString(str):
    return str.rstrip().lstrip()

def isValidAmount(amt):
    temp = amt.replace('.', '', 1)
    if len(temp) < 1:
        return False
    else:
        if temp[0] == '$':
            temp = temp.replace('$', '', 1)
    return temp.isdigit()

def getFormattedAmountFromString(amt):
    tempAmt = float(float(amt) + float(0.005))
    strAmt = str(tempAmt)
    decimalPosition = strAmt.find('.')
    temp = list(strAmt)
    strToReturn = ''
    if float(strAmt) == 0:
        return '0.00'
    if decimalPosition == -1:
        for digit in temp:
            if digit == '0' and strToReturn == '':
                continue
            else:
                strToReturn = strToReturn + digit
        strToReturn = strToReturn + '.00'
    else:
        counter = -1
        for digit in temp:
            counter += 1
            if counter > decimalPosition + 2:
                return strToReturn
            if digit == '0' and strToReturn == '' and counter != decimalPosition - 1:
                continue
            else:
                strToReturn = strToReturn + digit
        if counter == decimalPosition + 1:
            strToReturn = strToReturn + '0'
        if strToReturn.endswith('.'):
            strToReturn = strToReturn + '00'
    return strToReturn

def itemListToString(itemList):
    listStr = ''
    for item in itemList:
        print(item)
        listStr += '\n' + item[0] + ' ('
        listStr += '$' + item[1] + ')'
    return listStr    

# removeUsernameFromSplitAllEvenlyDebtMessage('testuser1', '6a39016c-cd25-11eb-955c-acde48001122')
class Order:
    def __init__(self, orderID, groupID, orderName, orderAmount, creditorID, date):
        self.orderID = orderID
        self.groupID = groupID
        self.orderName = orderName
        self.orderAmount = orderAmount
        self.creditorID = creditorID
        self.date = date

class UsersAndSplitAmount:
    def __init__(self, users, splitAmount):
        self.users = users
        self.splitAmount = splitAmount
        
class Transaction:
    def __init__(self, transaction_id, orderID, splitAmount, creditorID, userID):
        self.transaction_id = transaction_id
        self.orderID = orderID,
        self.splitAmount = splitAmount
        self.creditorID = creditorID
        self.userID = userID

