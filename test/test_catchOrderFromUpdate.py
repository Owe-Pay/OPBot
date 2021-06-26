import pytest
from flaky import flaky
import datetime
from datetime import *

from telegram import Update, User, Message, Chat
from ..owepaybot import catchOrderFromUpdate, groupMemberScanner
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

class TestCatchOrderFromUpdate:

    @flaky(3, 1)
    def test_catchOrderFromUpdate(self, orderUpdate):
        massDelete("Users")
        massDelete("Orders")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

        assert addGroup((345, 'groupname')) == "Group groupname 345 inserted"
        assert addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"
        assert addUserToGroup(456, 345) == "User 456 added to Group 345"
        assert updateUserTempAmount('456', '345', '123') == "User 456 in Group 345 has the temporary amount 123"
        order = catchOrderFromUpdate(orderUpdate)
        orderID = order.orderID
        assert order.creditorID == 456
        assert order.date.replace(tzinfo=None) == getOrderDateFromOrderID(orderID).replace(tzinfo=None)
        assert order.groupID == 345
        assert order.orderName == "testOrderName"
        assert order.orderAmount == 123

        massDelete("Users")
        massDelete("Orders")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")
        

