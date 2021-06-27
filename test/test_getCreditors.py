import pytest
from flaky import flaky
import datetime
from datetime import *

from telegram import Update, User, Message, Chat, InlineKeyboardMarkup, InlineKeyboardButton
from ..owepaybot import getCreditors
from ..HELPME.bot_sql_integration import *
from ..HELPME.helperFunctions import *

date = datetime.now().replace(microsecond=0)

@pytest.fixture(scope='class')
def getCreditorUpdate():
    return Update(
        123, 
        Message(
            234, 
            text='/whomeowes', 
            chat=Chat(
                1234, 
                username='debtoruser',
                type='private',
                first_name='debtorname'
                ),
            date=datetime.now()
        )
    )

@pytest.fixture(scope='class')
def formattedKeyboardMarkupOfCreditors():
    keyboardHolder = []
    orderTitle1 = InlineKeyboardButton('Order: testOrderName1 %s (groupname)' % date.strftime("%d %B %Y"), callback_data='null')
    orderTitle2 = InlineKeyboardButton('Order: testOrderName2 %s (groupname)' % date.strftime("%d %B %Y"), callback_data='null')
    orderTitle3 = InlineKeyboardButton('Order: testOrderName3 %s (groupname)' % date.strftime("%d %B %Y"), callback_data='null')
    orders = (orderTitle1, orderTitle2, orderTitle3)
    users = ('4321', '4322', '4323')
    usernames = ('creditor1', 'creditor2', 'creditor3')
    names = ('creditorname1', 'creditorname2', 'creditorname3')
    transactionIDs = ('2341', '2342', '2343')
    count = 0
    for user in users:
        transactionID = transactionIDs[count]
        keyboardHolder.append([orders[count]])
        tempKeyboard = [
            InlineKeyboardButton('%s' % names[count], callback_data='null'),
            InlineKeyboardButton('@%s' % usernames[count], callback_data='null'),
            InlineKeyboardButton('$123.00', callback_data='null'),            
            InlineKeyboardButton('Settle', callback_data="settledebtfordebtorcallbackdata%s" % transactionID)
        ]
        count = count + 1
        keyboardHolder.append(tempKeyboard)

    return InlineKeyboardMarkup(keyboardHolder)



class contextNoMarkup:
    class bot:
        def send_message(chat_id, text):
            return Message(1, datetime.now(), chat=Chat(chat_id, 'groupname'), text=text)

class contextWithMarkup:
    class bot:
        def send_message(chat_id, text, reply_markup):
            return Message(1, datetime.now(), chat=Chat(chat_id, 'groupname'), text=text, reply_markup=reply_markup)

class TestGetCreditors:

    @flaky(3, 1)
    def test_getCreditorsUserNotAdded(self, getCreditorUpdate):
        massDelete("Users")
        massDelete("Orders")
        massDelete("Transactions")
        massDelete("TelegramGroups")
        assert isinstance(getCreditors(getCreditorUpdate, contextNoMarkup), Message)
        assert getCreditors(getCreditorUpdate, contextNoMarkup).chat_id == 1234
        assert getCreditors(getCreditorUpdate, contextNoMarkup).text == 'Please register with us first by using /start!'

    @flaky(3, 1)
    def test_getCreditorsNoOneOwes(self, getCreditorUpdate):
        massDelete("Users")
        massDelete("Orders")
        massDelete("Transactions")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")
        assert addUser(('1234', 'debtor', 0, 'debtorname')) == "User 1234 inserted"
        assert addGroup(('9871', 'groupname')) == "Group groupname 9871 inserted"
        assert addUserToGroup('1234', '9871') == "User 1234 added to Group 9871"
        assert isinstance(getCreditors(getCreditorUpdate, contextNoMarkup), Message)
        assert getCreditors(getCreditorUpdate, contextNoMarkup).chat_id == 1234
        assert getCreditors(getCreditorUpdate, contextNoMarkup).text == "Wow! Amazing! You don't owe anyone any money!"
        

    @flaky(3, 1)
    def test_getCreditors(self, getCreditorUpdate, formattedKeyboardMarkupOfCreditors):
        massDelete("Users")
        massDelete("Orders")
        massDelete("Transactions")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

        assert addUser(('1234', 'debtoruser', 0, 'debtorname')) == "User 1234 inserted"
        assert addUser(('4321', 'creditor1', 0, 'creditorname1')) == "User 4321 inserted"
        assert addUser(('4322', 'creditor2', 0, 'creditorname2')) == "User 4322 inserted"
        assert addUser(('4323', 'creditor3', 0, 'creditorname3')) == "User 4323 inserted"
        assert addGroup(('9871', 'groupname')) == "Group groupname 9871 inserted"
        assert addUserToGroup('1234', '9871') == "User 1234 added to Group 9871"
        assert addUserToGroup('4321', '9871') == "User 4321 added to Group 9871"
        assert addUserToGroup('4322', '9871') == "User 4322 added to Group 9871"
        assert addUserToGroup('4323', '9871') == "User 4323 added to Group 9871"
        assert addOrder(('5432', '9871', 'testOrderName1', '123', '4321', date)) == "Order 5432 has been added"
        assert addOrder(('5433', '9871', 'testOrderName2', '123', '4322', date)) == "Order 5433 has been added"
        assert addOrder(('5434', '9871', 'testOrderName3', '123', '4323', date)) == "Order 5434 has been added"
        assert addTransaction(('2341', '5432', '123', '4321', '1234', date)) == "User 1234 owes User 4321 123"
        assert addTransaction(('2342', '5433', '123', '4322', '1234', date)) == "User 1234 owes User 4322 123"
        assert addTransaction(('2343', '5434', '123', '4323', '1234', date)) == "User 1234 owes User 4323 123"
        assert getUnsettledTransactionsForDebtor('1234') == [
            ('2341', '5432', '4321', 123),
            ('2342', '5433', '4322', 123),
            ('2343', '5434', '4323', 123)
        ]
        assert formatTransactionsForDebtorKeyboardMarkup(getUnsettledTransactionsForDebtor('1234')) == formattedKeyboardMarkupOfCreditors
        assert isinstance(getCreditors(getCreditorUpdate, contextWithMarkup), Message)
        assert getCreditors(getCreditorUpdate, contextWithMarkup).chat_id == 1234
        assert getCreditors(getCreditorUpdate, contextWithMarkup).text == "The kind people who you've taken from:"
        assert getCreditors(getCreditorUpdate, contextWithMarkup).reply_markup == formattedKeyboardMarkupOfCreditors

        massDelete("Users")
        massDelete("Orders")
        massDelete("Transactions")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

