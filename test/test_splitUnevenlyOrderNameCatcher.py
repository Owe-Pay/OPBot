import pytest
from flaky import flaky
import datetime
from datetime import *

from telegram import Update, User, Message, Chat
from ..owepaybot import catchOrderFromUpdate, groupMemberScanner, splitUnevenlyOrderNameCatcher, waitingForSomeNames
from ..HELPME.bot_sql_integration import *
from ..HELPME.helperFunctions import *

@pytest.fixture(scope='class')
def orderUpdate():
    return Update(
        123, 
        Message(
            234, 
            text='testOrderName', 
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
            ),
        )

class tempContext:
    class bot:
        def send_message(chat_id, reply_to_message_id, text):
            return Message(1, datetime.now(), chat=Chat(chat_id, 'groupname'), text=text, reply_to_message_id=reply_to_message_id)

class TestSplitUnevenlyOrderNameCatcher:

    @flaky(3, 1)
    def test_splitUnevenlyOrderNameCatcher(self, orderUpdate):
        massDelete("Users")
        massDelete("Orders")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

        assert addGroup((345, 'groupname')) == "Group groupname 345 inserted"
        assert addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"
        assert addUserToGroup(456, 345) == "User 456 added to Group 345"
        assert updateUserTempAmount('456', '345', '123') == "User 456 in Group 345 has the temporary amount 123"
        assert isinstance(splitUnevenlyOrderNameCatcher(orderUpdate, tempContext, 456, 345), Message)
        assert splitUnevenlyOrderNameCatcher(orderUpdate, tempContext, 456, 345).chat_id == 345
        assert splitUnevenlyOrderNameCatcher(orderUpdate, tempContext, 456, 345).text ==  "Please send in the items in the following format:\nItem Name - Price\n\nFor example:\nChicken Rice - 5\nCurry Chicken - 5.50\nNasi Lemak - 4"

        massDelete("Users")
        massDelete("Orders")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")