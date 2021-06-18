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
   
# [User Guide]
   
## Introduction
We at Owe$Pay$ hope to make the tracking payments for ordering of food simple and integrable into Telegram group chats.
In the future, we also hope to create a system to simplify the process of tracking orders and payments in a cohesive app.
We aim to solve two main problems with O$P$. Firstly, we aim to make tracking your debts easy, clean and hassle-free. Secondly, we aim to make the process of chasing after your debtors much more impersonal so you won’t feel as ‘paiseh’ to ask them to return you what is rightfully yours!

## O$P$ Telegram Bot (@OwePay_bot)
One of the main ways we intend to execute our project is through our Telegram Bot. Telegram is one of the most used Instant Messaging Platforms amongst both university students and the world at large today. Hence, we decided that it would be an excellent platform to execute our idea since most friend groups who would typically have a Telegram Group to chat in.

Currently, we have implemented our bot with the ability to create a debt collection order from a user between all other users in the group by going dutch (everyone pays the same amount) as well as the ability for the bot to privately message registered users debt collection orders from their creditors.

Our bot then tracks this order and takes note of who has yet to pay and sends a message to the group with a ‘I Paid!’ button where users can have the option of letting the bot as well as others know that 

Due to the nature of the Telegram Bot API, in order for our bot to send a private message to users, we will require them to have started a private conversation with the bot first. This can be done through the User Setup found below.
   
User Setup
	
   1.Start a private conversation with our bot (@OwePay_bot)
   2.Send the /start command
   3.Click on ‘Register’ to get registered in our database

   

Group Setup
	
   1.Add the bot (@OwePay_bot) to the group
   2.Send the /start@OwePay_bot command
   3.Click on ‘Register’ to get your group registered in our database
   4.Start splitting!

Splitting bills among 
	
   1.Begin your message with the following: @OwePay_bot and an inline message asking you to key in the amount to be split should appear
   2.Key in the amount to be split (currently, only $ is supported) and two popups will appear above the textbox asking you to choose whether you wish to split the bill            evenly among everyone or among some people
   3.Selecting the ‘split among everyone’ option will cause a message to be sent in the group by you detailing the amount to be split and that everyone is partaking
   4.The bot will now prompt you to send in a name for the bill
   5.The next message you send will be registered as the bill’s name
   6.The bot will finally send a message to the group with the total amount, amount to be paid by each person, and a list of people who have yet to pay and below this message     will be a clickable button ‘I paid!’
   7.Other users can click the ‘I paid!’ button in step 6 in order to remove their name from the list.
	
Getting help in a Group
	
   1.Send the /help@OwePay_bot command
   2.The bot will send a list of commands that you can use with our bot as well as detailed instructions on how to use the bot

Getting Help via Private message
	
   1.Send the /help command
   2.The bot will send a list of commands that you can use with our bot as well as detailed instructions on how to use the bot   
   3.To document your work, please start creating a user guide and a developer guide.

# Developer Guide

## Introduction
   
Our project hopes to be extensible and easy for others to collaborate on either by contributing directly to the codebase or providing suggestions by means of comments. In the write-up below, we have detailed how others can develop using the code we’ve already written.

## Setup
   
All of our code can be found on our GitHub. Feel free to leave comments if you feel like there is anything we should work on! In the event that you have yet to install Git on your machine, please look to this guide here for instructions on how to do so.
   
### Telegram Bot
	
The codebase for the Telegram Bot is written in mainly Python and we will require multiple plugins in order to run our bot for development.

#### 1. Install Python
   
	As of time of writing, we’re currently using Python 3.9.5 for development. You can download Python from their official website here. In the event that you are   experiencing difficulties, try to follow this guide here.


![Terminal Window](https://res.cloudinary.com/jianoway/image/upload/v1623863631/elegantTerminal.png)
	
*Figure 1: The elegant Terminal Window*
   
Once you have installed Python, we will be running most of our commands via the Command Line Interface (CLI) to install plugins as well as test our software. For Windows Users, this would be your Command Prompt and for MacOS users this would be your Terminal.

If you are using an older version of Python, please update to Python 3.9.5 as the following instructions are specific to this version. To avoid constant repetition, all text in the courier new font is to be executed via the CLI unless stated otherwise.

#### 2. Cloning of Git Repository

Open a new CLI window and navigate to the parent directory you intend to work in before cloning the Git Repository.
```
git clone https://github.com/Owe-Pay/OPBot.git
```
Navigate to the newly created OPBot directory. You will notice that this folder would already be initialised with the Git commands as it is registered as a Git repository.

#### 3. Install Necessary Plugins
	
Our codebase uses several plugins and we will go over how to install them. 

   1. Pipenv
   
    Pipenv is a tool that automatically creates and maintains a virtual environment for our project to maintain a consistent virtual environment across different machines. If you wish to run the code via you local machine please continue with the installation of other plugins.
    ```
    pip install pipenv
    ```
	
   In the event that the above code does not work for you (especially if you are on Windows, try running any variation of the following code and continue to replace pip with the one that works for you.
	
    ```
    python -m pip install pipenv
    py -m pip install pipenv
    ```
	
   If you are still struggling with installing via pip feel free to contact us via GitHub and we’ll try our best to help you out! :)
	
   2. Python-Telegram-Bot
   
   Python-Telegram-Bot is a wrapper tool that helps us to control and interact with our bot and is the backbone of our bot. Please try to familiarize yourself with it’s API and wrappers as a fundamental understanding of their classes is crucial for developing the codebase for O$P$.
	
    ```
    pip install python-telegram-bot
    ```
	
   3. Logging
   
   Nothing much to say here. Just to create error logs for us to view later on.
	
    ```
	pip install logging
	```
	
   4.Cryptography
	
   This package allows us to conceal certain keys and tokens we wouldn’t want prying eyes to see. It is also a dependency for some of our other packages like python-telegram-bot.
	
   ```
	pip install cryptography
	```

   5.Pytest
	
   A very useful package that forms the backbone of our testing environment
	
   ```
	pip install pytest
	```
	
   6.Flaky
	
   This package helps to rerun Pytest tests for some of the more gimmicky tests that might not pass on the first try.
	
   ```
	pip install flaky
	```
   7.Tabulate
   
   This package helps to make printing of tables prettier. Mostly for aesthetic purposes only.
	
   ```
	pip install tabulate
	```
   8.Pymysql
	
   This package allows us to create MySQL queries with our Python functions in order to access our backend MySQL database.
	
   ```
	pip install pymsysql
	```
   9.os-sys
	
   If for some odd reason you don’t have os-sys installed you can do so as follows. It is crucial for accessing environment variables which I will explain how to set up later.
	
   ```
	pip install os-sys
	```
	
#### 4. MySql
 
To set up MySQL, first go to their official website and download the MySQL installer [here](https://dev.mysql.com/downloads/installer/). As of time of writing, we are using MySQL version 8.0.25. Run the installer and go through the necessary steps. If you encounter any difficulties, please refer to the guide [here](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/).
	
To initialise a local MySQL database on Windows, please follow this guide [here](https://www.microfocus.com/documentation/idol/IDOL_12_0/MediaServer/Guides/html/English/Content/Getting_Started/Configure/_TRN_Set_up_MySQL.html).

To initialise a local MySQL database on MacOS, please follow this guide [here](https://dev.mysql.com/doc/refman/8.0/en/macos-installation-launchd.html).
	
In order to access the MySQL database, install MySQL Workbench from the link here and run the installation setup. After you have successfully set up MySQL Workbench you will be able to access your local MySQL database which would be called localhost if you have already initialised and would be visible in the home page of MySQL Workbench.

Our bot’s backend relies on a Heroku hosted ClearDB MySQL implementation. To access our database you will require a specific API token. Please submit a request to us via GitHub if you would like to have access to our database.

Because of the way ClearDB works, it does not allow us to create new databases to work with and instead we work with the database that is created by default. To optimally set up the MySQL database on your computer, we will be doing it on a new database so as to ensure your default sys database does not get overcrowded.

The video tutorial on how to set up the database can be found [here](https://www.youtube.com/watch?v=tl1O0NVMB2U). Please have MySQL Workbench up and running first though! For clarity’s sake, the command that is run can be found below:
	
``` 
CREATE DATABASE `owepay`
```
	
Please note that the botsql_1.sql file used in the video might be outdated by the time you watch it.   
   
#### 5. .env

After reading some of the code you will realise that there is a reference to os.environ[‘’]. This is because we are accessing environment variables. We have set up the variables to be retrieved on Heroku but for your local machine which should not have access to the Heroku server at all times, you should set up a .env file for your own testing purposes.

First create the .env file. You can use any Integrated Development Environment (IDE) but for the sake of demonstration we will be using Visual Studio Code (VSC).
	
```
   code .env
   ```

Next, you will need to set up the path to the parent of the Git Repository you’re working in. To do this,  in .env include the following in the first line.	
```
   CONFIG_PATH=${HOME}<PATH TO THE PARENT OF THE OPBOT REPOSITORY>
   ```
	
Now we will be declaring the following variables. Do so by including them in the lines after the first.

```
   API_TOKEN=’SOME TOKEN’
   DB_HOST='localhost'
   DB_USER=root
   DB_PASSWORD=<YOUR LOCALHOST PASSWORD>
   DB_DB='owepay'
```
	
The field API_TOKEN is the token that we will be using to connect to the bot. For testing purposes, we have a bot dedicated to it. Please submit a request to us via GitHub if you wish to obtain a copy of the token as it is sensitive. You can also choose to use your own test bot. Instructions on how to make your own Telegram Bot can be found [here](https://core.telegram.org/bots).

The .env file has been added to our .gitignore and will not be tracked by Git so you can rest assured that your personal data will not be uploaded every time you commit a change.

## Testing

#### Testing Methodology 
	
We will be using the pytest framework to design our tests since most of our code is in Python. It is a very flexible testing framework and allows us to design test cases that are specific to our requirements. In pytest, the Stubs used in testing can be called fixtures and are defined before the execution of the test.

We are currently in the process of designing tests for the rest of our functions.
	
#### Design of Tests

The tests designed are hopefully sufficient to catch out all bugs and leave no cases unaccounted for. We will be designing them with the mindset of the trying to capture all possible inputs and how will our functions and system react when given these inputs either directly fed from the User or passed in as a result of another function,
	
#### Unit Testing

Unit Tests would involve testing the functionality of individual functions used in our code so as to ensure that our code is safe and relatively bug-free.

#### Integration Testing

Integration Tests would involve testing whether different parts of our software work together. In our case, we will be testing the interaction between our Telegram Bot and our backend MySQL database.

#### System Testing

System Tests would involve testing whether the system would function properly on day to day usage. In our case, we will be testing whether any bugs arise when the system is subjected to heavy user load among other tests.

##### Testing the *help* function of *owepaybot.py*
	
**Stubs used**
	
test_bot: A bot to simulate the functionality of a Telegram bot without actually running one

userHelpUpdate: An Update object to simulate the Update that is received when the help command is issued by a user via private message

groupHelpUpdate: An Update object to simulate the Update that is received when the help command is issued by a user via group

wrongHelpCommandPrivateUpdate: An Update object to simulate the Update that is received when the help command is issued by a user via private message but the chat_id is invalid

wrongHelpCommandGroupUpdate: An Update object to simulate the Update that is received when the help command is issued by a user via group but the chat_id is invalid

tempContext: A Context object to simulate the functionality of an actual Context object

| Test Name      | Description           | Expected   | Actual   |
| ------------- |:-------------:| -----:| -----:|
| test_help_group | To test if when given the correct Group Update and Context objects as parameters, it will return the correct Message object  | Message.chat_id == 4123123 <br /> Message.text == self.text | ---
 |
| test_help_private    | To test if when given the correct User Update and Context objects as parameters, it will return the correct Message object       |   Message.chat_id == 4123123 <br /> Message.text == self.text|  Message.chat_id == 4123123 <br /> Message.text == self.text |
| test_help_wrong_group_id    | To test if an error is raised when an Group Update is sent from an Invalid chat_id (bot not added to this group, chat_id does not exist)|   BadRequest: Chat not found error caught|  BadRequest: Chat not found error caught |
| 
test_help_wrong_private_id    | To test if an error is raised when an Group Update is sent from an Invalid chat_id (bot has not conversed with user before, user does not exist)|   BadRequest: Chat not found error caught|  BadRequest: Chat not found error caught |


##### Testing the *button* function of *owepaybot.py*
	
**Stubs used**

user_register_callback_query: A Callback Query object that is used to simulate the event when a Callback Query is sent out after the Register button is pressed by a User via private message

user_dont_register_callback_query: A Callback Query object that is used to simulate the event when a Callback Query is sent out after the Don’t Register button is pressed by a User via private message

group_register_callback_query: A Callback Query object that is used to simulate the event when a Callback Query is sent out after the Register button is pressed by a User via group

group_register_callback_query: A Callback Query object that is used to simulate the event when a Callback Query is sent out after the Don’t Register button is pressed by a User via group

tempContext: A Context object to simulate the functionality of an actual Context object

| Test Name      | Description           | Expected   | Actual   |
| ------------- |:-------------:| -----:| -----:|
| test_user_register_callback_query | To test if the correct callback_query is caught when when the User presses the Register button via private message<br />The test for userAlreadyAdded is actually an integration test. | query.data == ‘userRegister’<br /> query.from_user == self.from_user <br /> query.chat_instance == self.chat_instance <br /> query.message == self.private_message <br /> query.inline_message_id == ‘userRegisterInlineMessageID’<br /> userAlreadyAdded(chat_id) <br /> <br /> callback_query.from_user == self.from_user <br /> callback_query.chat_instance == self.chat_instance <br /> callback_query.message == self.private_message <br /> callback_query.inline_message_id == ‘userRegisterInlineMessageID’| query.data == ‘userRegister’ <br /> query.from_user == self.from_user <br /> query.chat_instance == self.chat_instance <br /> query.message == self.private_message <br /> query.inline_message_id == ‘userRegisterInlineMessageID’ <br /> userAlreadyAdded(chat_id) <br /> <br /> callback_query.from_user == self.from_user <br /> callback_query.chat_instance == self.chat_instance <br /> callback_query.message == self.private_message <br /> callback_query.inline_message_id == ‘userRegisterInlineMessageID’|
| test_user_dont_register_callback_query    | To test if the correct callback_query is caught when when the User presses the Don’t Register button via private message <br /> The test for userAlreadyAdded is actually an integration test.|   query.data == ‘userDontRegister’ <br /> query.from_user == self.from_user <br /> query.chat_instance == self.chat_instance <br /> query.message == sel.private_message query.inline_message_id <br /> == ‘userDontRegisterInlineMessageID’ query.data <br /> == ‘userDontRegister’ NOT userAlreadyAdded(chat_id) <br />  <br />  <br /> callback_query.from_user == self.from_user <br /> callback_query.chat_instance == self.chat_instance <br /> callback_query.message == self.private_message <br /> callback_query.inline_message_id == ‘userDontRegisterInlineMessageID’| query.data == ‘userDontRegister’ <br /> query.from_user == self.from_user <br /> query.chat_instance == self.chat_instance <br /> query.message == self.private_message <br /> query.inline_message_id == ‘userDontRegisterInlineMessageID’ <br /> NOT userAlreadyAdded(chat_id)  <br />  <br /> callback_query.from_user == self.from_user <br /> callback_query.chat_instance == self.chat_instance <br /> callback_query.message == self.private_message <br /> callback_query.inline_message_id == ‘userDontRegisterInlineMessageID’
| test_group_register_callback_query | To test if the correct callback_query is caught when when the User presses the Register button in a group. <br /> The test for groupAlreadyAdded is actually an integration test.|query.data == ‘groupRegister’ <br /> query.from_user == self.from_user <br /> query.chat_instance == self.chat_instance <br /> query.message == self.group_message<br /> query.inline_message_id == ‘groupRegisterInlineMessageID’<br /> groupAlreadyAdded(chat_id) <br /> <br /> callback_query.from_user == self.from_user <br /> callback_query.chat_instance == self.chat_instance <br /> callback_query.message == self.group_message<br /> callback_query.inline_message_id == ‘groupRegisterInlineMessageID’| query.data == ‘groupRegister’ <br /> query.from_user == self.from_user <br /> query.chat_instance == self.chat_instance <br /> query.message == self.group_message<br /> query.inline_message_id == ‘groupRegisterInlineMessageID’<br /> groupAlreadyAdded(chat_id) <br /> <br /> callback_query.from_user == self.from_user <br /> callback_query.chat_instance == self.chat_instance <br /> callback_query.message == self.group_message<br /> callback_query.inline_message_id == ‘groupRegisterInlineMessageID’ |query.data == ‘groupRegister’ <br /> query.from_user == self.from_user <br /> query.chat_instance == self.chat_instance <br /> query.message == self.group_message<br /> query.inline_message_id == ‘groupRegisterInlineMessageID’<br /> groupAlreadyAdded(chat_id) <br /> <br /> callback_query.from_user == self.from_user <br /> callback_query.chat_instance == self.chat_instance <br /> callback_query.message == self.group_message<br /> callback_query.inline_message_id == ‘groupRegisterInlineMessageID’
| 
test_group_dont_register_callback_query    | To test if the correct callback_query is caught when when the User presses the Don’t Register button in a group<br /> The test for groupAlreadyAdded is actually an integration test.|   query.data == ‘groupDontRegister’<br /> query.from_user == self.from_user<br /> query.chat_instance == self.chat_instance<br /> query.message == self.group_message<br /> query.inline_message_id == ‘groupDontRegisterInlineMessageID’ NOT groupAlreadyAdded(chat_id)<br /> <br /> callback_query.from_user == self.from_user<br /> callback_query.chat_instance == self.chat_instance<br /> callback_query.message == self.group_message<br /> callback_query.inline_message_id == ‘groupDontRegisterInlineMessageID’|  query.data == ‘groupDontRegister’<br /> query.from_user == self.from_user<br /> query.chat_instance == self.chat_instance<br /> query.message == self.group_message<br /> query.inline_message_id == ‘groupDontRegisterInlineMessageID’ NOT groupAlreadyAdded(chat_id)<br /> <br /> callback_query.from_user == self.from_user<br /> callback_query.chat_instance == self.chat_instance<br /> callback_query.message == self.group_message<br /> callback_query.inline_message_id == ‘groupDontRegisterInlineMessageID’|	





## Prototyping
### O$P$ Mobile Application

We plan to launch a mobile application with similar functionality to our Telegram Bot with certain extensions. You can find a demonstration of what we hope to see from it below.

![sample Login Page](https://res.cloudinary.com/jianoway/image/upload/v1623863754/homepageGif_wtx6xh.gif)
![Sample Home Page](https://res.cloudinary.com/jianoway/image/upload/v1623863761/uiGif_sb9kka.gif)

### Telegram Bot (@OwePay_bot)

Currently, we are hosting our Telegram Bot via Heroku so it should be up 24/7. You can test out it’s features by messaging it directly on Telegram. (@OwePay_bot)


## Software Engineering Principles

As with many other projects, ours utilises Object-Oriented Programming (OOP) to structure and design our code. 

Below you can find some UML diagrams for your reference.
