import pytest
import os

from flaky import flaky
from telegram import Chat, User, Message, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyMarkup, ReplyKeyboardMarkup, keyboardbutton, replymarkup
from telegram.ext import ExtBot
from telegram.error import BadRequest, InvalidToken
from ..owepaybot import startGroup
from ..HELPME.bot_sql_integration import *

# Placeholder COMPROMISED PK
PRIVATE_KEY = b"-----BEGIN RSA PRIVATE KEY-----\r\nMIIEowIBAAKCAQEA0AvEbNaOnfIL3GjB8VI4M5IaWe+GcK8eSPHkLkXREIsaddum\r\nwPBm/+w8lFYdnY+O06OEJrsaDtwGdU//8cbGJ/H/9cJH3dh0tNbfszP7nTrQD+88\r\nydlcYHzClaG8G+oTe9uEZSVdDXj5IUqR0y6rDXXb9tC9l+oSz+ShYg6+C4grAb3E\r\nSTv5khZ9Zsi/JEPWStqNdpoNuRh7qEYc3t4B/a5BH7bsQENyJSc8AWrfv+drPAEe\r\njQ8xm1ygzWvJp8yZPwOIYuL+obtANcoVT2G2150Wy6qLC0bD88Bm40GqLbSazueC\r\nRHZRug0B9rMUKvKc4FhG4AlNzBCaKgIcCWEqKwIDAQABAoIBACcIjin9d3Sa3S7V\r\nWM32JyVF3DvTfN3XfU8iUzV7U+ZOswA53eeFM04A/Ly4C4ZsUNfUbg72O8Vd8rg/\r\n8j1ilfsYpHVvphwxaHQlfIMa1bKCPlc/A6C7b2GLBtccKTbzjARJA2YWxIaqk9Nz\r\nMjj1IJK98i80qt29xRnMQ5sqOO3gn2SxTErvNchtBiwOH8NirqERXig8VCY6fr3n\r\nz7ZImPU3G/4qpD0+9ULrt9x/VkjqVvNdK1l7CyAuve3D7ha3jPMfVHFtVH5gqbyp\r\nKotyIHAyD+Ex3FQ1JV+H7DkP0cPctQiss7OiO9Zd9C1G2OrfQz9el7ewAPqOmZtC\r\nKjB3hUECgYEA/4MfKa1cvaCqzd3yUprp1JhvssVkhM1HyucIxB5xmBcVLX2/Kdhn\r\nhiDApZXARK0O9IRpFF6QVeMEX7TzFwB6dfkyIePsGxputA5SPbtBlHOvjZa8omMl\r\nEYfNa8x/mJkvSEpzvkWPascuHJWv1cEypqphu/70DxubWB5UKo/8o6cCgYEA0HFy\r\ncgwPMB//nltHGrmaQZPFT7/Qgl9ErZT3G9S8teWY4o4CXnkdU75tBoKAaJnpSfX3\r\nq8VuRerF45AFhqCKhlG4l51oW7TUH50qE3GM+4ivaH5YZB3biwQ9Wqw+QyNLAh/Q\r\nnS4/Wwb8qC9QuyEgcCju5lsCaPEXZiZqtPVxZd0CgYEAshBG31yZjO0zG1TZUwfy\r\nfN3euc8mRgZpSdXIHiS5NSyg7Zr8ZcUSID8jAkJiQ3n3OiAsuq1MGQ6kNa582kLT\r\nFPQdI9Ea8ahyDbkNR0gAY9xbM2kg/Gnro1PorH9PTKE0ekSodKk1UUyNrg4DBAwn\r\nqE6E3ebHXt/2WmqIbUD653ECgYBQCC8EAQNX3AFegPd1GGxU33Lz4tchJ4kMCNU0\r\nN2NZh9VCr3nTYjdTbxsXU8YP44CCKFG2/zAO4kymyiaFAWEOn5P7irGF/JExrjt4\r\nibGy5lFLEq/HiPtBjhgsl1O0nXlwUFzd7OLghXc+8CPUJaz5w42unqT3PBJa40c3\r\nQcIPdQKBgBnSb7BcDAAQ/Qx9juo/RKpvhyeqlnp0GzPSQjvtWi9dQRIu9Pe7luHc\r\nm1Img1EO1OyE3dis/rLaDsAa2AKu1Yx6h85EmNjavBqP9wqmFa0NIQQH8fvzKY3/\r\nP8IHY6009aoamLqYaexvrkHVq7fFKiI6k8myMJ6qblVNFv14+KXU\r\n-----END RSA PRIVATE KEY-----"  # noqa: E501
TOKEN = os.environ['API_TOKEN']

@pytest.fixture(scope='class')
def group_inline_keyboard_markup():
    return InlineKeyboardMarkup(TestStartGroup.keyboard)

@pytest.fixture(scope='class')
def groupUpdate():
    return Update(1, TestStartGroup.group_message)

@pytest.fixture(scope='session')
def test_bot():
    return ExtBot(TOKEN, private_key=PRIVATE_KEY)

class contextWithMarkup:
    class bot:
        def send_message(chat_id, text, reply_markup):
            return Message(1, datetime.now(), chat=Chat(chat_id, 'test,bot'), text=text, reply_markup=reply_markup)

class TestStartGroup:

    group_message = Message(3, None, Chat(4321234, 'group', username='test,bot', first_name='botname'), from_user=User(5, 'bot', False, username='bota'))
    keyboard = [
        [
            InlineKeyboardButton("Register", callback_data='groupRegister'),
        ],
        [
            InlineKeyboardButton("Don't Register", callback_data='groupDontRegister')
        ],
    ]

    inline_keyboard_markup_to_be_sent = InlineKeyboardMarkup(keyboard)
    text = (
       "Hello this is O$P$, your personal Telegram loan chaser and debt tracker!\n\n" +
        "We aim to make the process of tracking which of your 'friends' still owe you " +
        "and reminding them as impersonal as possible so you won't feel the paiseh!"
        "Along with that, you can now also notify people who you've returned money to" +
        "with a simple click of a button.\n\n" +
        "Simply register your group with us by pressing the button below!"
    )

    @flaky(3, 1)
    def test_startGroup(self, groupUpdate):
        assert isinstance(startGroup(groupUpdate, contextWithMarkup), Message)
        assert startGroup(groupUpdate, contextWithMarkup).chat_id == 4321234
        assert startGroup(groupUpdate, contextWithMarkup).text == self.text
        assert startGroup(groupUpdate, contextWithMarkup).reply_markup == InlineKeyboardMarkup(self.keyboard)

        
    @flaky(3, 1)
    def test_invalid_group_id(self, wrongStartCommandGroupIDUpdate, test_bot, group_inline_keyboard_markup):
        
        # Test if a bad request error is thrown if using an invalid group id to send a message
        with pytest.raises(BadRequest, match='Chat not found'):
            message = test_bot.send_message(
                chat_id=wrongStartCommandGroupIDUpdate['message']['chat']['id'],
                text=self.text,
                reply_markup=group_inline_keyboard_markup,
            )


