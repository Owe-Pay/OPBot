import pytest
from flaky import flaky
import datetime
from datetime import *

from telegram import Update, User, Message, Chat, InlineKeyboardMarkup, InlineKeyboardButton
from ..HELPME.helperFunctions import Order
from ..owepaybot import catchSplitEvenlyOrderFromUpdate
from ..HELPME.bot_sql_integration import *
from ..HELPME.helperFunctions import *

@pytest.fixture(scope='class')
def orderUpdate():
    return Update(
        123, 
        Message(
            234, 
            text='1234', 
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

class TestCatchSplitEvenlyOrderFromUpdate:

    @flaky(3, 1)
    def test_catchSplitEvenlyOrderFromUpdate(self, orderUpdate):
        massDelete("Orders")
        massDelete("TelegramGroups")
        massDelete("Users")
        massDelete("UserGroupRelational")
        assert addGroup((345, 'groupname')) == "Group groupname 345 inserted"
        assert addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"
        assert addUserToGroup(456, 345) == "User 456 added to Group 345"
        assert updateOrderIDToUserGroupRelational(456, 345, 'tempOrderName') == "User 456 in Group 345 has OrderID tempOrderName"
        assert isinstance(catchSplitEvenlyOrderFromUpdate(orderUpdate), Order)
        assert catchSplitEvenlyOrderFromUpdate(orderUpdate).groupID == 345
        assert catchSplitEvenlyOrderFromUpdate(orderUpdate).orderName == 'tempOrderName'
        assert catchSplitEvenlyOrderFromUpdate(orderUpdate).orderAmount == '1234'
        assert catchSplitEvenlyOrderFromUpdate(orderUpdate).creditorID == 456

        massDelete("Orders")
        massDelete("TelegramGroups")
        massDelete("Users")
        massDelete("UserGroupRelational")