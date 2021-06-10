import pytest

from flaky import flaky
from telegram import InlineKeyboardButton

@pytest.fixture(scope='class')
def group_register_inline_keyboard_button():
    return InlineKeyboardButton(
        TestGroupRegisterInlineKeyboardButton.text,
        callback_data=TestGroupRegisterInlineKeyboardButton.callback_data,
    )

@pytest.fixture(scope='class')
def group_dont_register_inline_keyboard_button():
    return InlineKeyboardButton(
        TestGroupDontRegisterInlineKeyboardButton.text,
        callback_data=TestGroupDontRegisterInlineKeyboardButton.callback_data,
    )

@pytest.fixture(scope='class')
def user_register_inline_keyboard_button():
    return InlineKeyboardButton(
        TestUserRegisterInlineKeyboardButton.text,
        callback_data=TestUserRegisterInlineKeyboardButton.callback_data,
    )

@pytest.fixture(scope='class')
def user_dont_register_inline_keyboard_button():
    return InlineKeyboardButton(
        TestUserDontRegisterInlineKeyboardButton.text,
        callback_data=TestUserDontRegisterInlineKeyboardButton.callback_data,
    )

class TestGroupRegisterInlineKeyboardButton:
    text = 'Register'
    callback_data = 'groupRegister'

    @flaky(3, 1)
    def test_expected_values(self, group_register_inline_keyboard_button):
        assert group_register_inline_keyboard_button.text == self.text
        assert group_register_inline_keyboard_button.callback_data == self.callback_data

    @flaky(3, 1)
    def test_to_dict(self, group_register_inline_keyboard_button):
        group_register_inline_keyboard_button_dict = group_register_inline_keyboard_button.to_dict()

        assert isinstance(group_register_inline_keyboard_button_dict, dict)
        assert group_register_inline_keyboard_button_dict['text'] == self.text
        assert group_register_inline_keyboard_button_dict['callback_data'] == self.callback_data

class TestGroupDontRegisterInlineKeyboardButton:
    text = "Don't Register"
    callback_data = 'groupDontRegister'

    @flaky(3, 1)
    def test_expected_values(self, group_dont_register_inline_keyboard_button):
        assert group_dont_register_inline_keyboard_button.text == self.text
        assert group_dont_register_inline_keyboard_button.callback_data == self.callback_data

    @flaky(3, 1)
    def test_to_dict(self, group_dont_register_inline_keyboard_button):
        group_dont_register_inline_keyboard_button_dict = group_dont_register_inline_keyboard_button.to_dict()

        assert isinstance(group_dont_register_inline_keyboard_button_dict, dict)
        assert group_dont_register_inline_keyboard_button_dict['text'] == self.text
        assert group_dont_register_inline_keyboard_button_dict['callback_data'] == self.callback_data

class TestBetweenGroupRegisterInlineKeyboardButtons:
    @flaky(3, 1)
    def test_equality(self):
        temp_group_register_inline_keyboard_button_1 = InlineKeyboardButton('Register', callback_data='groupRegister')
        temp_group_register_inline_keyboard_button_2 = InlineKeyboardButton('Register', callback_data='groupRegister')
        temp_group_dont_register_inline_keyboard_button_1 = InlineKeyboardButton("Don't Register", callback_data='groupDontRegister')
        temp_group_dont_register_inline_keyboard_button_2 = InlineKeyboardButton("Don't Register", callback_data='groupDontRegister')

        assert temp_group_register_inline_keyboard_button_1 == temp_group_register_inline_keyboard_button_2
        assert hash(temp_group_register_inline_keyboard_button_1) == hash(temp_group_register_inline_keyboard_button_2)

        assert temp_group_dont_register_inline_keyboard_button_1 == temp_group_dont_register_inline_keyboard_button_2
        assert hash(temp_group_dont_register_inline_keyboard_button_1) == hash(temp_group_dont_register_inline_keyboard_button_2)

        assert temp_group_register_inline_keyboard_button_1 != temp_group_dont_register_inline_keyboard_button_1
        assert hash(temp_group_register_inline_keyboard_button_1) != hash(temp_group_dont_register_inline_keyboard_button_1)

class TestUserRegisterInlineKeyboardButton:
    text = 'Register'
    callback_data = 'userRegister'

    @flaky(3, 1)
    def test_expected_values(self, user_register_inline_keyboard_button):
        assert user_register_inline_keyboard_button.text == self.text
        assert user_register_inline_keyboard_button.callback_data == self.callback_data

    @flaky(3, 1)
    def test_to_dict(self, user_register_inline_keyboard_button):
        user_register_inline_keyboard_button_dict = user_register_inline_keyboard_button.to_dict()

        assert isinstance(user_register_inline_keyboard_button_dict, dict)
        assert user_register_inline_keyboard_button_dict['text'] == self.text
        assert user_register_inline_keyboard_button_dict['callback_data'] == self.callback_data

class TestUserDontRegisterInlineKeyboardButton:
    text = "Don't Register"
    callback_data = 'userDontRegister'

    @flaky(3, 1)
    def test_expected_values(self, user_dont_register_inline_keyboard_button):
        assert user_dont_register_inline_keyboard_button.text == self.text
        assert user_dont_register_inline_keyboard_button.callback_data == self.callback_data

    @flaky(3, 1)
    def test_to_dict(self, user_dont_register_inline_keyboard_button):
        user_dont_register_inline_keyboard_button_dict = user_dont_register_inline_keyboard_button.to_dict()

        assert isinstance(user_dont_register_inline_keyboard_button_dict, dict)
        assert user_dont_register_inline_keyboard_button_dict['text'] == self.text
        assert user_dont_register_inline_keyboard_button_dict['callback_data'] == self.callback_data

class TestBetweenUserRegisterInlineKeyboardButtons:
    
    @flaky(3, 1)
    def test_equality(self):
        temp_user_register_inline_keyboard_button_1 = InlineKeyboardButton('Register', callback_data='userRegister')
        temp_user_register_inline_keyboard_button_2 = InlineKeyboardButton('Register', callback_data='userRegister')
        temp_user_dont_register_inline_keyboard_button_1 = InlineKeyboardButton("Don't Register", callback_data='userDontRegister')
        temp_user_dont_register_inline_keyboard_button_2 = InlineKeyboardButton("Don't Register", callback_data='userDontRegister')

        assert temp_user_register_inline_keyboard_button_1 == temp_user_register_inline_keyboard_button_2
        assert hash(temp_user_register_inline_keyboard_button_1) == hash(temp_user_register_inline_keyboard_button_2)

        assert temp_user_dont_register_inline_keyboard_button_1 == temp_user_dont_register_inline_keyboard_button_2
        assert hash(temp_user_dont_register_inline_keyboard_button_1) == hash(temp_user_dont_register_inline_keyboard_button_2)

        assert temp_user_register_inline_keyboard_button_1 != temp_user_dont_register_inline_keyboard_button_1
        assert hash(temp_user_register_inline_keyboard_button_1) != hash(temp_user_dont_register_inline_keyboard_button_1)






