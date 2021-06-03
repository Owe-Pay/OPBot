# import mysql.connector
import pymysql
from tabulate import tabulate
import datetime
import time
import os

db_host = os.environ['DB_HOST']
db_username = os.environ['DB_USER']
db_database = os.environ['DB_DB']
db_password = os.environ['DB_PASSWORD']

def closeConnection(connection, cursor):
    cursor.close()
    connection.close()
    

def massDelete(table):  # Do note that this mass delete removes everything from a table, but it does not reset the auto-increment value (drop table to reset it)
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mycursor.execute("DELETE FROM " + table)
    mysqldb.commit()
    print('Records updated successfully! Your table is now empty')

# massDelete("users")
#userr is stored as {'id': 497722299 ,'username': 'jianowa',"notifiable": boolean 1}
normalUser1 = ('4997399', 'bear', 1)
normalUser2 = ('487722299', 'apple',0)
normalUser3 = ('477722299', 'donkey',1)


def addUser(input):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    sql = "INSERT into Users (UserID, UserName, notifiable) VALUES (%s, %s, %s)"
    mycursor.execute(sql, input)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print('Records inserted successfully!')

# addUser(normalUser3)

def display_Users():
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT * from users")
    result = mycursor.fetchall()
    closeConnection(mysqldb, mycursor)
    print(tabulate(result, headers=[
        "UserID", "UserName", "notifiable"]))
# display_Users()

def userAlreadyAdded(primary_key):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM Users WHERE UserID LIKE %s" % primary_key
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return (t!=None)

# timing = datetime.datetime.now()
# dt_obj = datetime.datetime.strptime(str(timing), '%Y-%m-%d %H:%M:%S.%f')
# print(dt_obj)

transaction1 =('1288299','123213124','2021-05-29', 10, '497722299', '487722299')

### transaction stored as (transactionid, OrderID, date, AmountOwed, UserID_Creditor, User_id_debitor)
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
        # mysqldb.rollback()


# addTransaction(transaction1)


#################### orders are OrderID, GroupID ###########################
order1 = ('1289923','241414')

def addOrder(input):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    try:
        sql = "INSERT into Orders(OrderID, GroupID) VALUES (%s, %s)"
        val = input
        mycursor.execute(sql,val)
        mysqldb.commit()
        closeConnection(mysqldb, mycursor)
        print('Records inserted successfully!')
    except:
        closeConnection(mysqldb, mycursor)
        print("entry already in database")

        # mysqldb.rollback()
    # mysqldb.close()

# addOrder(order1)


########################## groups are groupid, Number_of_members ###############
group1 = ('24141332', 'TestName')

def addGroup(input):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    # sql = "INSERT into `groups` (`GroupID`, `GroupName`) VALUES " + str((input))
    sql = "INSERT into TelegramGroups (GroupID, GroupName) VALUES (%s, %s)"
    mycursor.execute(sql, input)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)
    print('Records inserted successfully!')

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
    print('Records inserted successfully!')

# def groupMemberAdder(update, context):

# addUserToGroup('2130', '2134')

def increaseGroupMemberCount(group_id):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    sql = "UPDATE TelegramGroups SET Number_of_members = Number_of_members + 1 WHERE GroupID = %s"
    mycursor.execute(sql, group_id)
    mysqldb.commit()
    closeConnection(mysqldb, mycursor)

# increaseGroupMemberCount(-583617452)

def userInGroup(userId, groupId):
    mysqldb = pymysql.connect(
        host=db_host, user=db_username, password=db_password, db=db_database)
    mycursor = mysqldb.cursor()
    mysql = "SELECT * FROM UserGroupRelational WHERE UserID LIKE %s and GroupID LIKE %s" % (userId, groupId)
    mycursor.execute(mysql)
    t = mycursor.fetchone()
    closeConnection(mysqldb, mycursor)
    return (t!=None)

# userInGroup("123","456")
# addGroup(group1)
# addUser(normalUser1)