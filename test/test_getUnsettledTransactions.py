import pytest
from flaky import flaky
import datetime
from datetime import *

from telegram import Update, User, Message, Chat, InlineKeyboardMarkup, InlineKeyboardButton
from ..owepaybot import getUnsettledTransactionsForCreditor
from ..HELPME.bot_sql_integration import *
from ..HELPME.helperFunctions import *

class TestGetUnsettledTransactions:

    @flaky(3, 1)
    def test_getUnsettledTransactionsForCreditor(self):
        massDelete("Users")
        massDelete("Orders")
        massDelete("Transactions")
        massDelete("TelegramGroups")
        massDelete("UserGroupRelational")
        date = datetime.now().replace(microsecond=0)
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
        assert addTransaction(('2341', '5432', '123', '1234', '4322', date)) == "User 4322 owes User 1234 123"
        assert addTransaction(('2341', '5432', '123', '1234', '4323', date)) == "User 4323 owes User 1234 123"
        



        massDelete("Users")


        