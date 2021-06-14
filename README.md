# O$P$

We at Owe$Pay$ hope to make the tracking payments for ordering of food simple and integrable into Telegram group chats.

In the future, we also hope to create a system to simplify the process of tracking orders and payments in a cohesive app.

Track our progress via our GitHub page: https://github.com/Owe-Pay/


# Motivation 

Whenever you’re out with your friends or ordering supper with your hallmates, splitting the bill afterwards can be a hassle. From keeping track of who has yet to pay you back to updating your debts, we can only wish for a system that streamlines this process and is easy and intuitive to use all while being fully customisable.

For us personally, whenever someone orders supper, we will create a list of names and item costs and ask them to pay and remove the names from the list.

This generally clutters the group chat and makes things extremely messy especially when they are multiple orders and people who have not paid for previous orders.

Having a system that integrates with Telegram, a common group messaging platform allows for much higher adoption among users.

Going further, We aim to have a fully fledged app that is able to scan menu entries in receipts that reduces the input of each item manually.

# User Stories

* As the person who usually helps to pay first for food when ordering in deliveries for my hostel mates, I wish I had a way to easily visualise who is in debt with me so that I can manage my finances better.

* As the person who mainly orders food for my hostel level mates, I want presets that accomodate for common additional fees such as Goods and Services Charge (GST) and service charge so that I can add orders without having to manually calculate these common fees for individual items.

* As a student who tags on to food orders, I want to have a system that keeps track of how much I still owe to people and the breakdown of the debt so that I can pay back what I owe easier.

* As a person who goes out to eat with friends , I want a simple system to create new orders to be repaid and update the status of my debts so that I can have an easier time managing multiple debts at once.

* As a person who eats out with friends, I want a system that tracks the food items bought without the need for manually inputting the information so that it is more convenient for myself to create new orders.

* As an existing user of Telegram, I would like the debt calculation to be done on Telegram so that it will integrate with my group chats so that I can manage them seamlessly without having to leave Telegram.

# Development Plan

We have decided to start by implementing our Telegram Bot and our MySQL database to store user information for us to manage and use for our Telegram Bot.

## Requirement Management

With regards to how we will address the requirements to satisfy our User needs, we have split them into two categories: Functional and Non-Functional Requirements

### Functional Requirements

Functional Requirements refer to requirements for our project to work, without which it would be unable to provide it's core functionality.

* User Registration
* Group Registration
* Order Creation with Unique Identification (UID)
* Transaction Creation with UID
* User Notification System
* Historical Data of past Transactions and Orders
* Help function to provide Users with assistance


### Non-Functional Requirements

Non-Functional Requirements refer to requirements that would optimise User experience when using our product.

* Fast response time of bot when issued with commands/messages
* Integrity of User Data stored
* Security of Telegram Bot (API Token)
* 24/7 Availability of Bot
* Mild impact on the Group Chat the Bot is in (Low spam)



## Timeline

You will find our proposed timeline below:

![Timeline](https://res.cloudinary.com/jianoway/image/upload/v1622808447/photo_2021-06-04_20-05-45_dwnjql.jpg)

## Planned Implementation

**Telegram Bot (@OwePay_bot)**

![New User Registration](https://res.cloudinary.com/jianoway/image/upload/v1622368793/O_P_-_First_Time_Registration_Fixed_mdpff8.jpg)
*Figure 1: Registration process for Users and Groups*

* **Registration**
   1. /start will initiate the bot and ask users to register.
   1. Users and groups will have the option of choosing if they wish to register with us in order to give users control over their private data. We have implemented this feature by using Inline Keyboard Buttons that appear under the registration message.
   1. Registration for groups and individuals would be a different process. Using the Telegram Bot API allows us to register groups and individuals separately and we will be able to use a relational database to link users to the groups they belong to.
   1. After Users and Groups are registered, we will store their unique chat_ids in our database 
   1. Due to the nature of Telegram Bots, for our bot to message the user, the user will have had to have messaged our bot first. Hence, to ensure our Notification feature works we will have a column dedicated to keeping track if a registered user is Notifiable.

![New Order Flow](https://res.cloudinary.com/jianoway/image/upload/v1622368925/O_P_-_TeleBot_New_Order_Flow_qfpbtr.jpg)
*Figure 2: Process of creating a new order*

* **Bill Splitting (Partial implementation)**
  1. The bot can be prompted to split bills via an Inline Query from the group that they’re splitting from (e.g @OwePay_bot <Amount to be split>).
  1. After entering the Inline Query, the user will be prompted to choose if they wish to split amongst either everyone in the group or only some people in the group and will also be prompted to input an order name.
  1. Splitting bills will create an Order in the Orders database so each Order is unique and will be associated with the group it was split in.
  1. Splitting with everyone will pull all users in the current group from the group database and split among these users while splitting with some will require the user submitting the Order to manually input all the members who are being split among (To be reconsidered)
  1. Splitting bills will create a Transaction in the Transactions database between the creditor and the debtors which is related to the Order created in c.

![Get Debtors](https://res.cloudinary.com/jianoway/image/upload/v1622368841/O_P_-_TeleBot_Check_Debtors_t9mpw0.jpg)
*Figure 3: Keeping track of creditor’s personal debtors*
   
* **Creditor’s Debtors (To be implemented)**
  1. The bot can retrieve a creditor’s debtors by looking up the respective creditor’s chat_id in the Transactions database where they are the creditor and reply to them with a list of their debtors sorted by their Groups and the respective Order names the Transactions are associated with.
  1. If the creditor does not exist, it prompts the creditor to first register with us. In this case, since the creditor does not exist then it is not possible that our system has records of their transactions and will not return.
  1. After the bot replies to the creditor with the appropriate message listing their debtors, the creditor will have an option to select which debtors to notify or they can also choose to notify all debtors that they have yet to return the creditor their money. After the selection is done, the creditor then sends in the notification request to the bot and the bot will send out a private message to each debtor if they are notifiable.
  1. For debtors who are non-notifiable, the creditor will receive a compiled list of the debtors who the bot had failed to notify along with the respective Transaction details.
  1. Upon receiving the message from their creditor, the debtor will be able to notify their creditor that they have returned the creditor’s money through the bot which will then prompt the bot to send a message to the creditor and also mark the Transaction as settled.
  1. Creditors also have the option to mark the Transaction as settled on their end

![Get Creditors](https://res.cloudinary.com/jianoway/image/upload/v1622368805/O_P_-_TeleBot_Check_Creditors_eo4x8i.jpg)
*Figure 4: Keeping track of debtor’s personal creditors*
   
* **Debtor’s Creditors (To be implemented)**
  1. The bot can retrieve a debtor’s creditors by looking up the respective debtor’s chat_id in the Transactions database where they are the debtor and reply to them with a list of their creditors sorted by their Groups and the respective Order names the Transactions are associated with.
     1. If the debtor does not exist, it prompts the debtor to first register with us. In this case, since the creditor does not exist then it is not possible that our system has records of their transactions and will not return.
  1. After the bot replies to the debtor with the appropriate message listing their creditors, the debtor will have an option to select which creditor to notify or they can also choose to notify all debtors that they have successfully returned the creditor their money. After the selection is done, the creditor then sends in the notification request to the bot and the bot will send out a private message to each creditor if they are notifiable.
     1. For creditors who are non-notifiable, the debtor will receive a compiled list of the creditors who the bot had failed to notify along with the respective Transaction details.
  1. Debtors also have the option to mark the Transaction as settled and will notify the respective creditor so as to ensure that the debtor and creditor are both aware that the Transaction has been settled.

* Help command
  1. Replies users with a list of commands that can be used with the bot.
  1. Provides instructions to users on how to split bills.

## MySQL Setup
   
![SQL Flow](https://res.cloudinary.com/jianoway/image/upload/v1622380661/Screenshot_2021-05-30_at_9.17.34_PM_nccz5l.png)
This is a ER diagram displaying how our data will be stored.
Each transaction would be any exchange of money between 2 users 
Each order can consist of multiple transactions. 
Each group will consist of the total orders in the group. The group will be the telegram groupid

Our backend will be connected to the frontend using python
   
# Guides

We have created various guides for both Users and Developers alike with more information about our project. Please find the links below
   
### Markup: [User Guide](https://docs.google.com/document/d/1n1MOoQ7HTdIDqTgsoM7VEKqg6ebAI9tZ-y9crIS0ixQ/edit?usp=sharing)

### Markup: [Developer Guide](https://docs.google.com/document/d/1Zui7Zxd-1HufvyI80Nt83oNwH6zRincBDQME49KKnjI/edit?usp=sharing)



