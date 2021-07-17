import pytest
from flaky import flaky
import datetime
from datetime import *

from telegram import Update, User, Message, Chat, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.callbackquery import CallbackQuery
from ..owepaybot import newOrderSplitEvenly
from ..HELPME.bot_sql_integration import *
from ..HELPME.helperFunctions import *

@pytest.fixture(scope='class')
def orderUpdate():
    return Update(
        update_id= 123,
        callback_query=CallbackQuery(
            id='123', 
            message=Message(
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
            chat_instance='12345',
            from_user=User(
                        456, 
                        'userfirstname', 
                        False,
                        username='userusername'
                    )
        )
    )

class tempContext:
    class bot:
        def editMessageText(chat_id, message_id, text):
            return Message(message_id, datetime.now(), chat=Chat(chat_id, 'groupname'), text=text)


class TestNewOrderSplitEvenly:

    @flaky(3, 1)
    def test_newOrderSplitEvenly(self, orderUpdate):
        
        massDelete("Users")
        massDelete("Orders")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

        assert addGroup((345, 'groupname')) == "Group groupname 345 inserted"
        assert addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"
        assert addUserToGroup(456, 345) == "User 456 added to Group 345"
        assert updateUserStateNewOrder(456, 345) == "User 456 in Group 345 has state 'neworder'"
        assert updateMessageIDToUserGroupRelational(456, 345, 234) == "User 456 in Group 345 has MessageID 234"
        message = newOrderSplitEvenly(orderUpdate, tempContext)
        assert isinstance(message, Message)
        assert userStateSplitEvenly(456, 345) == True

        assert message.chat_id == 345
        assert message.message_id == 234
        assert message.text == "Please send in the amount to split!"

        massDelete("Users")
        massDelete("Orders")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")
