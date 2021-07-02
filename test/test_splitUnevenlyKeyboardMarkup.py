import pytest
from flaky import flaky
import datetime
from datetime import *

from telegram import Update, User, Message, Chat, InlineKeyboardMarkup, InlineKeyboardButton
from ..HELPME.bot_sql_integration import *
from ..HELPME.helperFunctions import *



@pytest.fixture(scope='class')
def splitUnevenlyReplyMarkupForTestManual():
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
        callback_data = 'splitunevenlycallbackdata' + '%s' % user 
        keyboardHolder.append([InlineKeyboardButton(firstNameWithUsername, callback_data=callback_data)])
        count = count + 1
    addEveryone = InlineKeyboardButton("Add Everyone!", callback_data='splitunevenlyaddeveryonecallbackdata')
    keyboardHolder.append([addEveryone])
    buttonToFinalise = InlineKeyboardButton("Next Item", callback_data='splitunevenlynextitem')
    keyboardHolder.append([buttonToFinalise])
    return InlineKeyboardMarkup(keyboardHolder)


class TestSplitUnevenly:
    
    @flaky(3, 1)
    def test_splitUnevenly(self, splitUnevenlyReplyMarkupForTestManual):
        
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
        assert splitUnevenlyKeyboardMarkup(345,False) == splitUnevenlyReplyMarkupForTestManual
        
        massDelete("Users")
        massDelete("Orders")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")