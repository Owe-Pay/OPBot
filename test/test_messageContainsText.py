import pytest
from flaky import flaky
import datetime
from datetime import *

from telegram import Update, User, Message, Chat, InlineKeyboardMarkup, InlineKeyboardButton
from ..owepaybot import messageContainsSplitEvenly, messageContainsSplitUnevenly
from ..HELPME.bot_sql_integration import *
from ..HELPME.helperFunctions import *

@pytest.fixture(scope='class')
def containsSplitUnevenlyUpdate():
    return Update(
        123, 
        Message(
            234, 
            text='Split unevenly: $12.00', 
            chat=Chat(
                345, 
                'groupname'
                ),
            from_user=User(
                456, 
                'userfirstname', 
                False,
                username='userusername'
                ),
            date=datetime.now()
        )
    )

@pytest.fixture(scope='class')
def containsSplitEvenlyUpdate():
    return Update(
        125, 
        Message(
            236, 
            text='Split evenly: $10.00', 
            chat=Chat(
                987, 
                'groupname'
                ),
            from_user=User(
                456, 
                'userfirstname', 
                False,
                username='userusername'
                ),
            date=datetime.now()
        )
    )
class tempContext:
    class bot:
        def send_message(chat_id, text):
            return Message(1, datetime.now(), chat=Chat(chat_id, 'groupname'), text=text)

class TestMessageContainsText:

    def test_messageContainsSplitEvenly(self, containsSplitEvenlyUpdate):
        massDelete("Users")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

        assert addGroup((987, 'groupname')) == "Group groupname 987 inserted"
        assert addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"
        assert addUserToGroup(456, 987) == "User 456 added to Group 987"

        assert isinstance(messageContainsSplitEvenly(containsSplitEvenlyUpdate, tempContext), Message)
        assert messageContainsSplitEvenly(containsSplitEvenlyUpdate, tempContext).chat_id == 987
        assert messageContainsSplitEvenly(containsSplitEvenlyUpdate, tempContext).text == "Hi! Please send the name of the order!"
        assert getUserStateFromUserIDAndGroupID(456, 987) == 'splitevenly'
        assert getUserTempAmount(456, 987) == 10

        massDelete("Users")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

    def test_messageContainsSplitUnevenly(self, containsSplitUnevenlyUpdate):
        massDelete("Users")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

        assert addGroup((345, 'groupname')) == "Group groupname 345 inserted"
        assert addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"
        assert addUserToGroup(456, 345) == "User 456 added to Group 345"

        assert isinstance(messageContainsSplitUnevenly(containsSplitUnevenlyUpdate, tempContext), Message)
        assert messageContainsSplitUnevenly(containsSplitUnevenlyUpdate, tempContext).chat_id == 345
        assert messageContainsSplitUnevenly(containsSplitUnevenlyUpdate, tempContext).text == "Hi! Please send the name of the order!"
        assert getUserStateFromUserIDAndGroupID(456, 345) == 'splitunevenlywaitingname'

        massDelete("Users")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

