import pytest
import os

from flaky import flaky
from telegram import Message, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyMarkup, ReplyKeyboardMarkup, keyboardbutton, replymarkup
from telegram.ext import ExtBot
from telegram.error import BadRequest, InvalidToken

# Placeholder COMPROMISED PK
PRIVATE_KEY = b"-----BEGIN RSA PRIVATE KEY-----\r\nMIIEowIBAAKCAQEA0AvEbNaOnfIL3GjB8VI4M5IaWe+GcK8eSPHkLkXREIsaddum\r\nwPBm/+w8lFYdnY+O06OEJrsaDtwGdU//8cbGJ/H/9cJH3dh0tNbfszP7nTrQD+88\r\nydlcYHzClaG8G+oTe9uEZSVdDXj5IUqR0y6rDXXb9tC9l+oSz+ShYg6+C4grAb3E\r\nSTv5khZ9Zsi/JEPWStqNdpoNuRh7qEYc3t4B/a5BH7bsQENyJSc8AWrfv+drPAEe\r\njQ8xm1ygzWvJp8yZPwOIYuL+obtANcoVT2G2150Wy6qLC0bD88Bm40GqLbSazueC\r\nRHZRug0B9rMUKvKc4FhG4AlNzBCaKgIcCWEqKwIDAQABAoIBACcIjin9d3Sa3S7V\r\nWM32JyVF3DvTfN3XfU8iUzV7U+ZOswA53eeFM04A/Ly4C4ZsUNfUbg72O8Vd8rg/\r\n8j1ilfsYpHVvphwxaHQlfIMa1bKCPlc/A6C7b2GLBtccKTbzjARJA2YWxIaqk9Nz\r\nMjj1IJK98i80qt29xRnMQ5sqOO3gn2SxTErvNchtBiwOH8NirqERXig8VCY6fr3n\r\nz7ZImPU3G/4qpD0+9ULrt9x/VkjqVvNdK1l7CyAuve3D7ha3jPMfVHFtVH5gqbyp\r\nKotyIHAyD+Ex3FQ1JV+H7DkP0cPctQiss7OiO9Zd9C1G2OrfQz9el7ewAPqOmZtC\r\nKjB3hUECgYEA/4MfKa1cvaCqzd3yUprp1JhvssVkhM1HyucIxB5xmBcVLX2/Kdhn\r\nhiDApZXARK0O9IRpFF6QVeMEX7TzFwB6dfkyIePsGxputA5SPbtBlHOvjZa8omMl\r\nEYfNa8x/mJkvSEpzvkWPascuHJWv1cEypqphu/70DxubWB5UKo/8o6cCgYEA0HFy\r\ncgwPMB//nltHGrmaQZPFT7/Qgl9ErZT3G9S8teWY4o4CXnkdU75tBoKAaJnpSfX3\r\nq8VuRerF45AFhqCKhlG4l51oW7TUH50qE3GM+4ivaH5YZB3biwQ9Wqw+QyNLAh/Q\r\nnS4/Wwb8qC9QuyEgcCju5lsCaPEXZiZqtPVxZd0CgYEAshBG31yZjO0zG1TZUwfy\r\nfN3euc8mRgZpSdXIHiS5NSyg7Zr8ZcUSID8jAkJiQ3n3OiAsuq1MGQ6kNa582kLT\r\nFPQdI9Ea8ahyDbkNR0gAY9xbM2kg/Gnro1PorH9PTKE0ekSodKk1UUyNrg4DBAwn\r\nqE6E3ebHXt/2WmqIbUD653ECgYBQCC8EAQNX3AFegPd1GGxU33Lz4tchJ4kMCNU0\r\nN2NZh9VCr3nTYjdTbxsXU8YP44CCKFG2/zAO4kymyiaFAWEOn5P7irGF/JExrjt4\r\nibGy5lFLEq/HiPtBjhgsl1O0nXlwUFzd7OLghXc+8CPUJaz5w42unqT3PBJa40c3\r\nQcIPdQKBgBnSb7BcDAAQ/Qx9juo/RKpvhyeqlnp0GzPSQjvtWi9dQRIu9Pe7luHc\r\nm1Img1EO1OyE3dis/rLaDsAa2AKu1Yx6h85EmNjavBqP9wqmFa0NIQQH8fvzKY3/\r\nP8IHY6009aoamLqYaexvrkHVq7fFKiI6k8myMJ6qblVNFv14+KXU\r\n-----END RSA PRIVATE KEY-----"  # noqa: E501
TOKEN = os.environ['API_TOKEN']

@pytest.fixture(scope='class')
def private_inline_keyboard_markup():
    return InlineKeyboardMarkup(TestStartPrivate.keyboard)

@pytest.fixture(scope='session')
def test_bot():
    return ExtBot(TOKEN, private_key=PRIVATE_KEY)

class TestStartPrivate:
    keyboard = [
        [
            InlineKeyboardButton("Register", callback_data='userRegister'),
        ],
        [
            InlineKeyboardButton("Don't Register", callback_data='userDontRegister')
        ],
    ]

    chat_id = int(os.environ['PRIVATE_ID'])
    inline_keyboard_markup_to_be_sent = InlineKeyboardMarkup(keyboard)
    testd = InlineKeyboardButton("Register", callback_data='userRegister')
    text = (
       "Hi! Thank you for choosing O$P$, your one stop debt chaser!\n\n" +
        "Simply register with us by clicking pressing the button below!"
    )

    @flaky(3, 1)
    def test_send_message(self, correctStartCommandPrivateUpdate, test_bot, private_inline_keyboard_markup):
        message = test_bot.send_message(
            chat_id=correctStartCommandPrivateUpdate['message']['chat']['id'],
            text=self.text,
            reply_markup=private_inline_keyboard_markup,
        )
        # Testing that the message variable to be sent
        assert message.chat_id == self.chat_id
        assert message.text == self.text
        assert message.reply_markup == self.inline_keyboard_markup_to_be_sent
        assert message.reply_markup.inline_keyboard == self.keyboard

        # Testing text in buttons
        assert message.reply_markup.inline_keyboard[0][0].text == 'Register'
        assert message.reply_markup.inline_keyboard[1][0].text == "Don't Register"

        # Testing functionality of buttons where their callback data remains the same
        assert message.reply_markup.inline_keyboard[0][0].callback_data == 'userRegister'
        assert message.reply_markup.inline_keyboard[1][0].callback_data == 'userDontRegister'
    
    @flaky(3, 1)
    def test_invalid_user_id(self, wrongStartCommandPrivateIDUpdate, test_bot, private_inline_keyboard_markup):
        
        # Test if a bad request error is thrown if using an invalid group id to send a message
        with pytest.raises(BadRequest, match='Chat not found'):
            message = test_bot.send_message(
                chat_id=wrongStartCommandPrivateIDUpdate['message']['chat']['id'],
                text=self.text,
                reply_markup=private_inline_keyboard_markup,
            )


