import pymysql
from tabulate import tabulate
from uuid import uuid1
import datetime
import time
import os

from telegram import message

db_host = os.environ['DB_HOST']
db_username = os.environ['DB_USER']
db_database = os.environ['DB_DB']
db_password = os.environ['DB_PASSWORD']


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
    sql = "INSERT into Users (UserID, UserName, notifiable) VALUES (%s, %s, %s)"
    mycursor.execute(sql, input)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print('User added successfully!')

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
    print('test')
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print("User is now in splitall state temporarily!")

def updateUserTempAmount(user_id, group_id, amount):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE UserGroupRelational SET Temp_Amount = %s WHERE UserID LIKE %s and GroupID LIKE %s" % (amount,user_id, group_id)
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print("User amount is updated temporarily!")


def userStateSplitAllEvenly(user_id,group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    #state ='active'
    mysql = "SELECT * FROM UserGroupRelational WHERE UserID LIKE %s and GroupID LIKE %s and State = 'splitallevenly' " % (user_id, group_id)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return (t!=None)

def setUserStateInactive(user_id, group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE usergrouprelational SET State = 'inactive' WHERE UserID = %s and GroupID = %s" % (user_id, group_id)
    mycursor.execute(mysql)
    # t = mycursor.fetchone()
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

def getUserTempAmountSplitAllEvenly(user_id,group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM UserGroupRelational WHERE UserID LIKE %s and GroupID LIKE %s and State = 'splitallevenly' " % (user_id, group_id)
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
    print(holder)
    return holder
    #returns a list
# getAllUsersExceptCreditor(339096917,-524344128)

def getNumberOfUsersExceptCreditor(user_id, group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM UserGroupRelational WHERE UserID != %s and GroupID LIKE %s " % (user_id, group_id)
    mycursor.execute(mysql)
    t = mycursor.fetchall()
    closeConnection(mysqldb, mycursor)
    print(len(t))
    return len(t)

def addTransaction(input):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    try:
        sql = "INSERT into Transactions(transaction_id, OrderID, AmountOwed, UserID_Creditor, UserID_Debtor) VALUES (%s, %s, %s, %s, %s)"
        val = input
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
    sql = "INSERT into Orders(OrderID, GroupID, order_name, order_amount, UserID) VALUES (%s, %s, %s, %s, %s)"
    val = input
    mycursor.execute(sql,val)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print('Records inserted successfully!')

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

def getOrderIDFromMessageAndGroupID(messageID, groupID):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT OrderID FROM Orders WHERE MessageID LIKE '%s' and GroupID LIKE '%s'" % (messageID, groupID)
    mycursor.execute(mysql)
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
    print('User inserted successfully!')

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
