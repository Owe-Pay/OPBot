import pymysql
from tabulate import tabulate
from uuid import uuid1
import datetime
import time
import os
#
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
# massDelete("users")
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

#addUser((339096917,"poo_poo_platter",1))


def display_Users():
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

def updateTempState(userId, groupId):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE UserGroupRelational SET State = 'active' WHERE UserID LIKE %s and GroupID LIKE %s" % (userId, groupId)
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print("User is now in splitall state temporarily!")

def updateTempAmount(user_id, group_id, amount):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "UPDATE UserGroupRelational SET Temp_Amount = %s WHERE UserID LIKE %s and GroupID LIKE %s" % (amount,user_id, group_id)
    mycursor.execute(mysql)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print("User amount is updated temporarily!")


def checkstatus(user_id,group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    #state ='active'
    mysql = "SELECT * FROM UserGroupRelational WHERE UserID LIKE %s and GroupID LIKE %s and State = 'active' " % (user_id, group_id)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return (t!=None)


def getamount(user_id,group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    #state ='active'
    mysql = "SELECT * FROM UserGroupRelational WHERE UserID LIKE %s and GroupID LIKE %s and State = 'active' " % (user_id, group_id)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    print(t[2])
    return t[2]
#updateTempAmount(339096917,20)
#catchTempState(339096917,-524344128)
####################################
# Functions for Transactions Table #
####################################

def addTransaction(input):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    try:
        sql = "INSERT into Transactions(transaction_id, OrderID, date, AmountOwed, UserID_Creditor, UserID_Debitor) VALUES (%s, %s, %s, %s, %s, %s)"
        val = input
        mycursor.execute(sql,val)
        mysqldb.commit()
        closeConnection(mysqldb, mycursor)
        print('Records inserted successfully!')
    except:
        closeConnection(mysqldb, mycursor)
        print("entry already in database")

##############################
# Functions for Orders Table #
##############################

def addOrder(input):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    sql = "INSERT into Orders(OrderID, GroupID, order_name, order_amount) VALUES (%s, %s, %s, %s)"
    val = input
    mycursor.execute(sql,val)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print('Records inserted successfully!')

    # except:
    #     closeConnection(mysqldb, mycursor)
    #     print("entry already in database")


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

def retrieveNumberofMembers(groupId):
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
