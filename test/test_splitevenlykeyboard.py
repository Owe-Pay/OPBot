import pytest
import os 

from flaky import flaky
from telegram import User, Message, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyMarkup, ReplyKeyboardMarkup, keyboardbutton, replymarkup
from telegram.ext import ExtBot

from ..owepaybot import splitEvenly, waitingForSomeNames 
from ..HELPME.bot_sql_integration import *
from ..HELPME.helperFunctions import *


@pytest.fixture(scope='class')
def split_evenly_inline_keyboard_markup():
    return splitEvenlyKeyboardMarkup(345)

@pytest.fixture(scope='class')
def testsplitevenlykeyboardmarkup():
    keyboardHolder = []
    buttonToFinalise = None
    users = ('456', '9871', '9872', '9873')
    count = 0
    firstnames = ('userfirstname', 'dummyuser1', 'dummyuser2', 'dummyuser3')
    usernames = ('userusername', 'dummyusername1', 'dummyusername2', 'dummyusername3')
    for user in users:
        firstname = firstnames[count]
        username = usernames[count]
        firstNameWithUsername = firstname + " (@" + username + ")"
        callback_data = 'splitevenlycallbackdata' + '%s' % user 
        keyboardHolder.append([InlineKeyboardButton(firstNameWithUsername, callback_data=callback_data)])
        count = count + 1
    addEveryone = InlineKeyboardButton("Add Everyone!", callback_data='splitevenlyaddeveryonecallbackdata')
    keyboardHolder.append([addEveryone])
    buttonToFinalise = InlineKeyboardButton("Create Order", callback_data='SplitEvenlyFinalise')
    keyboardHolder.append([buttonToFinalise])
    return InlineKeyboardMarkup(keyboardHolder)

class tempContext:
    class bot:
        def send_message(chat_id, text, reply_markup):
            return Message(1, datetime.now(), chat=Chat(chat_id, 'groupname'), text=text, reply_markup=reply_markup)



class TestSplitevenly:
    
    @flaky(3, 1)
    def test_splitevenly(self,split_evenly_inline_keyboard_markup,testsplitevenlykeyboardmarkup):
        
        massDelete("Users")
        massDelete("Orders")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

        assert addGroup((345, 'groupname')) == "Group groupname 345 inserted"
        assert addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"
        assert addUser((9871, 'dummyusername1', 0, 'dummyuser1')) == "User 9871 inserted"
        assert addUser((9872, 'dummyusername2', 0, 'dummyuser2')) == "User 9872 inserted"
        assert addUser((9873, 'dummyusername3', 0, 'dummyuser3')) == "User 9873 inserted"
        assert addUserToGroup(456, 345) == "User 456 added to Group 345"
        assert addUserToGroup(9871, 345) == "User 9871 added to Group 345"
        assert addUserToGroup(9872, 345) == "User 9872 added to Group 345"
        assert addUserToGroup(9873, 345) == "User 9873 added to Group 345"
        assert splitEvenlyKeyboardMarkup(345) == split_evenly_inline_keyboard_markup
        assert splitEvenlyKeyboardMarkup(345) == testsplitevenlykeyboardmarkup
        
        massDelete("Users")
        massDelete("Orders")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")