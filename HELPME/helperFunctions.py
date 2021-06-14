from email.mime import text
import logging
import os
from tokenize import group

from .bot_sql_integration import *
from uuid import uuid4
from telegram.utils.helpers import escape_markdown
from telegram.ext import InlineQueryHandler, Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, MessageHandler
from telegram import Chat, Message, Bot, InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Update, replymarkup

TOKEN = os.environ['API_TOKEN']

def inlineQueryHelper(update):
    """Helps to provide the display text for the inline query pop-up"""
    query = update.inline_query.query
    if query.replace('$','',1).isnumeric():
        query = query.replace('$','',1)
        return [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Split $" + str(query) + ".00 among everyone",
                input_message_content=InputTextMessageContent("Split among everyone evenly: $" + query + ".00"),
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
                input_message_content=InputTextMessageContent("Split among everyone evenly: $" + formatted_query),
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

def formatListOfUsernames(usernameList):
    str = ''
    for username in usernameList:
        str += '\n@' + username
    return str

def splitAllEvenlyKeyboardMarkup():
    keyboard = [
        [
            InlineKeyboardButton("I've paid!", callback_data='debtorPaid'),
            InlineKeyboardButton("I've not paid!", callback_data='debtorUnpaid')
        ],
        [
            InlineKeyboardButton("Mark as settled", callback_data='markAsSettled')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

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

# removeUsernameFromSplitAllEvenlyDebtMessage('testuser1', '6a39016c-cd25-11eb-955c-acde48001122')
