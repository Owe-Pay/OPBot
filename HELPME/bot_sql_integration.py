from tokenize import group
import pytz
import pymysql
from tabulate import tabulate
from uuid import uuid1
import datetime
from datetime import timedelta
import time
import os
from datetime import *

from telegram import message

db_host = os.environ['DB_HOST']
db_username = os.environ['DB_USER']
db_database = os.environ['DB_DB']
db_password = os.environ['DB_PASSWORD']

tz = pytz.timezone('Asia/Singapore') 
now = datetime.now(tz) # the current time in your local timezone

#############################
# Functions for General Use #
#############################

def closeConnection(connection, cursor):
    cursor.close()
    connection.close()

def massDelete(table):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mycursor.execute("DELETE FROM " + table)
    mysqldb.commit()
    return 'deleted %s' % table
    # print('Records updated successfully! %s is now empty') % table

# massDelete("orders")
# massDelete("transactions")
#############################
# Functions for Users Table #
#############################

def addUser(input):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    sql = "INSERT into Users (UserID, UserName, notifiable, FirstName) VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, input)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print('User added successfully!')
    return "User %s inserted" % input[0]

# addUser((339096917,"poo_poo_platter",1))


def displayUsers():
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT * from users")
    result = mycursor.fetchall()
    closeConnection(mysqldb, mycursor)
    print(tabulate(result, headers=[
        "UserID", "UserName", "notifiable"]))

def userAlreadyAdded(primary_key):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM Users WHERE UserID LIKE %s" % primary_key
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return (t!=None)

def isNotifiable(user_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM Users WHERE UserID LIKE %s and notifiable LIKE %d" % (user_id, 1)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return (t!=None)

def makeNotifiable(user_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE Users SET notifiable = 1 WHERE UserID = %s" % user_id
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print("User is now notifiable!")

def updateUserStateSplitAllEvenly(userId, groupId):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE UserGroupRelational SET State = 'splitallevenly' WHERE UserID LIKE %s and GroupID LIKE %s" % (userId, groupId)
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print("User is now in splitall state temporarily!")

def updateUserStateSplitEvenly(userId, groupId):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE UserGroupRelational SET State = 'splitevenly' WHERE UserID LIKE %s and GroupID LIKE %s" % (userId, groupId)
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    return "User %s in Group %s has state 'splitevenly'" % (userId, groupId)

def updateUserTempAmount(user_id, group_id, amount):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE UserGroupRelational SET Temp_Amount = %s WHERE UserID LIKE %s and GroupID LIKE %s" % (amount,user_id, group_id)
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    return "User %s in Group %s has the temporary amount %s" % (user_id, group_id, amount)

def userStateSplitAllEvenly(user_id,group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM UserGroupRelational WHERE UserID LIKE %s and GroupID LIKE %s and State = 'splitallevenly' " % (user_id, group_id)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return (t!=None)

def userStateSplitEvenly(user_id,group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM UserGroupRelational WHERE UserID LIKE %s and GroupID LIKE %s and State = 'splitevenly' " % (user_id, group_id)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return (t!=None)

def updateUserStateSplitUnevenlyWaitingForName(userID, groupID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE UserGroupRelational SET State = 'splitunevenlywaitingname' WHERE UserID LIKE %s and GroupID LIKE %s" % (userID, groupID)
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    return "User %s in Group %s has state 'splitunevenlywaitingname'" % (userID, groupID)

def userStateSplitUnevenlyWaitingForName(user_id,group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    #state ='active'
    mysql = "SELECT * FROM UserGroupRelational WHERE UserID LIKE %s and GroupID LIKE %s and State = 'splitunevenlywaitingname' " % (user_id, group_id)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return (t!=None)

def updateUserStateSplitUnevenly(userID, groupID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE UserGroupRelational SET State = 'splitunevenly' WHERE UserID LIKE %s and GroupID LIKE %s" % (userID, groupID)
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    return "User %s in Group %s has state 'splitunevenly'" % (userID, groupID)

def userStateSplitUnevenly(user_id,group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    #state ='active'
    mysql = "SELECT * FROM UserGroupRelational WHERE UserID LIKE %s and GroupID LIKE %s and State = 'splitunevenly' " % (user_id, group_id)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return (t!=None)


def updateUserStateWaitingForSomeNames(user_id, group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE usergrouprelational SET State = 'waitingforsomenames' WHERE UserID = %s and GroupID = %s" % (user_id, group_id)
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print("set back into inactive")

def setUserStateInactive(user_id, group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE usergrouprelational SET State = 'inactive' WHERE UserID = %s and GroupID = %s" % (user_id, group_id)
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print("set back into inactive")

def resetUserTempAmount(user_id,group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE UserGroupRelational SET Temp_Amount = 0 WHERE UserID LIKE %s and GroupID LIKE %s" % (user_id, group_id)
    mycursor.execute(mysql)
    mysqldb.commit()
    # t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    print("reset temp amount to 0")

def resetUserTempOrderID(user_id, group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE UserGroupRelational SET Temp_OrderID = NULL WHERE UserID LIKE %s and GroupID LIKE %s" % (user_id, group_id)
    mycursor.execute(mysql)
    mysqldb.commit()
    # t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    print("reset temp amount to 0")

def updateUserTempItemList(userID, groupID, itemList):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE UserGroupRelational SET Temp_OrderID = %s WHERE UserID LIKE %s and GroupID LIKE %s" % (itemList, userID, groupID)
    mycursor.execute(mysql)
    mysqldb.commit()
    # t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)

def getUserTempAmount(user_id,group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM UserGroupRelational WHERE UserID LIKE %s and GroupID LIKE %s" % (user_id, group_id)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    print(t[2])
    return t[2]

def getUsername(userID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = 'SELECT USERNAME FROM Users WHERE UserID LIKE %s' % userID
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return t[0]

def getFirstName(userID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = 'SELECT FirstName FROM Users WHERE UserID LIKE %s' % userID
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return t[0]

# print(getUsername(123))

def getUsernameListFromUserIDList(userIDList):
    holder = []
    for userID in userIDList:        
        mysqldb = pymysql.connect(
            host=db_host, user=db_username, password=db_password, db=db_database)
        mycursor = mysqldb.cursor()
        mysql = "SELECT USERNAME FROM Users WHERE UserID LIKE %s" % userID
        mycursor.execute(mysql)
        t = mycursor.fetchone()
        closeConnection(mysqldb, mycursor)
        holder.append(t[0])
    return holder

def getUserIDListFromUsernameList(usernameList):
    holder = []
    for username in usernameList:    
        tempUsername = username
        if "@" in username:
            tempUsername = tempUsername.replace("@", "", 1)
        mysqldb = pymysql.connect(
            host=db_host, user=db_username, password=db_password, db=db_database)
        mycursor = mysqldb.cursor()
        mysql = "SELECT UserID FROM Users WHERE UserName LIKE '%s'" % tempUsername
        mycursor.execute(mysql)
        t = mycursor.fetchone()
        closeConnection(mysqldb, mycursor)
        if t!=None:
            holder.append(t[0])
    return holder

def getUserIDFromUsername(username):
    mysqldb = pymysql.connect(
            host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT UserID FROM Users WHERE UserName LIKE '%s'" % username
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return t[0]

def updateOrderIDToUserGroupRelational(userID, groupID, orderID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE UserGroupRelational SET Temp_OrderID = '%s' WHERE UserID LIKE '%s' and GroupID LIKE '%s'" % (orderID, userID, groupID)
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    return "User %s in Group %s has OrderID %s" % (userID, groupID, orderID)

def getOrderIDFromUserIDAndGroupID(userID, groupID):
    mysqldb = pymysql.connect(
    host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT Temp_OrderID FROM UserGroupRelational WHERE UserID LIKE '%s' and GroupID LIKE '%s'" % (userID, groupID)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    if t == None:
        return None
    else:
        return t[0]



    

####################################
# Functions for Transactions Table #
####################################

def getAllUsersExceptCreditor(user_id, group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT USERID FROM UserGroupRelational WHERE UserID != %s and GroupID LIKE %s " % (user_id, group_id)
    mycursor.execute(mysql)
    t = mycursor.fetchall()
    closeConnection(mysqldb, mycursor)
    holder=[]
    for user in t:
        holder.append(user[0])
    return holder
    #returns a list
# getAllUsersExceptCreditor(339096917,-524344128)

def getAllUsersFromGroup(group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT USERID FROM UserGroupRelational WHERE GroupID LIKE %s " % (group_id)
    mycursor.execute(mysql)
    t = mycursor.fetchall()
    closeConnection(mysqldb, mycursor)
    holder=[]
    for user in t:
        holder.append(user[0])
    return holder
# 
def getNumberOfUsersExceptCreditor(user_id, group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM UserGroupRelational WHERE UserID != %s and GroupID LIKE %s " % (user_id, group_id)
    mycursor.execute(mysql)
    t = mycursor.fetchall()
    closeConnection(mysqldb, mycursor)
    return len(t)

def addTransaction(input):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    try:
        sql = "INSERT into Transactions(transaction_id, OrderID, AmountOwed, UserID_Creditor, UserID_Debtor, date, last_notified) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (input[0], input[1], input[2], input[3], input[4], input[5], datetime(2010, 1, 1))
        mycursor.execute(sql,val)
        mysqldb.commit()
        closeConnection(mysqldb, mycursor)
        print('Records inserted successfully!')
    except:
        closeConnection(mysqldb, mycursor)
        print("entry already in database")

def markTransactionAsSettled(creditorID, debtorID, orderID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    sql = "UPDATE Transactions SET settled = '1' WHERE UserID_Creditor = '%s' and UserID_Debtor = '%s' and OrderID = '%s'" % (creditorID, debtorID, orderID)
    mycursor.execute(sql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)

def updateTransactionAsSettledWithTransactionID(transactionID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    sql = "UPDATE Transactions SET settled = '1' WHERE Transaction_ID = '%s'" % transactionID
    mycursor.execute(sql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)

def getLastNotifiedTimeFromTransactionID(transactionID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT last_notified FROM Transactions WHERE Transaction_ID LIKE '%s'" % transactionID
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return t[0]



# markTransactionAsSettled(497722299,339096917,'339c6d02-cd33-11eb-8e86-acde48001122')

def markTransactionAsUnsettled(creditorID, debtorID, orderID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    sql = "UPDATE Transactions SET settled = '0' WHERE UserID_Creditor = '%s' and UserID_Debtor = '%s' and OrderID = '%s'" % (creditorID, debtorID, orderID)
    mycursor.execute(sql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)


##############################
# Functions for Orders Table #
##############################

def addOrder(input):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    sql = "INSERT into Orders(OrderID, GroupID, order_name, order_amount, UserID, date) VALUES (%s, %s, %s, %s, %s, %s)"
    val = input
    mycursor.execute(sql,val)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print('Records inserted successfully!')
    return "Order %s has been added" % input[0]

    # except:
    #     closeConnection(mysqldb, mycursor)
    #     print("entry already in database")

def addMessageIDToOrder(orderID, messageID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE Orders SET MessageID = '%s' WHERE OrderID = '%s'" % (messageID, orderID)
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
# addMessageIDToOrder("b4f6a04a-cd13-11eb-a093-acde48001122", str(532))

def setOrderDifferentAmountsFromOrderID(orderID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE Orders SET differentAmounts = '1' WHERE OrderID = '%s'" % (orderID)
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)

def orderIsEvenlySplit(orderID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM Orders WHERE OrderID LIKE '%s' and differentAmounts = '0'" % orderID
    mycursor.execute(mysql)
    closeConnection(mysqldb, mycursor)
    t = mycursor.fetchone()
    return t!=None

def getMessageIDFromOrder(orderID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT MessageID FROM Orders WHERE OrderID LIKE '%s'" % orderID
    mycursor.execute(mysql)
    closeConnection(mysqldb, mycursor)
    t = mycursor.fetchone()
    return t[0]

def getGroupIDFromOrder(orderID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT GroupID FROM Orders WHERE OrderID LIKE '%s'" % orderID
    mycursor.execute(mysql)
    closeConnection(mysqldb, mycursor)
    t = mycursor.fetchone()
    return t[0]

def getOrderNameFromOrderID(orderID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT Order_name FROM Orders WHERE OrderID LIKE '%s'" % orderID
    mycursor.execute(mysql)
    closeConnection(mysqldb, mycursor)
    t = mycursor.fetchone()
    return t[0]

def getOrderDateFromOrderID(orderID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT date FROM Orders WHERE OrderID LIKE '%s'" % orderID
    mycursor.execute(mysql)
    closeConnection(mysqldb, mycursor)
    t = mycursor.fetchone()
    return t[0]

def getOrderIDFromMessageAndGroupID(messageID, groupID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT OrderID FROM Orders WHERE MessageID LIKE '%s' and GroupID LIKE '%s'" % (messageID, groupID)
    mycursor.execute(mysql)
    closeConnection(mysqldb, mycursor)
    t = mycursor.fetchone()
    return t[0]


def getCreditorIDFromMessageAndGroupID(messageID, groupID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT UserID FROM Orders WHERE MessageID LIKE '%s' and GroupID LIKE '%s'" % (messageID, groupID)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    return t[0]

def updateLastNotifiedTimeWithTransactionID(transactionID, newTime):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    sql = "UPDATE Transactions SET last_notified = '%s' WHERE Transaction_ID = '%s'" % (newTime, transactionID)
    print(sql)
    mycursor.execute(sql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)



######################################
# Functions for TelegramGroups Table #
######################################

def addGroup(input):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    # sql = "INSERT into `groups` (`GroupID`, `GroupName`) VALUES " + str((input))
    sql = "INSERT into TelegramGroups (GroupID, GroupName) VALUES (%s, %s)"
    mycursor.execute(sql, input)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print('Group inserted successfully!')
    return "Group %s %s inserted" % (input[1], input[0])

def groupAlreadyAdded(primary_key):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM TelegramGroups WHERE GroupID LIKE %s" % primary_key
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return (t!=None)

def addUserToGroup(userId, groupId):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    sql = "INSERT into UserGroupRelational (UserID, GroupID) VALUES (%s, %s)" % (userId, groupId)
    mycursor.execute(sql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    return "User %s added to Group %s" % (userId, groupId)

def increaseGroupMemberCount(group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    sql = "UPDATE TelegramGroups SET Number_of_members = Number_of_members + 1 WHERE GroupID = %s"
    mycursor.execute(sql, group_id)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)

def decreaseGroupMemberCount(group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    sql = "UPDATE TelegramGroups SET Number_of_members = Number_of_members - 1 WHERE GroupID = %s"
    mycursor.execute(sql, group_id)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)

def userInGroup(userId, groupId):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM UserGroupRelational WHERE UserID LIKE %s and GroupID LIKE %s" % (userId, groupId)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return (t!=None)

def getNumberOfMembers(groupId):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT Number_of_members  FROM  TelegramGroups WHERE  GroupID LIKE %s" % (groupId)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    print("retrieved group number!")
    return t[0]
#retrieveNumber(-583617452)

def getGroupNameFromGroupID(groupID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT GroupName FROM  TelegramGroups WHERE GroupID LIKE %s" % (groupID)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return t[0]

def userIsCreditorForMessage(messageID, groupID, userID):
    orderIDFromOrders = getOrderIDFromMessageAndGroupID(messageID, groupID)
    orderIDFromGroupRelationalTable = getOrderIDFromUserIDAndGroupID(userID, groupID)
    return orderIDFromGroupRelationalTable == orderIDFromOrders

def takeSecond(element):
    return element[1]

def getUnsettledTransactionsForCreditor(creditorID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM transactions WHERE UserID_Creditor LIKE '%s' and settled = '0'" % creditorID
    mycursor.execute(mysql)
    t = mycursor.fetchall()
    closeConnection(mysqldb, mycursor)
    holder=[]
    for transaction in t:
        transactionID = transaction[0]
        orderID = transaction[1]
        amountowed = transaction[3]
        debtorID = transaction[5]
        holder.append((transactionID, orderID, debtorID, amountowed))

    holder.sort(key=takeSecond)
    return holder

def transactionAlreadySettled(transactionID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM Transactions WHERE settled = '1' and Transaction_ID LIKE '%s'" % transactionID
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return (t!=None)

def getUnsettledTransactionsForDebtor(debtorID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM transactions WHERE UserID_Debtor LIKE '%s' and settled = '0'" % debtorID
    mycursor.execute(mysql)
    t = mycursor.fetchall()
    closeConnection(mysqldb, mycursor)
    holder=[]
    for transaction in t:
        transactionID = transaction[0]
        orderID = transaction[1]
        amountowed = transaction[3]
        creditorID = transaction[4]
        holder.append((transactionID, orderID, creditorID, amountowed))

    holder.sort(key=takeSecond)
    return holder

def getCreditorIDFromTransactionID(transactionID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT UserID_Creditor FROM Transactions WHERE Transaction_ID LIKE '%s'" % transactionID
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return t[0]

def getDebtorIDFromTransactionID(transactionID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT UserID_Debtor FROM Transactions WHERE Transaction_ID LIKE '%s'" % transactionID
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return t[0]

def getOrderIDFromTransactionID(transactionID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT OrderID FROM Transactions WHERE Transaction_ID LIKE '%s'" % transactionID
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return t[0]

def getAmountOwedFromTransactionID(transactionID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT AmountOwed FROM Transactions WHERE Transaction_ID LIKE '%s'" % transactionID
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return t[0]

def getTransactionIDFromOrderIDCreditorIDDebtorID(orderID, creditorID, debtorID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT Transaction_ID FROM Transactions WHERE OrderID LIKE '%s' and UserID_Creditor LIKE '%s' and UserID_Debtor LIKE '%s'" % (orderID, creditorID, debtorID)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return t[0]

# print(getUnsettledTransactionsForCreditor(497722299))
