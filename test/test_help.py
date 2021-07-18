import pytest
import os

from flaky import flaky
from telegram.ext import ExtBot
from telegram.error import BadRequest
# from telegram.update import Updsate
from telegram import Update, Message, Chat, User
from ..owepaybot import help

# Placeholder COMPROMISED PK
PRIVATE_KEY = b"-----BEGIN RSA PRIVATE KEY-----\r\nMIIEowIBAAKCAQEA0AvEbNaOnfIL3GjB8VI4M5IaWe+GcK8eSPHkLkXREIsaddum\r\nwPBm/+w8lFYdnY+O06OEJrsaDtwGdU//8cbGJ/H/9cJH3dh0tNbfszP7nTrQD+88\r\nydlcYHzClaG8G+oTe9uEZSVdDXj5IUqR0y6rDXXb9tC9l+oSz+ShYg6+C4grAb3E\r\nSTv5khZ9Zsi/JEPWStqNdpoNuRh7qEYc3t4B/a5BH7bsQENyJSc8AWrfv+drPAEe\r\njQ8xm1ygzWvJp8yZPwOIYuL+obtANcoVT2G2150Wy6qLC0bD88Bm40GqLbSazueC\r\nRHZRug0B9rMUKvKc4FhG4AlNzBCaKgIcCWEqKwIDAQABAoIBACcIjin9d3Sa3S7V\r\nWM32JyVF3DvTfN3XfU8iUzV7U+ZOswA53eeFM04A/Ly4C4ZsUNfUbg72O8Vd8rg/\r\n8j1ilfsYpHVvphwxaHQlfIMa1bKCPlc/A6C7b2GLBtccKTbzjARJA2YWxIaqk9Nz\r\nMjj1IJK98i80qt29xRnMQ5sqOO3gn2SxTErvNchtBiwOH8NirqERXig8VCY6fr3n\r\nz7ZImPU3G/4qpD0+9ULrt9x/VkjqVvNdK1l7CyAuve3D7ha3jPMfVHFtVH5gqbyp\r\nKotyIHAyD+Ex3FQ1JV+H7DkP0cPctQiss7OiO9Zd9C1G2OrfQz9el7ewAPqOmZtC\r\nKjB3hUECgYEA/4MfKa1cvaCqzd3yUprp1JhvssVkhM1HyucIxB5xmBcVLX2/Kdhn\r\nhiDApZXARK0O9IRpFF6QVeMEX7TzFwB6dfkyIePsGxputA5SPbtBlHOvjZa8omMl\r\nEYfNa8x/mJkvSEpzvkWPascuHJWv1cEypqphu/70DxubWB5UKo/8o6cCgYEA0HFy\r\ncgwPMB//nltHGrmaQZPFT7/Qgl9ErZT3G9S8teWY4o4CXnkdU75tBoKAaJnpSfX3\r\nq8VuRerF45AFhqCKhlG4l51oW7TUH50qE3GM+4ivaH5YZB3biwQ9Wqw+QyNLAh/Q\r\nnS4/Wwb8qC9QuyEgcCju5lsCaPEXZiZqtPVxZd0CgYEAshBG31yZjO0zG1TZUwfy\r\nfN3euc8mRgZpSdXIHiS5NSyg7Zr8ZcUSID8jAkJiQ3n3OiAsuq1MGQ6kNa582kLT\r\nFPQdI9Ea8ahyDbkNR0gAY9xbM2kg/Gnro1PorH9PTKE0ekSodKk1UUyNrg4DBAwn\r\nqE6E3ebHXt/2WmqIbUD653ECgYBQCC8EAQNX3AFegPd1GGxU33Lz4tchJ4kMCNU0\r\nN2NZh9VCr3nTYjdTbxsXU8YP44CCKFG2/zAO4kymyiaFAWEOn5P7irGF/JExrjt4\r\nibGy5lFLEq/HiPtBjhgsl1O0nXlwUFzd7OLghXc+8CPUJaz5w42unqT3PBJa40c3\r\nQcIPdQKBgBnSb7BcDAAQ/Qx9juo/RKpvhyeqlnp0GzPSQjvtWi9dQRIu9Pe7luHc\r\nm1Img1EO1OyE3dis/rLaDsAa2AKu1Yx6h85EmNjavBqP9wqmFa0NIQQH8fvzKY3/\r\nP8IHY6009aoamLqYaexvrkHVq7fFKiI6k8myMJ6qblVNFv14+KXU\r\n-----END RSA PRIVATE KEY-----"  # noqa: E501
TOKEN = os.environ['API_TOKEN']

@pytest.fixture(scope='session')
def test_bot():
    return ExtBot(TOKEN, private_key=PRIVATE_KEY)

@pytest.fixture(scope='class')
def correctHelpCommandPrivateUpdate():
    return {'message': {
        'photo': [], 
        'date': 1623312815, 
        'message_id': 3010, 
        'channel_chat_created': False, 
        'entities': [{
            'offset': 0, 
            'type': 'bot_command', 
            'length': 6
        }], 
        'new_chat_members': [], 
        'supergroup_chat_created': False, 
        'delete_chat_photo': False, 
        'text': '/help', 
        'group_chat_created': False, 
        'caption_entities': [], 
        'chat': {
            'type': 'private', 
            'id': os.environ['PRIVATE_ID'], 
            'username': 
            'jianoway', 
            'first_name': 
            'Jian Wei'
        }, 
        'new_chat_photo': [], 
        'from': {
            'language_code': 'en', 
            'id': os.environ['PRIVATE_ID'], 
            'first_name': 'Jian Wei', 
            'username': 'jianoway', 
            'is_bot': False
        }}, 
    'update_id': 916267500}

@pytest.fixture(scope='class')
def wrongHelpCommandPrivateUpdate():
    return {'message': {
        'photo': [], 
        'date': 1623312815, 
        'message_id': 3010, 
        'channel_chat_created': False, 
        'entities': [{
            'offset': 0, 
            'type': 'bot_command', 
            'length': 6
        }], 
        'new_chat_members': [], 
        'supergroup_chat_created': False, 
        'delete_chat_photo': False, 
        'text': '/help', 
        'group_chat_created': False, 
        'caption_entities': [], 
        'chat': {
            'type': 'private', 
            'id': 123456, 
            'username': 
            'jianoway', 
            'first_name': 
            'Jian Wei'
        }, 
        'new_chat_photo': [], 
        'from': {
            'language_code': 'en', 
            'id': 123456, 
            'first_name': 'Jian Wei', 
            'username': 'jianoway', 
            'is_bot': False
        }}, 
    'update_id': 916267500}

@pytest.fixture(scope='class')
def correctHelpCommandGroupUpdate():
    return {'update_id': 916267451, 
        'message': {
            'supergroup_chat_created': False, 
            'group_chat_created': False, 
            'chat': {
                'id':  -447010025, 
                'all_members_are_administrators': True, 
                'type': 'group', 
                'title': 'orbital 2021'
            }, 
            'entities': [{
                'length': 20, 
                'offset': 0, 
                'type': 'bot_command'
            }],
            'delete_chat_photo': False, 
            'date': 1623306802, 
            'channel_chat_created': False, 
            'text': '/help@OwePayTestbot', 
            'photo': [], 
            'message_id': 2907, 
            'new_chat_members': [], 
            'new_chat_photo': [], 
            'caption_entities': [], 
            'from': {
                'username': 'helpGroupTest', 
                'first_name': 'test', 
                'id': 456, 
                'language_code': 'en', 
                'is_bot': False
            }
        }
    }

@pytest.fixture(scope='class')
def wrongHelpCommandGroupUpdate():
    return {'update_id': 916267451, 
        'message': {
            'supergroup_chat_created': False, 
            'group_chat_created': False, 
            'chat': {
                'id': 110333025, 
                'all_members_are_administrators': True, 
                'type': 'group', 
                'title': 'orbital 2021'
            }, 
            'entities': [{
                'length': 20, 
                'offset': 0, 
                'type': 'bot_command'
            }],
            'delete_chat_photo': False, 
            'date': 1623306802, 
            'channel_chat_created': False, 
            'text': '/help@OwePayTestbot', 
            'photo': [], 
            'message_id': 2907, 
            'new_chat_members': [], 
            'new_chat_photo': [], 
            'caption_entities': [], 
            'from': {
                'username': 'helpGroupTest', 
                'first_name': 'test', 
                'id': 456, 
                'language_code': 'en', 
                'is_bot': False
            }
        }
    }


@pytest.fixture(scope='class')
def groupHelpUpdate():
    return Update(1, TestHelp.group_message)

@pytest.fixture(scope='class')
def userHelpUpdate():
    return Update(1, TestHelp.private_message)

class tempContext:
    class bot:
        def editMessageText(chat_id, message_id, text):
            None
        class send_message:
            def __init__(self, chat_id, text):
                self.chat_id = chat_id
                self.text = text

class TestHelp():
    
    private_message = Message(3, None, Chat(4123213, 'private', username='bot'), from_user=User(5, 'bot', False, username='bot'))
    group_message = Message(3, None, Chat(4123123, 'group', username='bot'), from_user=User(5, 'bot', False, username='bot'))
    text = (
         "List of commands:\n\n" +
        "/start Initialise and register with us.\n" +
        "/help For the confused souls.\n" +
        "/whoowesme To see your debtors (only in private message).\n" +
        "/whomeowes To see your creditors (only in private message).\n"+
        "/cancel To cancel any creation of order.\n"
        "\nAfter running /start and registering in the group you wish to split bills in, you can start splitting your bills by simply typing @OwePay_bot followed by name of the order." +
        "\n\nDue to the nature of Telegram Bots, our bot will only be able to detect users if they have either sent a message in the group after I've been added or users added after me!" 
    )

    @flaky(3, 1)
    def test_help_group(self, groupHelpUpdate):
        message = help(groupHelpUpdate, tempContext)
        assert message.chat_id == 4123123
        assert message.text == self.text

    @flaky(3, 1)
    def test_help_private(self, userHelpUpdate):
        
        message = help(userHelpUpdate, tempContext)
        assert message.chat_id == 4123213
        assert message.text == self.text

    @flaky(3, 1)
    def test_help_wrong_group_id(self, wrongHelpCommandGroupUpdate, test_bot):
        with pytest.raises(BadRequest, match='Chat not found'):
            message = test_bot.send_message(
                chat_id=wrongHelpCommandGroupUpdate['message']['chat']['id'],
                text=self.text,
            )

    @flaky(3, 1)
    def test_help_wrong_private_id(self, wrongHelpCommandPrivateUpdate, test_bot):
        with pytest.raises(BadRequest, match='Chat not found'):
            message = test_bot.send_message(
                chat_id=wrongHelpCommandPrivateUpdate['message']['chat']['id'],
                text=self.text,
            )
