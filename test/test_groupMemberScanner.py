import os
import pytest
from flaky import flaky

from telegram import Update, User, Message, Chat
from ..owepaybot import groupMemberScanner
from ..HELPME.bot_sql_integration import *

@pytest.fixture(scope='class')
def notAddedUpdate():
    return Update(1, TestGroupMemebrScanner.group_message)

class tempContext:
    class bot:
        class send_message:
            def __init__(self, chat_id, **kwargs):
                self.message_id=chat_id



class TestGroupMemebrScanner:

    from_user = User(1,'testUser', False)
    chat_instance = 'chat_instance'
    private_message = Message(3, None, Chat(4321234, 'private', username='test,bot', first_name='botname'), from_user=User(5, 'bot', False, username='bota'))
    group_message = Message(3, None, text='123', chat=Chat(1234321, 'group', username='test,bot', first_name='botname', title='bot_group'), from_user=User(11223344, 'bot', False, username='bota'))

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
        assert groupMemberScanner(notAddedUpdate, tempContext) == "User 11223344 has state 'splitevenly'"
        
        
        massDelete("UserGroupRelational")
        massDelete("TelegramGroups")
        massDelete("Users")
        massDelete("Orders")


