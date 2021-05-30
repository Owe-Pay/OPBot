import mysql.connector
from tabulate import tabulate
import datetime
import time
import os

db_host = os.environ['DB_HOST']
db_username = os.environ['DB_USER']
db_database = os.environ['DB_DB']
db_password = os.environ['DB_PASSWORD']

##connect to mysql database##
mysqldb = mysql.connector.connect(
    host=db_host, user=db_username, password=db_password, db=db_database)
    # auth_plugin = 'mysql_native_password')

mycursor = mysqldb.cursor()

def massDelete(table):  # Do note that this mass delete removes everything from a table, but it does not reset the auto-increment value (drop table to reset it)
    mycursor.execute("DELETE FROM " + table)
    mysqldb.commit()
    print('Records updated successfully! Your table is now empty')

# massDelete("users")
#userr is stored as {'id': 497722299 ,'username': 'jianowa',"notifiable": boolean 1}
normalUser1 = ('497722299', 'bear', 1)
normalUser2 = ('487722299', 'apple',0)
normalUser3 = ('477722299', 'donkey',1)


def addingUsers(input):
    sql = "INSERT into users(UserID, UserName, notifiable) VALUES (%s, %s, %s)"
    val = input
    mycursor.execute(sql,val)
    mysqldb.commit()
    print('Records inserted successfully!')


# addingUsers(normalUser3)

def display_Users():
    mycursor.execute("SELECT * from users")
    result = mycursor.fetchall()
    print(tabulate(result, headers=[
          "UserID", "UserName", "notifiable"]))
#display_Users

# timing = datetime.datetime.now()
# dt_obj = datetime.datetime.strptime(str(timing), '%Y-%m-%d %H:%M:%S.%f')
# print(dt_obj)

transaction1 =('1288299','123213124','2021-05-29', 10, '497722299', '487722299')
# transaction2=
### transaction stored as (transactionid, OrderID, date, AmountOwed, UserID_Creditor, User_id_debitor)
def addTransaction(input):
    try:
        sql = "INSERT into transactions(transaction_id, OrderID, date, AmountOwed, UserID_Creditor, UserID_Debitor) VALUES (%s, %s, %s, %s, %s, %s)"
        val = input
        mycursor.execute(sql,val)
        mysqldb.commit()
        print('Records inserted successfully!')
    except:
        print("entry already in database")
        # mysqldb.rollback()
    # mysqldb.close()

# addTransaction(transaction1)


#################### orders are OrderID, GroupID ###########################
order1 = ('1289923','241414')

def addOrder(input):
    try:
        sql = "INSERT into orders(OrderID, GroupID) VALUES (%s, %s)"
        val = input
        mycursor.execute(sql,val)
        mysqldb.commit()
        print('Records inserted successfully!')
    except:
        print("entry already in database")
        # mysqldb.rollback()
    # mysqldb.close()

# addOrder(order1)


########################## groups are groupid, Number_of_members ###############
group1=('241414',3)

def addGroup(input):
    try:
        sql = "INSERT into groups(GroupID, Number_of_members) VALUES (%s, %s)"
        val = input
        mycursor.execute(sql,val)
        mysqldb.commit()
        print('Records inserted successfully!')
    except:
        print("entry already in database")
        # mysqldb.rollback()
    # mysqldb.close()

# addGroup(group1)
