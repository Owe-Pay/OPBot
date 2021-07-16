import pytest
from flaky import flaky
import datetime
from datetime import *

from telegram import Update, User, Message, Chat, InlineKeyboardMarkup, InlineKeyboardButton
from ..owepaybot import messageContainsNewOrder
from ..HELPME.bot_sql_integration import *
from ..HELPME.helperFunctions import *

@pytest.fixture(scope='class')
def containsSplitNewOrderUpdate():
    return Update(
        123, 
        Message(
            234, 
            text='New Order: testOrderName', 
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
        def send_message(chat_id, text, reply_markup):
            return Message(1, datetime.now(), chat=Chat(chat_id, 'groupname'), text=text, reply_markup=reply_markup)

class TestMessageContainsText:

    def test_messageContainsNewOrder(self, containsSplitNewOrderUpdate):
        massDelete("Users")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

        assert addGroup((987, 'groupname')) == "Group groupname 987 inserted"
        assert addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"
        assert addUserToGroup(456, 987) == "User 456 added to Group 987"

        assert isinstance(messageContainsNewOrder(containsSplitNewOrderUpdate, tempContext), Message)
        assert messageContainsNewOrder(containsSplitNewOrderUpdate, tempContext).chat_id == 987
        assert messageContainsNewOrder(containsSplitNewOrderUpdate, tempContext).text == "Please choose if you wish to split testOrderName evenly or unevenly"
        assert getUserStateFromUserIDAndGroupID(456, 987) == 'neworder'

        massDelete("Users")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")
