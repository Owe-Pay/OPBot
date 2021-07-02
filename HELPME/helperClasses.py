class OPUser:
    def __init__(self, userID, username, notifiable, firstName):
        self.userID = userID
        self.username = username
        self.notifiable = notifiable
        self.firstName = firstName

class OPGroup:
    def __init__(self, groupID, groupName):
        self.groupID = groupID
        self.groupName = groupName

class OPOrder:
    def __init__(self, orderID, groupID, orderName, orderAmount, userID, date):
        self.orderID = orderID
        self.groupID = groupID
        self.orderName = orderName
        self.orderAmount = orderAmount
        self.userID = userID
        self.date = date

class OPTransaction:
    def __init__(self, transactionID, orderID, amountOwed, creditorID, debtorID, date):
        self.transactionID = transactionID
        self.orderID = orderID
        self.amountOwed = amountOwed
        self.creditorID = creditorID
        self.debtorID = debtorID
        self.date = date
