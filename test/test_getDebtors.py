import pytest
from flaky import flaky
import datetime
from datetime import *

from telegram import Update, User, Message, Chat, InlineKeyboardMarkup, InlineKeyboardButton
from ..owepaybot import getDebtors
from ..HELPME.bot_sql_integration import *
from ..HELPME.helperFunctions import *

date = datetime.now().replace(microsecond=0)

@pytest.fixture(scope='class')
def getDebtorUpdate():
    return Update(
        123, 
        Message(
            234, 
            text='/whoowesme', 
            chat=Chat(
                1234, 
                username='creditoruser',
                type='private',
                first_name='creditorname'
                ),
            date=datetime.now()
        )
    )

@pytest.fixture(scope='class')
def formattedKeyboardMarkupOfDebtors():
    keyboardHolder = []
    orderTitle = InlineKeyboardButton('Order: testOrderName %s (groupname)' % date.strftime("%d %B %Y"), callback_data='null')
    keyboardHolder.append([orderTitle])
    users = ('4321', '4322', '4323')
    usernames = ('debtor1', 'debtor2', 'debtor3')
    names = ('debtorname1', 'debtorname2', 'debtorname3')
    transactionIDs = ('2341', '2342', '2343')
    count = 0
    for user in users:
        transactionID = transactionIDs[count]
        tempKeyboard = [
            InlineKeyboardButton('%s' % names[count], callback_data='null'),
            InlineKeyboardButton('@%s' % usernames[count], callback_data='null'),
            InlineKeyboardButton('$123.00', callback_data='null'),            
            InlineKeyboardButton('Notify', callback_data="notifydebtorcallbackdata%s" % transactionID),
            InlineKeyboardButton('Settle', callback_data="settledebtforcreditor%s" % transactionID)
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

class TestGetDebtors:

    @flaky(3, 1)
    def test_getDebtorsUserNotAdded(self, getDebtorUpdate):
        massDelete("Users")
        massDelete("Orders")
        massDelete("Transactions")
        massDelete("TelegramGroups")
        assert isinstance(getDebtors(getDebtorUpdate, contextNoMarkup), Message)
        assert getDebtors(getDebtorUpdate, contextNoMarkup).chat_id == 1234
        assert getDebtors(getDebtorUpdate, contextNoMarkup).text == 'Please register with us first by using /start!'

    @flaky(3, 1)
    def test_getDebtorsNoOneOwes(self, getDebtorUpdate):
        massDelete("Users")
        massDelete("Orders")
        massDelete("Transactions")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")
        assert addUser(('1234', 'creditoruser', 0, 'creditorname')) == "User 1234 inserted"
        assert addGroup(('9871', 'groupname')) == "Group groupname 9871 inserted"
        assert addUserToGroup('1234', '9871') == "User 1234 added to Group 9871"
        assert isinstance(getDebtors(getDebtorUpdate, contextNoMarkup), Message)
        assert getDebtors(getDebtorUpdate, contextNoMarkup).chat_id == 1234
        assert getDebtors(getDebtorUpdate, contextNoMarkup).text == 'No one owes you money! What great friends you have!!!'
        

    @flaky(3, 1)
    def test_getDebtors(self, getDebtorUpdate, formattedKeyboardMarkupOfDebtors):
        massDelete("Users")
        massDelete("Orders")
        massDelete("Transactions")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")

        assert addUser(('1234', 'creditoruser', 0, 'creditorname')) == "User 1234 inserted"
        assert addUser(('4321', 'debtor1', 0, 'debtorname1')) == "User 4321 inserted"
        assert addUser(('4322', 'debtor2', 0, 'debtorname2')) == "User 4322 inserted"
        assert addUser(('4323', 'debtor3', 0, 'debtorname3')) == "User 4323 inserted"
        assert addGroup(('9871', 'groupname')) == "Group groupname 9871 inserted"
        assert addUserToGroup('1234', '9871') == "User 1234 added to Group 9871"
        assert addUserToGroup('4321', '9871') == "User 4321 added to Group 9871"
        assert addUserToGroup('4322', '9871') == "User 4322 added to Group 9871"
        assert addUserToGroup('4323', '9871') == "User 4323 added to Group 9871"
        assert addOrder(('5432', '9871', 'testOrderName', '369', '1234', date)) == "Order 5432 has been added"
        assert addTransaction(('2341', '5432', '123', '1234', '4321', date)) == "User 4321 owes User 1234 123"
        assert addTransaction(('2342', '5432', '123', '1234', '4322', date)) == "User 4322 owes User 1234 123"
        assert addTransaction(('2343', '5432', '123', '1234', '4323', date)) == "User 4323 owes User 1234 123"
        assert getUnsettledTransactionsForCreditor('1234') == [
            ('2341', '5432', '4321', 123),
            ('2342', '5432', '4322', 123),
            ('2343', '5432', '4323', 123),
        ]
        assert formatTransactionsForCreditorKeyboardMarkup(getUnsettledTransactionsForCreditor('1234')) == formattedKeyboardMarkupOfDebtors
        assert isinstance(getDebtors(getDebtorUpdate, contextWithMarkup), Message)
        assert getDebtors(getDebtorUpdate, contextWithMarkup).chat_id == 1234
        assert getDebtors(getDebtorUpdate, contextWithMarkup).text == 'The baddies who have your cash money! >:('
        assert getDebtors(getDebtorUpdate, contextWithMarkup).reply_markup == formattedKeyboardMarkupOfDebtors

        massDelete("Users")
        massDelete("Orders")
        massDelete("Transactions")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")