import pytest

from flaky import flaky

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyMarkup, ReplyKeyboardMarkup

@pytest.fixture(scope='class')
def group_registration_inline_keyboard_markup():
    return InlineKeyboardMarkup(TestGroupRegistrationInlineKeyboardMarkup.keyboard)

class TestGroupRegistrationInlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("Register", callback_data='groupRegister'),
        ],
        [
            InlineKeyboardButton("Don't Register", callback_data='groupDontRegister')
        ],
    ]
    text = (
            "Hello this is O$P$, your personal Telegram loan chaser and debt tracker!\n\n" +
            "We aim to make the process of tracking which of your 'friends' still owe you " +
            "and reminding them as impersonal as possible so you won't feel the paiseh!"
            "Along with that, you can now also notify people who you've returned money to" +
            "with a simple click of a  button.\n\n" +
            "Simply register your group with us by pressing the button below!"
        )

    @flaky(3, 1)
    def test_send_message_with_inline_keyboard_markup(self, chat_id, bot, group_registration_inline_keyboard_markup):
        message = bot.send_message(
            chat_id=chat_id, 
            text=TestGroupRegistrationInlineKeyboardMarkup.text, 
            reply_markup=group_registration_inline_keyboard_markup
        )

        register_button = InlineKeyboardButton("Register", callback_data='groupRegister')
        dont_register_button = InlineKeyboardButton("Don't Register", callback_data='groupDontRegister')

        assert message.text == self.text
        assert message.reply_markup == InlineKeyboardMarkup(self.keyboard)
    