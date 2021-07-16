import os
import pytest
from flaky import flaky
import datetime
from datetime import *

from telegram import Update, User, Message, Chat
from ..owepaybot import groupMemberScanner
from ..HELPME.bot_sql_integration import *

BOT_ID = os.environ['BOT_ID']

@pytest.fixture(scope='class')
def notAddedUpdate():
    return Update(1, TestGroupMemberScanner.group_message)

@pytest.fixture(scope='class')
def viaBotUpdate():
    return Update(1, TestGroupMemberScanner.bot_message)

class tempContext:
    class bot:
        class send_message:
            def __init__(self, chat_id, **kwargs):
                self.message_id=chat_id



class TestGroupMemberScanner:

    from_user = User(1,'testUser', False)
    chat_instance = 'chat_instance'
    private_message = Message(3, None, Chat(4321234, 'private', username='test,bot', first_name='botname'), from_user=User(5, 'bot', False, username='bota'))
    group_message = Message(3, None, text='123', chat=Chat(1234321, 'group', username='test,bot', first_name='botname', title='bot_group'), from_user=User(11223344, 'bot', False, username='bota'))
    bot_message = Message(3, None, text='ok-123\nkk-1234\niok - 5\n', chat=Chat(1234321, 'group', username='test,bot', first_name='botname', title='bot_group'), from_user=User(11223344, 'bot', False, username='bota'), via_bot=User(BOT_ID, 'bot', True))

    @flaky(3, 1)
    def test_groupNotAdded(self, notAddedUpdate):
        massDelete("Users") 
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")
        massDelete("TelegramGroups") # Clear out the Telegram Groups table
        assert groupMemberScanner(notAddedUpdate, tempContext) == 'Group with id 1234321 not added' # Group has yet to be registered in the TelegramGroups table
        massDelete("TelegramGroups")
        massDelete("Users") 
        massDelete("UserGroupRelational")

    @flaky(3, 1)
    def test_userNotAdded(self, notAddedUpdate):
        massDelete("TelegramGroups")
        assert addGroup(('1234321', 'group')) == 'Group group 1234321 inserted' # Group has been added to the MySQL
        
        massDelete("Users") 
        groupMemberScanner(notAddedUpdate, tempContext)
        assert userAlreadyAdded(11223344) == True # User is added in the Users table
        massDelete("Users") 
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

    @flaky(3, 1)
    def test_userNotInGroup(self, notAddedUpdate):
        massDelete("UserGroupRelational")
        assert addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'
        groupMemberScanner(notAddedUpdate, tempContext)
        assert userInGroup('11223344', '1234321') == True  # User and Group are related in the UserGroupRelational table
        massDelete("Users")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

    @flaky(3, 1)  
    def test_userStateSplitEvenly(self, notAddedUpdate):
        massDelete("UserGroupRelational")
        assert addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'
        groupMemberScanner(notAddedUpdate, tempContext) # Initial
        assert updateUserStateSplitEvenly('11223344', '1234321') == "User 11223344 in Group 1234321 has state 'splitevenly'"
        assert updateUserTempAmount('11223344', '1234321', '123') == "User 11223344 in Group 1234321 has the temporary amount 123"
        assert addOrder(('temporderid123', '345', 'testOrderName', 123, '345', datetime.now(tz).replace(microsecond=0))) == "Order temporderid123 has been added"
        assert updateOrderIDToUserGroupRelational(11223344, 1234321, 'temporderid123') == "User 11223344 in Group 1234321 has OrderID temporderid123"
        assert groupMemberScanner(notAddedUpdate, tempContext) == "User 11223344 has state 'splitevenly'"
        massDelete("UserGroupRelational")
        massDelete("TelegramGroups")
        massDelete("Users")
        massDelete("Orders")

    @flaky(3, 1)
    def test_userStateSplitUnevenly(self, notAddedUpdate):
        massDelete("UserGroupRelational")
        massDelete("TelegramGroups")
        assert addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'
        groupMemberScanner(notAddedUpdate, tempContext) # Initial
        assert updateUserStateSplitUnevenly('11223344', '1234321') == "User 11223344 in Group 1234321 has state 'splitunevenly'"
        assert addOrder(('4321', '1234321', 'ordertestname', '123', '11223344', datetime.now())) == "Order 4321 has been added"
        assert updateUserTempAmount('11223344', '1234321', '123') == "User 11223344 in Group 1234321 has the temporary amount 123"
        assert updateOrderIDToUserGroupRelational('11223344', '1234321', '4321') == "User 11223344 in Group 1234321 has OrderID 4321"
        assert groupMemberScanner(notAddedUpdate, tempContext) == "User 11223344 has state 'splitunevenly'"        
        massDelete("UserGroupRelational")
        massDelete("TelegramGroups")
        massDelete("Users")
        massDelete("Orders")
    
    @flaky(3, 1)
    def test_viabotCheck(self, viaBotUpdate):
        massDelete("UserGroupRelational")
        assert addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'
        assert groupMemberScanner(viaBotUpdate, tempContext) == "Bot found %s" % BOT_ID # Initial
        massDelete("UserGroupRelational")
        massDelete("TelegramGroups")
        massDelete("Users")


