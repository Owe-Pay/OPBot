import pytest
import os

from flaky import flaky
from telegram import CallbackQuery, User, Message, Chat, Update, user
from ..owepaybot import button, groupDontRegister
from ..bot_sql_integration import *

@pytest.fixture(scope='function', params=['message', 'inline'])
def user_register_callback_query(bot):
    cbq = CallbackQuery(
        'userRegisterID',
        TestButton.from_user,
        TestButton.chat_instance,
        data='userRegister',
        bot=bot,
        message=TestButton.private_message,
        inline_message_id='userRegisterInlineMessageID'
    )

    cbq.message.bot = bot
    return cbq



@pytest.fixture(scope='function', params=['message', 'inline'])
def user_dont_register_callback_query(bot, request):
    cbq = CallbackQuery(
        'userDontRegisterID',
        TestButton.from_user,
        TestButton.chat_instance,
        data='userDontRegister',
        game_short_name=TestButton.game_short_name,
        bot=bot,
        message=TestButton.private_message,
        inline_message_id='userDontRegisterInlineMessageID'
    )
    return cbq

@pytest.fixture(scope='function', params=['message', 'inline'])
def group_register_callback_query(bot, request):
    cbq = CallbackQuery(
        'groupRegisterID',
        TestButton.from_user,
        TestButton.chat_instance,
        data='groupRegister',
        game_short_name=TestButton.game_short_name,
        bot=bot,
        message = TestButton.group_message,
        inline_message_id='groupRegisterInlineMessageID'
    )
    cbq.message.bot = bot
    return cbq


@pytest.fixture(scope='function', params=['message', 'inline'])
def group_dont_register_callback_query(bot, request):
    cbq = CallbackQuery(
        'groupDontRegisterID',
        TestButton.from_user,
        TestButton.chat_instance,
        data='groupDontRegister',
        game_short_name=TestButton.game_short_name,
        bot=bot,
        message=TestButton.group_message,
        inline_message_id = 'groupDontRegisterInlineMessageID'
    )
    cbq.message.bot = bot
    return cbq

class tempContext:
    class bot:
        def editMessageText(chat_id, message_id, text):
            None
    
class TestButton:
    
    from_user = User(1, 'test_user', False)
    chat_instance = 'chat_instance'
    private_message = Message(3, None, Chat(4321234, 'private', username='bot'), from_user=User(5, 'bot', False, username='bot'))
    group_message = Message(3, None, Chat(1234321, 'group', username='bot', title='bot_group'), from_user=User(5, 'bot', False, username='bot'))
    game_short_name = 'the_game'

    @flaky(3, 1)
    def test_user_register_callback_query(self, user_register_callback_query):
        choice = user_register_callback_query.data
        assert choice == 'userRegister'
        
        massDelete("Users") # Deleting all entries from Users Table
        assert button(Update(1, callback_query=user_register_callback_query), tempContext).data == 'userRegister'
        assert button(Update(1, callback_query=user_register_callback_query), tempContext).from_user == self.from_user
        assert button(Update(1, callback_query=user_register_callback_query), tempContext).chat_instance == self.chat_instance
        assert button(Update(1, callback_query=user_register_callback_query), tempContext).message == self.private_message
        assert button(Update(1, callback_query=user_register_callback_query), tempContext).inline_message_id == 'userRegisterInlineMessageID'        
        assert userAlreadyAdded('4321234')
        massDelete("Users") # Deleting all entries from Users Table

        assert user_register_callback_query.from_user == self.from_user
        assert user_register_callback_query.chat_instance == self.chat_instance
        assert user_register_callback_query.message == self.private_message
        assert user_register_callback_query.inline_message_id == 'userRegisterInlineMessageID'

    @flaky(3, 1)
    def test_user_dont_register_callback_query(self, user_dont_register_callback_query):
        choice = user_dont_register_callback_query.data
        assert choice == 'userDontRegister'

        massDelete('Users') # Deleting all entries from Users Table
        assert button(Update(1, callback_query=user_dont_register_callback_query), tempContext).data == 'userDontRegister'
        assert button(Update(1, callback_query=user_dont_register_callback_query), tempContext).from_user == self.from_user
        assert button(Update(1, callback_query=user_dont_register_callback_query), tempContext).chat_instance == self.chat_instance
        assert button(Update(1, callback_query=user_dont_register_callback_query), tempContext).message == self.private_message
        assert button(Update(1, callback_query=user_dont_register_callback_query), tempContext).inline_message_id == 'userDontRegisterInlineMessageID'        
        assert not userAlreadyAdded('4321234')

        assert user_dont_register_callback_query.from_user == self.from_user
        assert user_dont_register_callback_query.chat_instance == self.chat_instance
        assert user_dont_register_callback_query.message == self.private_message
        assert user_dont_register_callback_query.inline_message_id == 'userDontRegisterInlineMessageID'

    
    @flaky(3, 1)
    def test_group_register_callback_query(self, group_register_callback_query):
        choice = group_register_callback_query.data
        # assert choice == 'groupRegister'
        
        massDelete('TelegramGroups') # Deleting all entries from TelegramGroups Table
        assert button(Update(1, callback_query=group_register_callback_query), tempContext).data == 'groupRegister'
        assert button(Update(1, callback_query=group_register_callback_query), tempContext).from_user == self.from_user
        assert button(Update(1, callback_query=group_register_callback_query), tempContext).chat_instance == self.chat_instance
        assert button(Update(1, callback_query=group_register_callback_query), tempContext).message == self.group_message
        assert button(Update(1, callback_query=group_register_callback_query), tempContext).inline_message_id == 'groupRegisterInlineMessageID'
        assert groupAlreadyAdded('1234321')
        massDelete('TelegramGroups') # Deleting all entries from TelegramGroups Table

        assert group_register_callback_query.from_user == self.from_user
        assert group_register_callback_query.chat_instance == self.chat_instance
        assert group_register_callback_query.message == self.group_message
        assert group_register_callback_query.inline_message_id == 'groupRegisterInlineMessageID'

    
    @flaky(3, 1)
    def test_group_register_callback_query(self, group_dont_register_callback_query):
        choice = group_dont_register_callback_query.data
        assert choice == 'groupDontRegister'
        
        massDelete('TelegramGroups') # Deleting all entries from TelegramGroups Table
        assert button(Update(1, callback_query=group_dont_register_callback_query), tempContext).data == 'groupDontRegister'
        assert button(Update(1, callback_query=group_dont_register_callback_query), tempContext).from_user == self.from_user
        assert button(Update(1, callback_query=group_dont_register_callback_query), tempContext).chat_instance == self.chat_instance
        assert button(Update(1, callback_query=group_dont_register_callback_query), tempContext).message == self.group_message
        assert button(Update(1, callback_query=group_dont_register_callback_query), tempContext).inline_message_id == 'groupDontRegisterInlineMessageID'
        assert not groupAlreadyAdded('1234321')


        assert group_dont_register_callback_query.data == 'groupDontRegister'
        assert group_dont_register_callback_query.from_user == self.from_user
        assert group_dont_register_callback_query.chat_instance == self.chat_instance
        assert group_dont_register_callback_query.message == self.group_message
        assert group_dont_register_callback_query.inline_message_id == 'groupDontRegisterInlineMessageID'