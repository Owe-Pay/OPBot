import logging
import os

from uuid import uuid4
from telegram.utils.helpers import escape_markdown
from telegram.ext import InlineQueryHandler, Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, MessageHandler
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Update

def inlineQueryHelper(update):
    """Helps to provide the display text for the inline query pop-up"""
    query = update.inline_query.query
    if query.replace('$','',1).isnumeric():
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