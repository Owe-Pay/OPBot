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
        None

class TestGroupMemebrScanner:

    from_user = User(1,'testUser', False)
    chat_instance = 'chat_instance'
    private_message = Message(3, None, Chat(4321234, 'private', username='test,bot', first_name='botname'), from_user=User(5, 'bot', False, username='bota'))
    group_message = Message(3, None, Chat(1234321, 'group', username='test,bot', first_name='botname', title='bot_group'), from_user=User(5, 'bot', False, username='bota'))

    @flaky(3, 1)
    def test_groupNotAdded(self, notAddedUpdate):
        massDelete("TelegramGroups") # Clear out the Telegram Groups table
        assert groupMemberScanner(notAddedUpdate, tempContext) == 'Group with id 1234321 not added'
    
    @flaky(3, 1)
    def test_userNotAdded(self, notAddedUpdate):
        massDelete("TelegramGroups")
        assert addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'
        
        massDelete("Users") 
        groupMemberScanner(notAddedUpdate, tempContext)
        assert userAlreadyAdded(5) == True
