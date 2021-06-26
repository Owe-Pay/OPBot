import pytest
import os 

from flaky import flaky
from telegram import User, Message, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyMarkup, ReplyKeyboardMarkup, keyboardbutton, replymarkup
from telegram.ext import ExtBot

from ..owepaybot import splitEvenly, waitingForSomeNames 
from ..HELPME.bot_sql_integration import *
from ..HELPME.helperFunctions import *

# Placeholder COMPROMISED PK
PRIVATE_KEY = b"-----BEGIN RSA PRIVATE KEY-----\r\nMIIEowIBAAKCAQEA0AvEbNaOnfIL3GjB8VI4M5IaWe+GcK8eSPHkLkXREIsaddum\r\nwPBm/+w8lFYdnY+O06OEJrsaDtwGdU//8cbGJ/H/9cJH3dh0tNbfszP7nTrQD+88\r\nydlcYHzClaG8G+oTe9uEZSVdDXj5IUqR0y6rDXXb9tC9l+oSz+ShYg6+C4grAb3E\r\nSTv5khZ9Zsi/JEPWStqNdpoNuRh7qEYc3t4B/a5BH7bsQENyJSc8AWrfv+drPAEe\r\njQ8xm1ygzWvJp8yZPwOIYuL+obtANcoVT2G2150Wy6qLC0bD88Bm40GqLbSazueC\r\nRHZRug0B9rMUKvKc4FhG4AlNzBCaKgIcCWEqKwIDAQABAoIBACcIjin9d3Sa3S7V\r\nWM32JyVF3DvTfN3XfU8iUzV7U+ZOswA53eeFM04A/Ly4C4ZsUNfUbg72O8Vd8rg/\r\n8j1ilfsYpHVvphwxaHQlfIMa1bKCPlc/A6C7b2GLBtccKTbzjARJA2YWxIaqk9Nz\r\nMjj1IJK98i80qt29xRnMQ5sqOO3gn2SxTErvNchtBiwOH8NirqERXig8VCY6fr3n\r\nz7ZImPU3G/4qpD0+9ULrt9x/VkjqVvNdK1l7CyAuve3D7ha3jPMfVHFtVH5gqbyp\r\nKotyIHAyD+Ex3FQ1JV+H7DkP0cPctQiss7OiO9Zd9C1G2OrfQz9el7ewAPqOmZtC\r\nKjB3hUECgYEA/4MfKa1cvaCqzd3yUprp1JhvssVkhM1HyucIxB5xmBcVLX2/Kdhn\r\nhiDApZXARK0O9IRpFF6QVeMEX7TzFwB6dfkyIePsGxputA5SPbtBlHOvjZa8omMl\r\nEYfNa8x/mJkvSEpzvkWPascuHJWv1cEypqphu/70DxubWB5UKo/8o6cCgYEA0HFy\r\ncgwPMB//nltHGrmaQZPFT7/Qgl9ErZT3G9S8teWY4o4CXnkdU75tBoKAaJnpSfX3\r\nq8VuRerF45AFhqCKhlG4l51oW7TUH50qE3GM+4ivaH5YZB3biwQ9Wqw+QyNLAh/Q\r\nnS4/Wwb8qC9QuyEgcCju5lsCaPEXZiZqtPVxZd0CgYEAshBG31yZjO0zG1TZUwfy\r\nfN3euc8mRgZpSdXIHiS5NSyg7Zr8ZcUSID8jAkJiQ3n3OiAsuq1MGQ6kNa582kLT\r\nFPQdI9Ea8ahyDbkNR0gAY9xbM2kg/Gnro1PorH9PTKE0ekSodKk1UUyNrg4DBAwn\r\nqE6E3ebHXt/2WmqIbUD653ECgYBQCC8EAQNX3AFegPd1GGxU33Lz4tchJ4kMCNU0\r\nN2NZh9VCr3nTYjdTbxsXU8YP44CCKFG2/zAO4kymyiaFAWEOn5P7irGF/JExrjt4\r\nibGy5lFLEq/HiPtBjhgsl1O0nXlwUFzd7OLghXc+8CPUJaz5w42unqT3PBJa40c3\r\nQcIPdQKBgBnSb7BcDAAQ/Qx9juo/RKpvhyeqlnp0GzPSQjvtWi9dQRIu9Pe7luHc\r\nm1Img1EO1OyE3dis/rLaDsAa2AKu1Yx6h85EmNjavBqP9wqmFa0NIQQH8fvzKY3/\r\nP8IHY6009aoamLqYaexvrkHVq7fFKiI6k8myMJ6qblVNFv14+KXU\r\n-----END RSA PRIVATE KEY-----"  # noqa: E501
TOKEN = os.environ['API_TOKEN']


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
        )
    )


@pytest.fixture(scope='class')
def split_evenly_inline_keyboard_markup():
    return splitEvenlyKeyboardMarkup(345)

@pytest.fixture(scope='class')
def Testsplitevenlykeyboardmarkup():
    keyboardHolder = []
    users = ('456', '9871', '9872', '9873')
    count = 0
    firstnames = ('userfirstname', 'dummyuser1', 'dummyuser2', 'dummyuser3')
    usernames = ('userusername', 'dummyusername1', 'dummyusername2', 'dummyusername3')
    
    for user in users:
        firstname = firstnames[count]
        username = usernames[count]
        firstNameWithUsername = firstname + " (@" + username + ")"
        callback_data = 'splitunevenlycallbackdata' + '%s' % user 
        keyboardHolder.append([InlineKeyboardButton(firstNameWithUsername, callback_data=callback_data)])
        count = count + 1

    addEveryone = InlineKeyboardButton("Add Everyone!", callback_data='splitevenlyaddeveryonecallbackdata')
    buttonToFinalise = InlineKeyboardButton("Create Order", callback_data='SplitEvenlyFinalise')
    keyboardHolder.append([addEveryone])
    keyboardHolder.append([buttonToFinalise])
    print(InlineKeyboardMarkup(keyboardHolder))
    return InlineKeyboardMarkup(keyboardHolder)

class tempContext:
    class bot:
        def send_message(chat_id, text, reply_markup):
            return Message(1, datetime.now(), chat=Chat(chat_id, 'groupname'), text=text, reply_markup=reply_markup)



class TestSplitevenly:
    
    @flaky(3, 1)
    def test_splitevenly(self, orderUpdate,split_evenly_inline_keyboard_markup):
        
        massDelete("Users")
        massDelete("Orders")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

        assert addGroup((345, 'groupname')) == "Group groupname 345 inserted"
        assert addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"
        assert addUser((9871, 'dummyusername1', 0, 'dummyuser1')) == "User 9871 inserted"
        assert addUser((9872, 'dummyusername2', 0, 'dummyuser2')) == "User 9872 inserted"
        assert addUser((9873, 'dummyusername3', 0, 'dummyuser3')) == "User 9873 inserted"
        assert addUserToGroup(456, 345) == "User 456 added to Group 345"
        assert addUserToGroup(9871, 345) == "User 9871 added to Group 345"
        assert addUserToGroup(9872, 345) == "User 9872 added to Group 345"
        assert addUserToGroup(9873, 345) == "User 9873 added to Group 345"
        assert updateUserTempAmount('456', '345', '123') == "User 456 in Group 345 has the temporary amount 123"
        assert isinstance(waitingForSomeNames(orderUpdate, tempContext, '456', '345'), Message)
        assert splitEvenly(orderUpdate, tempContext).reply_markup==split_evenly_inline_keyboard_markup

        massDelete("Users")
        massDelete("Orders")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")