


# O$P$

We at Owe$Pay$ hope to make the tracking payments for ordering of food simple and integrable into Telegram group chats.

In the future, we also hope to create a system to simplify the process of tracking orders and payments in a cohesive app.

Track our progress via our GitHub page: https://github.com/Owe-Pay/

# Table of contents
- [Motivation](#motivation)
- [User Stories](#user-stories)
- [Development Plan](#development-plan)
  - [Requirement Management](#requirement-management)
    - [Functional Requirements](#functional-requirements)
    - [Non-Functional Requirements](#non-functional-requirements)
  - [Timeline](#timeline)
  - [Planned Implementation](#planned-implementation)
  - [MySQL Setup](#mysql-setup)
- [Guides](#guides)
  - [User Guide](#user-guide)
    - [O$P$ Telegram Bot (@OwePay_bot)](#op-telegram-bot-owepay_bot)
        - [User Setup](#user-setup)
        - [Group Setup](#group-setup)
        - [Splitting bills](#splitting-bills)
        - [Checking your Debtors](#checking-your-debtors)
        - [Checking your Creditors](#checking-your-creditors)
        - [Getting Help in a Group](#getting-help-in-a-group)
        - [Getting Help via Private message](#getting-help-via-private-message)
  - [Developer Guide](#developer-guide)
    - [Setup](#setup)
      - [Telegram Bot](#telegram-bot)
        - [1. Install Python](#1-install-python)
        - [2. Cloning of Git Repository](#2-cloning-of-git-repository)
        - [3. Install Necessary Plugins](#3-install-necessary-plugins)
        - [4. MySQL](#4-mysql)
        - [5. .env](#5-env)
    - [Testing](#testing)
        - [Design of Tests](#design-of-tests)
        - [Unit Testing](#unit-testing)
          - [Testing the *startPrivate* function of *owepaybot.py*](#testing-the-startprivate-function-of-owepaybotpy)
          - [Testing the *startGroup* function of *owepaybot.py*](#testing-the-startgroup-function-of-owepaybotpy)
          - [Testing the *help* function of *owepaybot.py*](#testing-the-help-function-of-owepaybotpy)
          - [Testing the *button* function of *owepaybot.py*](#testing-the-button-function-of-owepaybotpy)
          - [Testing the *messageContains* functions of *owepaybot.py*](#testing-the-messagecontainssplitevenly-and-messagecontainssplitunevenly-functions-of-owepaybotpy)
          - [Testing the *splitUnevenlyOrderNameCatcher* function of *owepaybot.py*](#testing-the-splitunevenlyordernamecatcher-function-of-owepaybotpy)
          - [Testing the *splitEvenlyKeyboardMarkup* function of *HELPME/helperFunctions.py*](#testing-the-splitevenlykeyboardmarkup-function-of-helpmehelperfunctionspy)
          - [Testing the *splitUnevenlyKeyboardMarkup* function of *HELPME/helperFunctions.py*](#testing-the-splitunevenlykeyboardmarkup-function-of-helpmehelperfunctionspy)
        - [Integration Testing](#integration-testing)
           - [Testing the *groupMemberScanner* function of *owepaybot.py*](#testing-the-groupmemberscanner-function-of-owepaybotpy)
           - [Testing the *waitingForSomeNames* function of *owepaybot.py*](#testing-the-waitingforsomenames-function-of-owepaybotpy)
           - [Testing the *getCreditors* function of *owepaybot.py*](#testing-the-getcreditors-function-of-owepaybotpy)
           - [Testing the *getDebtors* function of *owepaybot.py*](#testing-the-getdebtors-function-of-owepaybotpy)
           - [Testing the *catchOrderFromUpdate* function of *owepaybot.py*](#testing-the-catchorderfromupdate-function-of-owepaybotpy)
        - [System Testing](#system-testing)
           - [Testing *Start Command* via Private Message](#testing-start-command-via-private-message)
           - [Testing *Start Command* via Group Message](#testing-start-command-via-group-message)
           - [Testing *help Command*](#testing-help-command)
           - [Testing Inline Query](#testing-inline-query)
           - [Testing Order Formatting](#testing-order-formatting)
    - [Prototyping](#prototyping)
      - [O$P$ Mobile Application](#op-mobile-application)
      - [Telegram Bot (@OwePay_bot)](#telegram-bot-owepay_bot)
    - [Software Engineering Principles](#software-engineering-principles)


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

![New Order Flow](https://res.cloudinary.com/jianoway/image/upload/v1624865774/Untitled_Diagram_1_coovfs.jpg)
*Figure 2: Process of creating a new order*

* **Bill Splitting**
  1. Bill spliting can be done via an Inline Query from the group that they're splitting the bill from. (e.g <@OwePay_bot 123> would prompt the bot to recognise that the user is attempting to split a bill of $123.00.
  1. After recognising the user's intentions, the bot will prompt the user to choose if they wish to split the bill evenly or unevenly through means of the Inline Query Result Article.
  1. The process flow can be seen from the flowchart above (Fig. 2), with the users being able to add users to the split throguh means of an Inline Keyboard Button. 
  1. The 'Split Evenly' function asks for the users to add the people involved in the bill only once while the 'Split Unevenly' will have the additional step of requesting the user for the list of items to split before asking the user to add the people paying for each item.
  1. Splitting bills will create an Order in the Orders database such that each order is unique and will be able to be tracked through its unique ID.
  1. After the Order is created, for each user that owes the creditor for the bill being split, a unique Transaction is created between the debtor and the creditor in the Transactions database and will be linked back to the Order it was created from.

![Get Debtors](https://res.cloudinary.com/jianoway/image/upload/v1622368841/O_P_-_TeleBot_Check_Debtors_t9mpw0.jpg)
*Figure 3: Keeping track of creditor’s personal debtors*
   
* **Creditor’s Debtors**
  1. The bot can retrieve a creditor’s debtors by looking up the respective creditor’s chat_id in the Transactions database where they are the creditor and reply to them with a list of their debtors sorted by their associated Order.
  1. If the creditor does not exist, it prompts the creditor to first register with us. In this case, since the creditor does not exist then it is not possible that our system has records of their transactions and will not return.
  1. After the bot replies to the creditor with the appropriate message listing their debtors, the creditor will have an option to select which debtors to notify or they can also choose to notify all debtors that they have yet to return the creditor their money. After the selection is done, the creditor then sends in the notification request to the bot and the bot will send out a private message to each debtor if they are notifiable.
  1. For debtors who are non-notifiable, the creditor will receive a compiled list of the debtors who the bot had failed to notify along with the respective Transaction details.
  1. Upon receiving the message from their creditor, the debtor will be able to notify their creditor that they have returned the creditor’s money through the bot which will then prompt the bot to send a message to the creditor and also mark the Transaction as settled.
  1. Creditors also have the option to mark the Transaction as settled on their end

![Get Creditors](https://res.cloudinary.com/jianoway/image/upload/v1622368805/O_P_-_TeleBot_Check_Creditors_eo4x8i.jpg)
*Figure 4: Keeping track of debtor’s personal creditors*
   
* **Debtor’s Creditors**
  1. The bot can retrieve a debtor’s creditors by looking up the respective debtor’s chat_id in the Transactions database where they are the debtor and reply to them with a list of their creditors sorted by their associated Order.
     1. If the debtor does not exist, it prompts the debtor to first register with us. In this case, since the creditor does not exist then it is not possible that our system has records of their transactions and will not return.
  1. After the bot replies to the debtor with the appropriate message listing their creditors, the debtor will have an option to select which creditor to notify or they can also choose to notify all debtors that they have successfully returned the creditor their money. After the selection is done, the creditor then sends in the notification request to the bot and the bot will send out a private message to each creditor if they are notifiable.
     1. For creditors who are non-notifiable, the debtor will receive a compiled list of the creditors who the bot had failed to notify along with the respective Transaction details.
  1. Debtors also have the option to mark the Transaction as settled and will notify the respective creditor so as to ensure that the debtor and creditor are both aware that the Transaction has been settled.

* Help command
  1. Replies users with a list of commands that can be used with the bot.
  1. Provides instructions to users on how to split bills.

## MySQL Setup
   
![SQL Flow](https://res.cloudinary.com/jianoway/image/upload/v1624886060/er_diagram_orbital_zbuphe.jpg)

* Our MySQL Database will be hosted on ClearDB via Heroku and will be interacted with using Pymysql The figure above is the Entity Relationship (ER) diagram representing how our data will be stored.

* Users
   
   * The Users table will be used to store the users whom our bot has interacted with as well as our bot's ability to privately message the User.
   * The Primary Key (PK) we will be using for Users will be the User's unique chat_id provided by Telegram.
   
* TelegramGroups

   * The TelegramGroups table will be used to store the groups that our bot has been added into and will also keep track of the number of users.

   *  The PK we will be using for TelegramGroups will be the Group's unique chat_id provided by Telegram.

* UserGroupRelational
   
   * The UserGroupRelational table will be used to create relationships between Users and TelegramGroups where the table will store which Users are Members of which TelegramGroups.

   *  The PK we will be using for UserGroupRelational will be a combination of PKs' from the respective User and TelegramGroup.

* Orders

   * The Orders table will be used to store the Orders created by Users in their respective Groups.

   * The PK we will be using for Orders will be a UUID generated using the UUID package.

* Transactions

   * The Transactions table will be used to store the Transactiosn associated with the Orders created by Users where it will store the amount owed by the Debtor to the Creditor from that Order.

   * The PK we will be using for Orders will be a UUID generated using the UUID package.
   
# Guides

We have created various guides for both Users and Developers alike with more information about our project. Please find the links below
   
# User Guide


## O$P$ Telegram Bot (@OwePay_bot)
One of the main ways we intend to execute our project is through our Telegram Bot. Telegram is one of the most used Instant Messaging Platforms amongst both university students and the world at large today. Hence, we decided that it would be an excellent platform to execute our idea since most friend groups who would typically have a Telegram Group to chat in.

Currently, we have implemented our bot with the ability to create a debt collection order between a user and other users in the group by either going dutch (everyone pays the same amount) or each item has different people paying for it. It also has the ability to privately message registered users debt collection orders from their creditors.

Our bot then tracks this order and takes note of who has yet to pay and sends a message to the group with a ‘I Paid!’ button where users can have the option of letting the bot as well as others know that 

Due to the nature of the Telegram Bot API, in order for our bot to send a private message to users, we will require them to have started a private conversation with the bot first. This can be done through the User Setup found below.
   
#### User Setup
	
   1. Start a private conversation with our bot (@OwePay_bot)
   
   2. Send the /start command
   
   3. Click on ‘Register’ to get registered in our database

   

#### Group Setup
	
   1. Add the bot (@OwePay_bot) to the group
   
   2. Send the /start@OwePay_bot command
   
   3. Click on ‘Register’ to get your group registered in our database
   
   4. Start splitting!

#### Splitting bills
	
   1. Begin your message with the following: @OwePay_bot and an inline message asking you to key in the amount to be split should appear
   
   2. Key in the amount to be split (currently, only $ is supported) and two popups will appear above the textbox asking you to choose whether you wish to split the bill evenly or unevenly.
   
   3. Splitting Evenly:
   
      1. Selecting the ‘split evenly’ option will cause a message to be sent in the group by you detailing the amount to be split and that it is to be split evenly.
      
      2. The bot will prompt you to send in a name for the bill and the next message you send will be registered as the bill's name.

      3. The bot then send a message to the group with buttons for every user in the group where you can click on their name to add them to the split for the bill.

      4. When you are done selecting the users involved in the bill, press the "Create Order" button to create the bill.
      
      5.  The bot will finally send a message to the group with the total amount, amount to be paid by each person, and a list of people who have yet to pay and below this message will be clickable buttons ‘I've paid!’ and I've not paid!'.
      
      6.  Other users can click the ‘I've paid!’ button in the message from the previous step in order to remove their name from the list.
   
   4. Splitting Unevenly:
      
      1. Selecting the ‘split unevenly’ option will cause a message to be sent in the group by you detailing the amount to be split and that it is to be split unevenly.
      
      2. The bot will prompt you to send in a name for the bill and the next message you send will be registered as the bill's name.
      
      3. The bot will prompt you to send in the items to be split for the bill in the appropriate format and the next message you send will be registered as the item list.
      
      4. The bot will then request for you to send in the send a message to the group with buttons for every user in the group where you can click on their name to add them to the split for each item in the item list you sent in the previous step.
      
      5. When you are done selecting the users involved for each item, you have the option of adding Goods and Services Tax (GST) and/or Service Charge to the bill.
      
      6. After you are done accounting for additional costs, press the "Create Order" button to create the bill.
      
      7. The bot will finally send a message to the group with the total amount and a list of people who have yet to pay with the amount they owe you next to their respective names and below this message will be a clickable button ‘I paid!’.
      
      6.  Other users can click the ‘I paid!’ button in the message from the previous step in order to remove their name from the list.
   
   5. The next message you send will be registered as the bill’s name
   
   6. The bot will finally send a message to the group with the total amount, amount to be paid by each person, and a list of people who have yet to pay and below this message will be clickable buttons ‘I've paid!’ and and I've not paid!'.
   
   7. Other users can click the ‘I've paid!’ button in step 6 in order to remove their name from the list.
	
#### Checking your Debtors

   1. Send the /whoowesme command to @OwePay_bot via private message
   
   2. The bot will send a list of the people who still owe you money organised by the bills they are associated with along with the option next to each person to notify them about the outstanding debt or to settle the debt. Please only press settle if you have guaranteed the bill has been settled.

#### Checking your Creditors
  
   1. Send the /whoomeowes command to @OwePay_bot via private message
   
   2. The bot will send a list of the people whom you still owe money to organised by the bills they are associated with along with the option to settle the debt. Please only press settle if you have guaranteed the bill has been settled.

	
#### Getting Help in a Group
	
   1. Send the /help@OwePay_bot command
   
   2. The bot will send a list of commands that you can use with our bot as well as detailed instructions on how to use the bot

#### Getting Help via Private message
	
   1. Send the /help command
   
   2. The bot will send a list of commands that you can use with our bot as well as detailed instructions on how to use the bot 
   
   3. To document your work, please start creating a user guide and a developer guide.

# Developer Guide

With this developer guide, we hope that collaborating with our project will be something a person with the relevant python skillset will be able to easily start on.

## Setup
   
All of our code can be found on our GitHub. Feel free to leave comments if you feel like there is anything we should work on! In the event that you have yet to install Git on your machine, please look to this guide here for instructions on how to do so.
   
### Telegram Bot
	
The codebase for the Telegram Bot is written in mainly Python and we will require multiple plugins in order to run our bot for development.

### 1. Install Python
   
As of time of writing, we’re currently using Python 3.9.5 for development. You can download Python from their official website here. In the event that you are   experiencing difficulties, try to follow this guide here.

![Terminal Window](https://res.cloudinary.com/jianoway/image/upload/v1623863631/elegantTerminal.png)
	
*Figure 1: The elegant Terminal Window*
   
Once you have installed Python, we will be running most of our commands via the Command Line Interface (CLI) to install plugins as well as test our software. For Windows Users, this would be your Command Prompt and for MacOS users this would be your Terminal.

If you are using an older version of Python, please update to Python 3.9.5 as the following instructions are specific to this version. To avoid constant repetition, all text in the courier new font is to be executed via the CLI unless stated otherwise.

### 2. Cloning of Git Repository

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
	
4. Cryptography
	
   This package allows us to conceal certain keys and tokens we wouldn’t want prying eyes to see. It is also a dependency for some of our other packages like python-telegram-bot.
   ```
   pip install cryptography
   ```

5. Pytest
	
   A very useful package that forms the backbone of our testing environment
	
   ```
   pip install pytest
   ```
	
6. Flaky
	
   This package helps to rerun Pytest tests for some of the more gimmicky tests that might not pass on the first try.
	
   ```
   pip install flaky
   ```
7. Tabulate
   
   This package helps to make printing of tables prettier. Mostly for aesthetic purposes only.	
   ```
   pip install tabulate
   ```
8. Pymysql
	
   This package allows us to create MySQL queries with our Python functions in order to access our backend MySQL database.
	
   ```
   pip install pymsysql
   ```
9. os-sys
	
   If for some odd reason you don’t have os-sys installed you can do so as follows. It is crucial for accessing environment variables which I will explain how to set up later.
	
   ```
   pip install os-sys
   ```
	
### 4. MySQL
 
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

* We will be using the pytest framework to design our tests since most of our code is in Python. It is a very flexible testing framework and allows us to design test cases that are specific to our requirements. In pytest, the Stubs used in testing can be called fixtures and are defined before the execution of the test.

     ![pytest gif](https://res.cloudinary.com/jianoway/image/upload/v1624888464/pytestgif2_jepnlu.gif)|





	


   We are currently in the process of designing tests for the rest of our functions.
	
### Design of Tests

The tests designed are hopefully sufficient to catch out all bugs and leave no cases unaccounted for. We will be designing them with the mindset of the trying to capture all possible inputs and how will our functions and system react when given these inputs either directly fed from the User or passed in as a result of another function,
	
### Unit Testing

Unit Tests would involve testing the functionality of individual functions used in our code so as to ensure that our code is safe and relatively bug-free.

### **Testing the *startPrivate* function of *owepaybot.py***
	
The main purpose of this test is to test the functionality of the /start command in a private message setting.

#### **Stubs used**

* privateUpdate: The Update object passed into the startPrivate function when /start is called by the user

* contextWithMarkup: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_markup)

| Test Name| Description | Expected           | Actual             |
| ---------|-------------| -------------------| -------------------|
| test_startPrivate|To test if given an update, it will be able to respond in the correct chat with the correct message. | Message = startPrivate(privateUpdate, contextWithMarkup)<br /><br />Message.chat_id == 4321234<br /><br />Message.text == self.text<br /><br />Message.reply_markup == InlineKeyboardMarkup(self.keyboard)|Message = startPrivate(privateUpdate, contextWithMarkup)<br /><br />Message.chat_id == 4321234<br /><br />Message.text == self.text<br /><br />Message.reply_markup == InlineKeyboardMarkup(self.keyboard)|
|test_invalid_user_id |To test if receiving an update with an invalid chat_id, it will flag a BadRequest error|BadRequest: Chat not found error caught|BadRequest: Chat not found error caught



### **Testing the *startGroup* function of *owepaybot.py***
	
The main purpose of this test is to test the functionality of the /start command in a group chat setting.

#### **Stubs used**

* groupUpdate: The Update object passed into the startPrivate function when /start is called by the user

* contextWithMarkup: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_markup)

| Test Name        | Description | Expected           | Actual             |
| ---------        |-------------| -------------------| -------------------|
|test_startGroup|To test if given an update, it will be able to respond in the correct chat with the correct message.|Message = startGroup(groupUpdate, contextWithMarkup)<br /><br />Message.chat_id == 4321234 Message.text == self.text<br /><br />Message.reply_markup == InlineKeyboardMarkup(self.keyboard)|Message = startGroup(groupUpdate, contextWithMarkup)<br /><br />Message.chat_id == 4321234 Message.text == self.text<br /><br />Message.reply_markup == InlineKeyboardMarkup(self.keyboard|
|test_invalid_group_id|To test if receiving an update with an invalid chat_id, it will flag a BadRequest error|BadRequest: Chat not found error caught |BadRequest: Chat not found error caught|

### **Testing the *help* function of *owepaybot.py***
	
#### **Stubs used**
	
* test_bot: A bot to simulate the functionality of a Telegram bot without actually running one

* userHelpUpdate: An Update object to simulate the Update that is received when the help command is issued by a user via private message

* groupHelpUpdate: An Update object to simulate the Update that is received when the help command is issued by a user via group

* wrongHelpCommandPrivateUpdate: An Update object to simulate the Update that is received when the help command is issued by a user via private message but the chat_id is invalid

* wrongHelpCommandGroupUpdate: An Update object to simulate the Update that is received when the help command is issued by a user via group but the chat_id is invalid

* tempContext: A Context object to simulate the functionality of an actual Context object

| Test Name       | Description | Expected           | Actual             |
| ---------       |-------------| -------------------| -------------------|
| test_help_group | To test if when given the correct Group Update and Context objects as parameters, it will return the correct Message object  | Message.chat_id == 4123123 <br /> <br /> Message.text == self.text | Message.chat_id == 4123123 <br /> <br />Message.text == self.text|
| test_help_private    | To test if when given the correct User Update and Context objects as parameters, it will return the correct Message object       |   Message.chat_id == 4123123 <br /> <br />Message.text == self.text|  Message.chat_id == 4123123 <br /> <br /> Message.text == self.text |
| test_help_wrong_group_id    | To test if an error is raised when an Group Update is sent from an Invalid chat_id (bot not added to this group, chat_id does not exist)|   BadRequest: Chat not found error caught|  BadRequest: Chat not found error caught |
| test_help_wrong_private_id    | To test if an error is raised when an Group Update is sent from an Invalid chat_id (bot has not conversed with user before, user does not exist)|   BadRequest: Chat not found error caught|  BadRequest: Chat not found error caught |


### Testing the *button* function of *owepaybot.py*
	
#### **Stubs used**

* user_register_callback_query: A Callback Query object that is used to simulate the event when a Callback Query is sent out after the Register button is pressed by a User via private message

* user_dont_register_callback_query: A Callback Query object that is used to simulate the event when a Callback Query is sent out after the Don’t Register button is pressed by a User via private message

* group_register_callback_query: A Callback Query object that is used to simulate the event when a Callback Query is sent out after the Register button is pressed by a User via group

* group_register_callback_query: A Callback Query object that is used to simulate the event when a Callback Query is sent out after the Don’t Register button is pressed by a User via group

* tempContext: A Context object to simulate the functionality of an actual Context object

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
| test_user_register_callback_query | To test if the correct callback_query is caught when when the User presses the Register button via private message<br /><br />The test for userAlreadyAdded is actually an integration test. | query.data == ‘userRegister’<br /><br /> query.from_user == self.from_user <br /><br /> query.chat_instance == self.chat_instance <br /><br /> query.message == self.private_message <br /><br /> query.inline_message_id == ‘userRegisterInlineMessageID’<br /><br /> userAlreadyAdded(chat_id) <br /> <br /> callback_query.from_user == self.from_user <br /> callback_query.chat_instance == self.chat_instance <br /><br /> callback_query.message == self.private_message <br /><br /> callback_query.inline_message_id == ‘userRegisterInlineMessageID’| query.data == ‘userRegister’<br /> <br /> query.from_user == self.from_user <br /> <br />query.chat_instance == self.chat_instance <br /><br /> query.message == self.private_message <br /><br /> query.inline_message_id == ‘userRegisterInlineMessageID’ <br /> <br />userAlreadyAdded(chat_id) <br /> <br /> callback_query.from_user == self.from_user <br /><br /> callback_query.chat_instance == self.chat_instance <br /><br /> callback_query.message == self.private_message <br /> <br />callback_query.inline_message_id == ‘userRegisterInlineMessageID’|
| test_user_dont_register_callback_query    | To test if the correct callback_query is caught when when the User presses the Don’t Register button via private message <br /><br /> The test for userAlreadyAdded is actually an integration test.|   query.data == ‘userDontRegister’ <br /><br /> query.from_user == self.from_user <br /> <br />query.chat_instance == self.chat_instance <br /> query.message == sel.private_message query.inline_message_id <br /> <br />== ‘userDontRegisterInlineMessageID’ <br /><br />query.data == ‘userDontRegister’ NOT userAlreadyAdded(chat_id) <br />  <br />  callback_query.from_user == self.from_user <br /> <br />callback_query.chat_instance == self.chat_instance <br /><br /> callback_query.message == self.private_message <br /> <br />callback_query.inline_message_id == ‘userDontRegisterInlineMessageID’| query.data == ‘userDontRegister’ <br /><br /> query.from_user == self.from_user <br /><br /> query.chat_instance == self.chat_instance <br /> <br />query.message == self.private_message<br /> <br /> query.inline_message_id == ‘userDontRegisterInlineMessageID’ <br /><br /> NOT userAlreadyAdded(chat_id)  <br />  <br /> callback_query.from_user == self.from_user <br /> <br />callback_query.chat_instance == self.chat_instance <br /> <br />callback_query.message == self.private_message <br /> <br />callback_query.inline_message_id == ‘userDontRegisterInlineMessageID’
| test_group_register_callback_query | To test if the correct callback_query is caught when when the User presses the Register button in a group. <br /><br /> The test for groupAlreadyAdded is actually an integration test.|query.data == ‘groupRegister’ <br /> <br />query.from_user == self.from_user <br /><br /> query.chat_instance == self.chat_instance <br /><br /> query.message == self.group_message<br /><br /> query.inline_message_id == ‘groupRegisterInlineMessageID’<br /> <br />groupAlreadyAdded(chat_id) <br /> <br /> callback_query.from_user == self.from_user <br /> c<br />allback_query.chat_instance == self.chat_instance <br /><br /> callback_query.message == self.group_message<br /><br /> callback_query.inline_message_id == ‘groupRegisterInlineMessageID’| query.data == ‘groupRegister’ <br /> <br />query.from_user == self.from_user <br /><br /> query.chat_instance == self.chat_instance <br /> <br />query.message == self.group_message<br /><br /> query.inline_message_id == ‘groupRegisterInlineMessageID’<br /><br /> groupAlreadyAdded(chat_id) <br /> <br /> callback_query.from_user == self.from_user <br /> c<br />allback_query.chat_instance == self.chat_instance <br /><br /> callback_query.message == self.group_message<br /> <br />callback_query.inline_message_id == ‘groupRegisterInlineMessageID’ |query.data == ‘groupRegister’ <br /><br /> query.from_user == self.from_user <br /> <br />query.chat_instance == self.chat_instance <br /><br /> query.message == self.group_message<br /><br /> query.inline_message_id == ‘groupRegisterInlineMessageID’<br /> <br />groupAlreadyAdded(chat_id) <br /> <br /> callback_query.from_user == self.from_user <br /> <br />callback_query.chat_instance == self.chat_instance <br /> <br />callback_query.message == self.group_message<br /> <br />callback_query.inline_message_id == ‘groupRegisterInlineMessageID’
| test_group_dont_register_callback_query    | To test if the correct callback_query is caught when when the User presses the Don’t Register button in a group<br /><br /> The test for groupAlreadyAdded is actually an integration test.|   query.data == ‘groupDontRegister’<br /><br /> query.from_user == self.from_user<br /> <br />query.chat_instance == self.chat_instance<br /><br />query.message == self.group_message<br /> <br />query.inline_message_id == ‘groupDontRegisterInlineMessageID’ NOT groupAlreadyAdded(chat_id)<br /> <br /> callback_query.from_user == self.from_user<br /><br /> callback_query.chat_instance == self.chat_instance<br /> callback_query.message == self.group_message<br /> <br />callback_query.inline_message_id == ‘groupDontRegisterInlineMessageID’|  query.data == ‘groupDontRegister’<br /><br /> query.from_user == self.from_user<br /><br /> query.chat_instance == self.chat_instance<br /> <br />query.message == self.group_message<br /><br /> query.inline_message_id == ‘groupDontRegisterInlineMessageID’ NOT groupAlreadyAdded(chat_id)<br /> <br /> callback_query.from_user == self.from_user<br /> <br />callback_query.chat_instance == self.chat_instance<br /><br /> callback_query.message == self.group_message<br /> <br />callback_query.inline_message_id == ‘groupDontRegisterInlineMessageID’|	


### **Testing the *messageContainsSplitEvenly* and *messageContainsSplitUnevenly* functions of *owepaybot.py***

The main purpose of this test is to test if the two messageContains functions are able to return the expected output

#### **Stubs used**

* containsSplitUnevenlyUpdate: An Update object simulating a user sending a message in a group setting that has text containing the ‘Split unevenly’

* containsSplitEvenlyUpdate: An Update object simulating a user sending a message in a group setting that has text containing the ‘Split evenly

* tempContext: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text)

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|test_messageContainsSplitEvenly|To test if messageContainsSplitEvenly is able to catch the order name from the update and return the correct Message|addGroup((987, 'groupname')) == "Group groupname 987 inserted" <br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted" <br /><br />addUserToGroup(456, 987) == "User 456 added to Group 987" <br /><br />isinstance(messageContainsSplitEvenly(containsSplitEvenlyUpdate, tempContext), Message) <br /><br />messageContainsSplitEvenly(containsSplitEvenlyUpdate, tempContext).chat_id == 987 <br /><br />messageContainsSplitEvenly(containsSplitEvenlyUpdate, tempContext).text == "Hi! Please send the name of the order!" <br /><br />getUserStateFromUserIDAndGroupID(456, 987) == 'splitevenly' <br /><br />getUserTempAmount(456, 987) == 10|addGroup((987, 'groupname')) == "Group groupname 987 inserted" <br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted" <br /><br />addUserToGroup(456, 987) == "User 456 added to Group 987" <br /><br />isinstance(messageContainsSplitEvenly(containsSplitEvenlyUpdate, tempContext), Message) <br /><br />messageContainsSplitEvenly(containsSplitEvenlyUpdate, tempContext).chat_id == 987 <br /><br />messageContainsSplitEvenly(containsSplitEvenlyUpdate, tempContext).text == "Hi! Please send the name of the order!" <br /><br />getUserStateFromUserIDAndGroupID(456, 987) == 'splitevenly' <br /><br />getUserTempAmount(456, 987) == 10|
|test_messageContainsSplitUnevenly|To test if messageContainsSpliUnevenly is able to catch the order name from the update, update the user’s state to ‘splitunevenlywaitingname’ and return the correct Message|addGroup((345, 'groupname')) == "Group groupname 345 inserted" <br /><br />addUser((456, 'userusername', 0,'userfirstname')) == "User 456 inserted" <br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345" <br /><br />isinstance(messageContainsSplitUnevenly(containsSplitUnevenlyUpdate, tempContext), Message) <br /><br />messageContainsSplitUnevenly(containsSplitUnevenlyUpdate, tempContext).chat_id == 345 <br /><br />messageContainsSplitUnevenly(containsSplitUnevenlyUpdate, tempContext).text == "Hi! Please send the name of the order!" <br /><br />getUserStateFromUserIDAndGroupID(456, 345) == 'splitunevenlywaitingname'|addGroup((345, 'groupname')) == "Group groupname 345 inserted" <br /><br />addUser((456, 'userusername', 0,'userfirstname')) == "User 456 inserted" <br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345" <br /><br />isinstance(messageContainsSplitUnevenly(containsSplitUnevenlyUpdate, tempContext), Message) <br /><br />messageContainsSplitUnevenly(containsSplitUnevenlyUpdate, tempContext).chat_id == 345 <br /><br />messageContainsSplitUnevenly(containsSplitUnevenlyUpdate, tempContext).text == "Hi! Please send the name of the order!" <br /><br />getUserStateFromUserIDAndGroupID(456, 345) == 'splitunevenlywaitingname'|

### **Testing the *splitUnevenlyOrderNameCatcher* function of *owepaybot.py***

The main purpose of this test is to test if the splitUnevenlyOrderNameCatcher is able to return the expected Message given a certain orderUpdate

#### **Stubs used**

* orderUpdate: An Update object simulating a user sending a message in a group setting that has text containing the order name

* tempContext: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, reply_to_message_id, text)

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|test_splitUnevenlyOrderNameCatcher|To test if splitUnevenlyOrderNameCatcher correctly catches the order name message, updates the user’s state to the expected state and returns the expected Message|addGroup((345, 'groupname')) == "Group groupname 345 inserted"<br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"<br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345"<br /><br />updateUserTempAmount('456', '345', '123') == "User 456 in Group 345 has the temporary amount 123"<br /><br />isinstance(splitUnevenlyOrderNameCatcher(orderUpdate, tempContext, 456, 345), Message)<br /><br />splitUnevenlyOrderNameCatcher(orderUpdate, tempContext, 456, 345).chat_id == 345<br /><br />userStateSplitUnevenly('456', '345') == True<br /><br />splitUnevenlyOrderNameCatcher(orderUpdate, tempContext, 456, 345).text ==  "Please send in the items in the following format:\nItem Name - Price\n\nFor example:\nChicken Rice - 5\nCurry Chicken - 5.50\nNasi Lemak - 4"|addGroup((345, 'groupname')) == "Group groupname 345 inserted"<br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"<br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345"<br /><br />updateUserTempAmount('456', '345', '123') == "User 456 in Group 345 has the temporary amount 123"<br /><br />isinstance(splitUnevenlyOrderNameCatcher(orderUpdate, tempContext, 456, 345), Message)<br /><br />splitUnevenlyOrderNameCatcher(orderUpdate, tempContext, 456, 345).chat_id == 345<br /><br />userStateSplitUnevenly('456', '345') == True<br /><br />splitUnevenlyOrderNameCatcher(orderUpdate, tempContext, 456, 345).text ==  "Please send in the items in the following format:\nItem Name - Price\n\nFor example:\nChicken Rice - 5\nCurry Chicken - 5.50\nNasi Lemak - 4"|

### **Testing the *splitEvenlyKeyboardMarkup* function of *HELPME/helperFunctions.py***

The main purpose of this test is to test if the splitEvenlyKeyboardMarkup function returns the expected InlineKeyboardMarkup given a certain input.

#### **Stubs used**

* testsplitevenlykeyboardmarkup: A hardcoded version of the expected InlineKeyboardMarkup object with the expected buttons and their respective callback data.

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|test_splitEvenlyKeyboardMarkup|To test the ability for the splitEvenlyKeyboardMarkup function to return the expected InlineKeyboardMarkup object|addGroup((345, 'groupname')) == "Group groupname 345 inserted"<br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"<br /><br />addUser((9871, 'dummyusername1', 0, 'dummyuser1')) == "User 9871 inserted"<br /><br />addUser((9872, 'dummyusername2', 0, 'dummyuser2')) == "User 9872 inserted"<br /><br />addUser((9873, 'dummyusername3', 0, 'dummyuser3')) == "User 9873 inserted”<br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345"<br /><br />addUserToGroup(9871, 345) == "User 9871 added to Group 345"<br /><br />addUserToGroup(9872, 345) == "User 9872 added to Group 345"<br /><br />addUserToGroup(9873, 345) == "User 9873 added to Group 345"<br /><br />splitEvenlyKeyboardMarkup(345) == testsplitevenlykeyboardmarkup|addGroup((345, 'groupname')) == "Group groupname 345 inserted"<br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"<br /><br />addUser((9871, 'dummyusername1', 0, 'dummyuser1')) == "User 9871 inserted"<br /><br />addUser((9872, 'dummyusername2', 0, 'dummyuser2')) == "User 9872 inserted"<br /><br />addUser((9873, 'dummyusername3', 0, 'dummyuser3')) == "User 9873 inserted”<br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345"<br /><br />addUserToGroup(9871, 345) == "User 9871 added to Group 345"<br /><br />addUserToGroup(9872, 345) == "User 9872 added to Group 345"<br /><br />addUserToGroup(9873, 345) == "User 9873 added to Group 345"<br /><br />splitEvenlyKeyboardMarkup(345) == testsplitevenlykeyboardmarkup|

### **Testing the *splitUnevenlyKeyboardMarkup* function of *HELPME/helperFunctions.py***

The main purpose of this test is to test if the splitUnevenlyKeyboardMarkup function returns the expected InlineKeyboardMarkup given a certain input.

#### **Stubs used**

* splitUnevenlyReplyMarkupForTestManual: A hardcoded version of the expected InlineKeyboardMarkup object with the expected buttons and their respective callback data.

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|test_splitUnevenly|To test the ability for the splitUnevenlyKeyboardMarkup function to return the expected InlineKeyboardMarkup object|addGroup((345, 'groupname')) == "Group groupname 345 inserted"<br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"<br /><br />addUser((9871, 'dummyusername1', 0, 'dummyuser1')) == "User 9871 inserted"<br /><br />addUser((9872, 'dummyusername2', 0, 'dummyuser2')) == "User 9872 inserted"<br /><br />addUser((9873, 'dummyusername3', 0, 'dummyuser3')) == "User 9873 inserted”<br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345"<br /><br />addUserToGroup(9871, 345) == "User 9871 added to Group 345"<br /><br />addUserToGroup(9872, 345) == "User 9872 added to Group 345"<br /><br />addUserToGroup(9873, 345) == "User 9873 added to Group 345"<br /><br />splitUnevenlyKeyboardMarkup(345,False) == splitUnevenlyReplyMarkupForTestManual|addGroup((345, 'groupname')) == "Group groupname 345 inserted"<br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"<br /><br />addUser((9871, 'dummyusername1', 0, 'dummyuser1')) == "User 9871 inserted"<br /><br />addUser((9872, 'dummyusername2', 0, 'dummyuser2')) == "User 9872 inserted"<br /><br />addUser((9873, 'dummyusername3', 0, 'dummyuser3')) == "User 9873 inserted”<br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345"<br /><br />addUserToGroup(9871, 345) == "User 9871 added to Group 345"<br /><br />addUserToGroup(9872, 345) == "User 9872 added to Group 345"<br /><br />addUserToGroup(9873, 345) == "User 9873 added to Group 345"<br /><br />splitUnevenlyKeyboardMarkup(345,False) == splitUnevenlyReplyMarkupForTestManual|

### Integration Testing

Integration Tests would involve testing whether different parts of our software work together. In our case, we will be testing the integration of our different functions and how they work together along with the integration of our Telegram Bot and backend MySQL database.

### **Testing the *groupMemberScanner* function of *owepaybot.py***
	
The main purpose of this test is to test the ability of our bot to catch messages in the group setting in for various processes such as catching order names or orders themselves based on the state of the users in the group.

Due to the nature of the groupMemberScanner requiring certain conditions for certain tests to run e.g the group has to already have been added, we will be setting up these test environments within each of the tests before resetting the testing environment before the next test as seen by use of the massDelete function.

#### **Stubs used**

* notAddedUpdate: The update object to simulate the case where a user sends a message into the group

* tempContext: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, **kwargs)

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|test_groupNotAdded|To test if groupMemberScanner can correctly check and return if the group has yet to be added yet.|groupMemberScanner(notAddedUpdate, tempContext) == 'Group with id 1234321 not added'|groupMemberScanner(notAddedUpdate, tempContext) == 'Group with id 1234321 not added'|
|test_userNotAdded|To test if groupMemberScanner can check if the user is not added to the Users database yet when the group has already been added and proceeds to add the user to the database.|addGroup(('1234321', 'group')) == 'Group group 1234321 inserted' <br /><br />userAlreadyAdded(11223344) == True|addGroup(('1234321', 'group')) == 'Group group 1234321 inserted' <br /><br />userAlreadyAdded(11223344) == True|
|test_userNotInGroup|To test if groupMemberScanner will associate a user to the group the message was sent in in the UserGroupRelational table after the message is sent|addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'<br /><br />userInGroup('11223344', '1234321') == True|addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'<br /><br />userInGroup('11223344', '1234321') == True|
test_userStateSplitEvenly|To test if groupMemberScanner will be able to recognise when the user has state ‘splitevenly’|addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'<br /><br />updateUserStateSplitEvenly('11223344', '1234321') == "User 11223344 in Group 1234321 has state 'splitevenly'"<br /><br />updateUserTempAmount('11223344', '1234321', '123') == "User 11223344 in Group 1234321 has the temporary amount 123"<br /><br />groupMemberScanner(notAddedUpdate, tempContext) == "User 11223344 has state 'splitevenly'"|addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'<br /><br />updateUserStateSplitEvenly('11223344', '1234321') == "User 11223344 in Group 1234321 has state 'splitevenly'"<br /><br />updateUserTempAmount('11223344', '1234321', '123') == "User 11223344 in Group 1234321 has the temporary amount 123"<br /><br />groupMemberScanner(notAddedUpdate, tempContext) == "User 11223344 has state 'splitevenly'"|
|test_userStateSplitUnevenly|To test if groupMemberScanner will be able to recognise when the user has state ‘splitunevenly’|addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'<br /><br />updateUserStateSplitUnevenly('11223344', '1234321') == "User 11223344 in Group 1234321 has state 'splitunevenly'"<br /><br />addOrder(('4321', '1234321', 'ordertestname', '123', '11223344', datetime.now())) == "Order 4321 has been added"<br /><br />updateUserTempAmount('11223344', '1234321', '123') == "User 11223344 in Group 1234321 has the temporary amount 123"<br /><br />updateOrderIDToUserGroupRelational('11223344', '1234321', '4321') == "User 11223344 in Group 1234321 has OrderID 4321"<br /><br />groupMemberScanner(notAddedUpdate, tempContext) == "User 11223344 has state 'splitunevenly'"| addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'<br /><br />updateUserStateSplitUnevenly('11223344', '1234321') == "User 11223344 in Group 1234321 has state 'splitunevenly'"<br /><br />addOrder(('4321', '1234321', 'ordertestname', '123', '11223344', datetime.now())) == "Order 4321 has been added"<br /><br />updateUserTempAmount('11223344', '1234321', '123') == "User 11223344 in Group 1234321 has the temporary amount 123"<br /><br />updateOrderIDToUserGroupRelational('11223344', '1234321', '4321') == "User 11223344 in Group 1234321 has OrderID 4321"<br /><br />groupMemberScanner(notAddedUpdate, tempContext) == "User 11223344 has state 'splitunevenly'"|    
|test_userStateSplitUnevenlyWaitingForName|To test if groupMemberScanner will be able to recognise when the user has state ‘splitunevenlywaitingforname’|addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'<br /><br />updateUserStateSplitUnevenlyWaitingForName('11223344', '1234321') == "User 11223344 in Group 1234321 has state 'splitunevenlywaitingname'"<br /><br />groupMemberScanner(notAddedUpdate, tempContext) == "Waiting for User 11223344 in Group 1234321 to send in their Order Name"|addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'<br /><br />updateUserStateSplitUnevenlyWaitingForName('11223344', '1234321') == "User 11223344 in Group 1234321 has state 'splitunevenlywaitingname'"<br /><br />groupMemberScanner(notAddedUpdate, tempContext) == "Waiting for User 11223344 in Group 1234321 to send in their Order Name"|
|test_viabotCheck|To test if groupMemberScanner will be able to recognise if the message was sent via_bot which is a message that is sent with the via_bot tag and that the bot sending the message is itself.m| addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'<br /><br />groupMemberScanner(viaBotUpdate, tempContext) == "Bot found %s" % BOT_ID* <br /><br /> *For security reasons, BOT_ID is left redacted|addGroup(('1234321', 'group')) == 'Group group 1234321 inserted'<br /><br />groupMemberScanner(viaBotUpdate, tempContext) == "Bot found %s" % BOT_ID|

### **Testing the *waitingForSomeNames* function of *owepaybot.py***

The main purpose of this test is to test the ability of our bot to produce the correct message with the correct keyboard markup, with the keyboard markup being constructed using the details of other users in the group.

#### **Stubs used**

* orderUpdate: The update object to simulate the case where a user sends a message into the group containing the order name

* splitEvenlyReplyMarkupTestManual: A InlineKeyboardMarkup object that contains the expected InlineKeyboardButtons with their respective callback data

* tempContext: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_markup) 

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|test_waitingForSomeNames|To test if waitingForSomeNames returns the correct Message object.|addGroup((345, 'groupname')) == "Group groupname 345 inserted"<br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"<br /><br />addUser((9871, 'dummyusername1', 0, 'dummyuser1')) == "User 9871 inserted"<br /><br />addUser((9872, 'dummyusername2', 0, 'dummyuser2')) == "User 9872 inserted"<br /><br />addUser((9873, 'dummyusername3', 0, 'dummyuser3')) == "User 9873 inserted"<br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345"<br /><br />addUserToGroup(9871, 345) == "User 9871 added to Group 345"<br /><br />addUserToGroup(9872, 345) == "User 9872 added to Group 345"<br /><br />addUserToGroup(9873, 345) == "User 9873 added to Group 345"<br /><br />updateUserTempAmount('456', '345', '123') == "User 456 in Group 345 has the temporary amount 123"<br /><br />isinstance(waitingForSomeNames(orderUpdate, tempContext, '456', '345'), Message)<br /><br />waitingForSomeNames(orderUpdate, tempContext, '456', '345').chat_id == 345<br /><br />waitingForSomeNames(orderUpdate, tempContext, '456', '345').text == "People who have your cash money:"<br /><br />waitingForSomeNames(orderUpdate, tempContext, '456', '345').reply_markup == splitEvenlyKeyboardMarkup(345)<br /><br />waitingForSomeNames(orderUpdate, tempContext, '456', '345').reply_markup == splitEvenlyReplyMarkupForTestManual|addGroup((345, 'groupname')) == "Group groupname 345 inserted"<br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"<br /><br />addUser((9871, 'dummyusername1', 0, 'dummyuser1')) == "User 9871 inserted"<br /><br />addUser((9872, 'dummyusername2', 0, 'dummyuser2')) == "User 9872 inserted"<br /><br />addUser((9873, 'dummyusername3', 0, 'dummyuser3')) == "User 9873 inserted"<br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345"<br /><br />addUserToGroup(9871, 345) == "User 9871 added to Group 345"<br /><br />addUserToGroup(9872, 345) == "User 9872 added to Group 345"<br /><br />addUserToGroup(9873, 345) == "User 9873 added to Group 345"<br /><br />updateUserTempAmount('456', '345', '123') == "User 456 in Group 345 has the temporary amount 123"<br /><br />isinstance(waitingForSomeNames(orderUpdate, tempContext, '456', '345'), Message)<br /><br />waitingForSomeNames(orderUpdate, tempContext, '456', '345').chat_id == 345<br /><br />waitingForSomeNames(orderUpdate, tempContext, '456', '345').text == "People who have your cash money:"<br /><br />waitingForSomeNames(orderUpdate, tempContext, '456', '345').reply_markup == splitEvenlyKeyboardMarkup(345)<br /><br />waitingForSomeNames(orderUpdate, tempContext, '456', '345').reply_markup == splitEvenlyReplyMarkupForTestManual|

### **Testing the *getCreditors* function of *owepaybot.py***

The main purpose of this test is to test the ability of our bot to produce the correct message with the correct keyboard markup, with the keyboard markup being constructed using the details of other users in the group.

#### **Stubs used**

* getCreditorUpdate: The update object to simulate the case where a user requests for their list of creditors from the bot in a private message setting

* formattedKeyboardMarkupOfCreditors: The InlineKeyboardMarkup object containing the expected InlineKeyboardButtons and their respective callback data.

* contextNoMarkup: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text)

* contextWithMarkup: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_markup)

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|test_getCreditorsUserNotAdded|To test if getCreditors will return the correct Message given the case that the user has yet to be registered in the Users database.|isinstance(getCreditors(getCreditorUpdate, contextNoMarkup), Message)<br /><br />getCreditors(getCreditorUpdate, contextNoMarkup).chat_id == 1234<br /><br />getCreditors(getCreditorUpdate, contextNoMarkup).text == 'Please register with us first by using /start!'|isinstance(getCreditors(getCreditorUpdate, contextNoMarkup), Message)<br /><br />getCreditors(getCreditorUpdate, contextNoMarkup).chat_id == 1234<br /><br />getCreditors(getCreditorUpdate, contextNoMarkup).text == 'Please register with us first by using /start!'|
|test_getCreditorsNoOneOwes|To test if getCreditors will return the correct Message given the case that the user does not owe anyone any money.|addUser(('1234', 'debtor', 0, 'debtorname')) == "User 1234 inserted"<br /><br />addGroup(('9871', 'groupname')) == "Group groupname 9871 inserted"<br /><br />addUserToGroup('1234', '9871') == "User 1234 added to Group 9871"<br /><br />isinstance(getCreditors(getCreditorUpdate, contextNoMarkup), Message)<br /><br />getCreditors(getCreditorUpdate, contextNoMarkup).chat_id == 1234<br /><br />getCreditors(getCreditorUpdate, contextNoMarkup).text == "Wow! Amazing! You don't owe anyone any money!"|addUser(('1234', 'debtor', 0, 'debtorname')) == "User 1234 inserted"<br /><br />addGroup(('9871', 'groupname')) == "Group groupname 9871 inserted"<br /><br />addUserToGroup('1234', '9871') == "User 1234 added to Group 9871"<br /><br />isinstance(getCreditors(getCreditorUpdate, contextNoMarkup), Message)<br /><br />getCreditors(getCreditorUpdate, contextNoMarkup).chat_id == 1234<br /><br />getCreditors(getCreditorUpdate, contextNoMarkup).text == "Wow! Amazing! You don't owe anyone any money!"|
|test_getCreditors|To test if getCreditors will return the correct Message given the case that the user has outstanding debts with other users.|addUser(('1234', 'debtoruser', 0, 'debtorname')) == "User 1234 inserted"<br /><br />addUser(('4321', 'creditor1', 0, 'creditorname1')) == "User 4321 inserted"<br /><br />addUser(('4322', 'creditor2', 0, 'creditorname2')) == "User 4322 inserted"<br /><br />addUser(('4323', 'creditor3', 0, 'creditorname3')) == "User 4323 inserted"<br /><br />addGroup(('9871', 'groupname')) == "Group groupname 9871 inserted"<br /><br />addUserToGroup('1234', '9871') == "User 1234 added to Group 9871"<br /><br />addUserToGroup('4321', '9871') == "User 4321 added to Group 9871"<br /><br />addUserToGroup('4322', '9871') == "User 4322 added to Group 9871"<br /><br />addUserToGroup('4323', '9871') == "User 4323 added to Group 9871"<br /><br />addOrder(('5432', '9871', 'testOrderName1', '123', '4321', date)) == "Order 5432 has been added"<br /><br />addOrder(('5433', '9871', 'testOrderName2', '123', '4322', date)) == "Order 5433 has been added"<br /><br />addOrder(('5434', '9871', 'testOrderName3', '123', '4323', date)) == "Order 5434 has been added"<br /><br />addTransaction(('2341', '5432', '123', '4321', '1234', date)) == "User 1234 owes User 4321 123"<br /><br />addTransaction(('2342', '5433', '123', '4322', '1234', date)) == "User 1234 owes User 4322 123"<br /><br />addTransaction(('2343', '5434', '123', '4323', '1234', date)) == "User 1234 owes User 4323 123"<br /><br />getUnsettledTransactionsForDebtor('1234') == [('2341', '5432', '4321', 123),('2342', '5433', '4322', 123),('2343', '5434', '4323', 123)]<br /><br />formatTransactionsForDebtorKeyboardMarkup(getUnsettledTransactionsForDebtor('1234')) == formattedKeyboardMarkupOfCreditors<br /><br />isinstance(getCreditors(getCreditorUpdate, contextWithMarkup), Message)<br /><br />getCreditors(getCreditorUpdate, contextWithMarkup).chat_id == 1234<br /><br />getCreditors(getCreditorUpdate, contextWithMarkup).text == "The kind people who you've taken from:"<br /><br />getCreditors(getCreditorUpdate, contextWithMarkup).reply_markup == formattedKeyboardMarkupOfCreditors|addUser(('1234', 'debtoruser', 0, 'debtorname')) == "User 1234 inserted"<br /><br />addUser(('4321', 'creditor1', 0, 'creditorname1')) == "User 4321 inserted"<br /><br />addUser(('4322', 'creditor2', 0, 'creditorname2')) == "User 4322 inserted"<br /><br />addUser(('4323', 'creditor3', 0, 'creditorname3')) == "User 4323 inserted"<br /><br />addGroup(('9871', 'groupname')) == "Group groupname 9871 inserted"<br /><br />addUserToGroup('1234', '9871') == "User 1234 added to Group 9871"<br /><br />addUserToGroup('4321', '9871') == "User 4321 added to Group 9871"<br /><br />addUserToGroup('4322', '9871') == "User 4322 added to Group 9871"<br /><br />addUserToGroup('4323', '9871') == "User 4323 added to Group 9871"<br /><br />addOrder(('5432', '9871', 'testOrderName1', '123', '4321', date)) == "Order 5432 has been added"<br /><br />addOrder(('5433', '9871', 'testOrderName2', '123', '4322', date)) == "Order 5433 has been added"<br /><br />addOrder(('5434', '9871', 'testOrderName3', '123', '4323', date)) == "Order 5434 has been added"<br /><br />addTransaction(('2341', '5432', '123', '4321', '1234', date)) == "User 1234 owes User 4321 123"<br /><br />addTransaction(('2342', '5433', '123', '4322', '1234', date)) == "User 1234 owes User 4322 123"<br /><br />addTransaction(('2343', '5434', '123', '4323', '1234', date)) == "User 1234 owes User 4323 123"<br /><br />getUnsettledTransactionsForDebtor('1234') == [('2341', '5432', '4321', 123),('2342', '5433', '4322', 123),('2343', '5434', '4323', 123)]<br /><br />formatTransactionsForDebtorKeyboardMarkup(getUnsettledTransactionsForDebtor('1234')) == formattedKeyboardMarkupOfCreditors<br /><br />isinstance(getCreditors(getCreditorUpdate, contextWithMarkup), Message)<br /><br />getCreditors(getCreditorUpdate, contextWithMarkup).chat_id == 1234<br /><br />getCreditors(getCreditorUpdate, contextWithMarkup).text == "The kind people who you've taken from:"<br /><br />getCreditors(getCreditorUpdate, contextWithMarkup).reply_markup == formattedKeyboardMarkupOfCreditors|

### **Testing the *getDebtors* function of *owepaybot.py***

The main purpose of this test is to test if the getDebtors is able to return the correct Message given different states of the user and group.

#### **Stubs used**

* getDebtorUpdate: The update object to simulate the case where a user requests for their list of creditors from the bot in a private message setting

* formattedKeyboardMarkupOfDebtors: The InlineKeyboardMarkup object containing the expected InlineKeyboardButtons and their respective callback data.

* contextNoMarkup: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text)

* contextWithMarkup: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_markup)

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|test_getDebtorsUserNotAdded|To test if getDebtors will return the correct Message given the case that the user has yet to be registered in the Users database.|isinstance(getDebtors(getDebtorUpdate, contextNoMarkup), Message)<br /><br />getDebtors(getDebtorUpdate, contextNoMarkup).chat_id == 1234<br /><br />getDebtors(getDebtorUpdate, contextNoMarkup).text == 'Please register with us first by using /start!'|isinstance(getDebtors(getDebtorUpdate, contextNoMarkup), Message)<br /><br />getDebtors(getDebtorUpdate, contextNoMarkup).chat_id == 1234<br /><br />getDebtors(getDebtorUpdate, contextNoMarkup).text == 'Please register with us first by using /start!'|
|test_getDebtorsNoOneOwes|To test if getDebtors will return the correct Message given the case that no one owes the user any money|addUser(('1234', 'creditoruser', 0, 'creditorname')) == "User 1234 inserted"<br /><br />addGroup(('9871', 'groupname')) == "Group groupname 9871 inserted"<br /><br />addUserToGroup('1234', '9871') == "User 1234 added to Group 9871"<br /><br />isinstance(getDebtors(getDebtorUpdate, contextNoMarkup), Message)<br /><br />getDebtors(getDebtorUpdate, contextNoMarkup).chat_id == 1234<br /><br />getDebtors(getDebtorUpdate, contextNoMarkup).text == 'No one owes you money! What great friends you have!!!'|addUser(('1234', 'creditoruser', 0, 'creditorname')) == "User 1234 inserted"<br /><br />addGroup(('9871', 'groupname')) == "Group groupname 9871 inserted"<br /><br />addUserToGroup('1234', '9871') == "User 1234 added to Group 9871"<br /><br />isinstance(getDebtors(getDebtorUpdate, contextNoMarkup), Message)<br /><br />getDebtors(getDebtorUpdate, contextNoMarkup).chat_id == 1234<br /><br />getDebtors(getDebtorUpdate, contextNoMarkup).text == 'No one owes you money! What great friends you have!!!'|
|test_getDebtors|To test if getDebtors will return the correct Message given the case the user has debtors.|addUser(('1234', 'creditoruser', 0, 'creditorname')) == "User 1234 inserted"<br /><br />addUser(('4321', 'debtor1', 0, 'debtorname1')) == "User 4321 inserted"<br /><br />addUser(('4322', 'debtor2', 0, 'debtorname2')) == "User 4322 inserted"<br /><br />addUser(('4323', 'debtor3', 0, 'debtorname3')) == "User 4323 inserted"<br /><br />addGroup(('9871', 'groupname')) == "Group groupname 9871 inserted"<br /><br />addUserToGroup('1234', '9871') == "User 1234 added to Group 9871"<br /><br />addUserToGroup('4321', '9871') == "User 4321 added to Group 9871"<br /><br />addUserToGroup('4322', '9871') == "User 4322 added to Group 9871"<br /><br />addUserToGroup('4323', '9871') == "User 4323 added to Group 9871"<br /><br />addOrder(('5432', '9871', 'testOrderName', '369', '1234', date)) == "Order 5432 has been added"<br /><br />addTransaction(('2341', '5432', '123', '1234', '4321', date)) == "User 4321 owes User 1234 123"<br /><br />addTransaction(('2342', '5432', '123', '1234', '4322', date)) == "User 4322 owes User 1234 123"<br /><br />addTransaction(('2343', '5432', '123', '1234', '4323', date)) == "User 4323 owes User 1234 123"<br /><br />getUnsettledTransactionsForCreditor('1234') == [('2341', '5432', '4321', 123),('2342', '5432', '4322', 123), ('2343', '5432', '4323', 123)]<br /><br />formatTransactionsForCreditorKeyboardMarkup(getUnsettledTransactionsForCreditor('1234')) == formattedKeyboardMarkupOfDebtors<br /><br />isinstance(getDebtors(getDebtorUpdate, contextWithMarkup), Message)<br /><br />getDebtors(getDebtorUpdate, contextWithMarkup).chat_id == 1234<br /><br />getDebtors(getDebtorUpdate, contextWithMarkup).text == 'The baddies who have your cash money! >:(<br />'getDebtors(getDebtorUpdate, contextWithMarkup).reply_markup == formattedKeyboardMarkupOfDebtors|addUser(('1234', 'creditoruser', 0, 'creditorname')) == "User 1234 inserted"<br /><br />addUser(('4321', 'debtor1', 0, 'debtorname1')) == "User 4321 inserted"<br /><br />addUser(('4322', 'debtor2', 0, 'debtorname2')) == "User 4322 inserted"<br /><br />addUser(('4323', 'debtor3', 0, 'debtorname3')) == "User 4323 inserted"<br /><br />addGroup(('9871', 'groupname')) == "Group groupname 9871 inserted"<br /><br />addUserToGroup('1234', '9871') == "User 1234 added to Group 9871"<br /><br />addUserToGroup('4321', '9871') == "User 4321 added to Group 9871"<br /><br />addUserToGroup('4322', '9871') == "User 4322 added to Group 9871"<br /><br />addUserToGroup('4323', '9871') == "User 4323 added to Group 9871"<br /><br />addOrder(('5432', '9871', 'testOrderName', '369', '1234', date)) == "Order 5432 has been added"<br /><br />addTransaction(('2341', '5432', '123', '1234', '4321', date)) == "User 4321 owes User 1234 123"<br /><br />addTransaction(('2342', '5432', '123', '1234', '4322', date)) == "User 4322 owes User 1234 123"<br /><br />addTransaction(('2343', '5432', '123', '1234', '4323', date)) == "User 4323 owes User 1234 123"<br /><br />getUnsettledTransactionsForCreditor('1234') == [('2341', '5432', '4321', 123),('2342', '5432', '4322', 123), ('2343', '5432', '4323', 123)]<br /><br />formatTransactionsForCreditorKeyboardMarkup(getUnsettledTransactionsForCreditor('1234')) == formattedKeyboardMarkupOfDebtors<br /><br />isinstance(getDebtors(getDebtorUpdate, contextWithMarkup), Message)<br /><br />getDebtors(getDebtorUpdate, contextWithMarkup).chat_id == 1234<br /><br />getDebtors(getDebtorUpdate, contextWithMarkup).text == 'The baddies who have your cash money! >:(<br />'getDebtors(getDebtorUpdate, contextWithMarkup).reply_markup == formattedKeyboardMarkupOfDebtors|

### **Testing the *catchOrderFromUpdate* function of *owepaybot.py***

The main purpose of this test is to test if the function catchOrderFromUpdate is able to retrieve the text from an update, create an order in the Orders database and return said Order object

#### **Stubs used**

* orderUpdate: An Update object simulating a user sending a message into the group with the order name

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|test_catchOrderFromUpdate|To test if the expectet Order object is returned given a certain update.|addGroup((345, 'groupname')) == "Group groupname 345 inserted" <br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted" <br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345" <br /><br />updateUserTempAmount('456', '345', '123') == "User 456 in Group 345 has the temporary amount 123" <br /><br />order = catchOrderFromUpdate(orderUpdate) <br /><br />order.creditorID == 456 <br /><br />order.date.replace(tzinfo=None) == getOrderDateFromOrderID(orderID).replace(tzinfo=None) <br /><br />order.groupID == 345 <br /><br />order.orderName == "testOrderName"<br /><br />order.orderAmount == 123|addGroup((345, 'groupname')) == "Group groupname 345 inserted" <br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted" <br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345" <br /><br />updateUserTempAmount('456', '345', '123') == "User 456 in Group 345 has the temporary amount 123" <br /><br />order = catchOrderFromUpdate(orderUpdate) <br /><br />order.creditorID == 456 <br /><br />order.date.replace(tzinfo=None) == getOrderDateFromOrderID(orderID).replace(tzinfo=None) <br /><br />order.groupID == 345 <br /><br />order.orderName == "testOrderName"<br /><br />order.orderAmount == 123|

### **Testing the *splitDifferentAmounts* function of *owepaybot.py***

The main purpose of this test is to test if the splitDifferentAmounts function returns the expected Message object given a certain input

#### **Stubs used**

* orderUpdate: An Update object simulating a user sending a message in a group setting that has text containing the order name

* splitUpdate: An Update object simulating a user sending a message in a group setting that has text containing the list of item*s to split

* splitUnevenlyReplyMarkupForTestUsingFunction: An InlineKeyboardMarkup generated using the HELPME/helperFunctions.splitUnevenlyKeyboardMarkup function

* splitUnevenlyReplyMarkupForTestManual: A hardcoded version of the expected InlineKeyboardMarkup

* nameCatcherContext: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_to_message_id)

* tempContext: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_markup)


| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|test_splitDifferentAmounts|To test if splitDifferentAmounts is able to return the expected Message given a set of conditions where there are multiple users in the group.|addGroup((345, 'groupname')) == "Group groupname 345 inserted"<br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"<br /><br />addUser((9871, 'dummyusername1', 0, 'dummyuser1')) == "User 9871 inserted"<br /><br />addUser((9872, 'dummyusername2', 0, 'dummyuser2')) == "User 9872 inserted"<br /><br />addUser((9873, 'dummyusername3', 0, 'dummyuser3')) == "User 9873 inserted"<br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345"<br /><br />addUserToGroup(9871, 345) == "User 9871 added to Group 345"<br /><br />addUserToGroup(9872, 345) == "User 9872 added to Group 345"<br /><br />addUserToGroup(9873, 345) == "User 9873 added to Group 345"<br /><br />updateUserTempAmount('456', '345', '123') == "User 456 in Group 345 has the temporary amount 123"<br /><br />isinstance(splitUnevenlyOrderNameCatcher(orderUpdate, nameCatcherContext, '456', '345'), Message)<br /><br />isinstance(splitDifferentAmounts(splitUpdate, tempContext, 456, 345), Message)<br /><br />splitDifferentAmounts(splitUpdate, tempContext, 456, 345).text == 'Current split for %s:\n\nItems left to split:%s\n\nPeople paying for %s:' % ('testOrderName', '\nsalad ($10.00)\nfries ($12.00)', 'chicken ($5.00)')<br /><br />splitDifferentAmounts(splitUpdate, tempContext, 456, 345).reply_markup == splitUnevenlyReplyMarkupForTestUsingFunctionsplitDifferentAmounts(splitUpdate, tempContext, 456, 345).reply_markup == splitUnevenlyReplyMarkupForTestManual|addGroup((345, 'groupname')) == "Group groupname 345 inserted"<br /><br />addUser((456, 'userusername', 0, 'userfirstname')) == "User 456 inserted"<br /><br />addUser((9871, 'dummyusername1', 0, 'dummyuser1')) == "User 9871 inserted"<br /><br />addUser((9872, 'dummyusername2', 0, 'dummyuser2')) == "User 9872 inserted"<br /><br />addUser((9873, 'dummyusername3', 0, 'dummyuser3')) == "User 9873 inserted"<br /><br />addUserToGroup(456, 345) == "User 456 added to Group 345"<br /><br />addUserToGroup(9871, 345) == "User 9871 added to Group 345"<br /><br />addUserToGroup(9872, 345) == "User 9872 added to Group 345"<br /><br />addUserToGroup(9873, 345) == "User 9873 added to Group 345"<br /><br />updateUserTempAmount('456', '345', '123') == "User 456 in Group 345 has the temporary amount 123"<br /><br />isinstance(splitUnevenlyOrderNameCatcher(orderUpdate, nameCatcherContext, '456', '345'), Message)<br /><br />isinstance(splitDifferentAmounts(splitUpdate, tempContext, 456, 345), Message)<br /><br />splitDifferentAmounts(splitUpdate, tempContext, 456, 345).text == 'Current split for %s:\n\nItems left to split:%s\n\nPeople paying for %s:' % ('testOrderName', '\nsalad ($10.00)\nfries ($12.00)', 'chicken ($5.00)')<br /><br />splitDifferentAmounts(splitUpdate, tempContext, 456, 345).reply_markup == splitUnevenlyReplyMarkupForTestUsingFunctionsplitDifferentAmounts(splitUpdate, tempContext, 456, 345).reply_markup == splitUnevenlyReplyMarkupForTestManual|


### System Testing

System Tests would involve testing whether the system would function properly on day to day usage. In our case, we will be testing whether any bugs arise when the system is subjected to heavy user load among other tests.

### Testing *start Command* via Private Message

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|/start once| To test basic functionality of the /start command|Bot sends user register message|Bot sends user register message|
|/start twice in a row without registering|To test basic functionality of the /start function given multiple /start inputs|Bot sends user register message after each /start command|Bot sends user register message after each /start command|
|/start once, user presses register button, /start again user presses register button|To test basic functionality of the /start function given multiple /start inputs with registration|Bot sends user register message after first /start command and sends user already registered after second /start command|Bot sends user register message after first /start command and sends user already registered after second /start command|

### Testing *start Command* via Group Message

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|/start once|To test basic functionality of the /start command|Bot sends group register message|Bot sends group register message|
|/start twice in a row without registering|To test basic functionality of the /start function given multiple /start inputs|Bot sends group register message after each /start command| Bot sends group register message after each /start command|
|/start once, user presses register button, /start again user presses register button|To test basic functionality of the /start function given multiple /start inputs with registration|Bot sends group register message after first /start command and sends group already registered after second /start command|Bot sends group register message after first /start command and sends group already registered after second /start command|

### Testing *help Command*

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|/help in group|To test basic functionality of the /help command in groups|Bot sends help message|Bot sends help message|
|/help in private message|To test basic functionality of the /help command in private message|Bot sends help message|Bot sends help message|

### Testing Inline Query

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|@OwePay_bot 123.00|To test if inline queries can handle a standard 2 decimal place float|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|
|@OwePay_bot 0123.00|To test if inline queries can handle a standard 2 decimal place float with an unnecessary 0|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|
|@OwePay_bot 123|To test if inline queries can handle a standard integer|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|
|@OwePay_bot 0123|To test if inline queries can handle a standard integer with an unnecessary 0|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|
|@OwePay_bot 123.00000|To test if inline queries can handle a standard 5 decimal place float|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|
|@OwePay_bot 00123.00912|To test if inline queries can handle a standard 5 decimal place float with rounding and 2 unnecessary 0’s|InlineResultArticles:<br />Split evenly: $123.01<br />Split unevenly: $123.01|InlineResultArticles:<br />Split evenly: $123.01<br />Split unevenly: $123.01|
|@OwePay_bot .112|To test if inline queries can handle standard 3 decimal place float without a number prefixing the period|InlineResultArticles:<br />Split evenly: $0.11<br />Split unevenly: $0.11|InlineResultArticles:<br />Split evenly: $0.11<br />Split unevenly: $0.11|
|@OwePay_bot $123.00|To test if inline queries can handle a standard 2 decimal place float  with $ sign at the front. |InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|
|@OwePay_bot $0123.00|To test if inline queries can handle a standard 2 decimal place float with an unnecessary 0  with $ sign at the front.|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|
|@OwePay_bot $123|To test if inline queries can handle a standard integer  with $ sign at the front.|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|
|@OwePay_bot $0123|To test if inline queries can handle a standard integer with an unnecessary 0  with $ sign at the front.|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|
|@OwePay_bot $123.00000|To test if inline queries can handle a standard 5 decimal place float  with $ sign at the front.|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00|
|@OwePay_bot $00123.00912|To test if inline queries can handle a standard 5 decimal place float with rounding and 2 unnecessary 0’s  with $ sign at the front.|InlineResultArticles:<br />Split evenly: $123.01<br />Split unevenly: $123.01|InlineResultArticles:<br />Split evenly: $123.01<br />Split unevenly: $123.01|
|@OwePay_bot $.112|To test if inline queries can handle standard 3 decimal place float without a number prefixing the period  with $ sign at the front.|InlineResultArticles:<br />Split evenly: $0.11<br />Split unevenly: $0.11|InlineResultArticles:<br />Split evenly: $0.11<br />Split unevenly: $0.11|
|@OwePay_bot $123.10.1|To test if inline queries can recognise invalid amount|InlineResultArticle:<br />$123.10.1 is not a valid amount.|InlineResultArticle:<br />$123.10.1 is not a valid amount.|
|@OwePay_bot 123d|To test if inline queries can recognise invalid amount|InlineResultArticle:<br />123d is not a valid amount.|InlineResultArticle:<br />123d is not a valid amount.|
|@OwePay_bot 123.1d|To test if inline queries can recognise invalid amount|InlineResultArticle:<br />123.1d is not a valid amount.|InlineResultArticle:<br />123.1d is not a valid amount.|
|@OwePay_bot abcd|To test if inline queries can recognise invalid amount|InlineResultArticle:<br />abcd is not a valid amount.|InlineResultArticle:<br />abcd is not a valid amount.|

### Testing Order Formatting

| Test Name | Description | Expected           | Actual             |
| --------- |-------------| -------------------| -------------------|
|Chicken rice - 5<br />Coke - 2|To test if the order list catcher can catch a correct order format|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice- 5<br />Coke- 2|To test if the order list catcher can catch a correct order format with no space between the item names and dashes|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice -5<br />Coke -2|To test if the order list catcher can catch a correct order format with no space between the dash and the item price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice-5<br />Coke-2|To test if the order list catcher can catch a correct order format with no space between the item name and the dash and the item price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice - 5<br />Coke -2|To test if the order list catcher can catch a correct order format with no space between the dash and the item price for one of the items only|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice- 5<br />Coke - 2|To test if the order list catcher can catch a correct order format with no space between the item name and the dash for one of the items only|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice-5<br />Coke - 2|To test if the order list catcher can catch a correct order format with no space between the item name and the dash and the price for one of the items only|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice - $5<br />Coke - $2|To test if the order list catcher can catch a correct order format with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice- $5<br />Coke- $2|To test if the order list catcher can catch a correct order format with no space between the item names and dashes with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice -$5<br />Coke -$2|To test if the order list catcher can catch a correct order format with no space between the dash and the item price with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice-$5<br />Coke-$2|To test if the order list catcher can catch a correct order format with no space between the item name and the dash and the item price with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice - $5<br />Coke -$2|To test if the order list catcher can catch a correct order format with no space between the dash and the item price for one of the items only with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice- $5<br />Coke - $2|To test if the order list catcher can catch a correct order format with no space between the item name and the dash for one of the items only with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice-$5<br />Coke - $2|To test if the order list catcher can catch a correct order format with no space between the item name and the dash and the price for one of the items only with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice - $5<br />Coke - 2|To test if the order list catcher can catch a correct order format with a $ sign in front of one of the prices only|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)|
|Chicken rice -$5Coke - 2|To test if the order list catcher can recognise an invalid syntax and request for user to resend order|Invalid order format, please send again|Invalid order format, please send again|
|Chicken rice - $5Coke - 2<br /><br />Followed by /cancel|To test if the order list catcher can recognise an invalid syntax and request for user to resend order and cancelling the order request will stop the bot from continually prompting for the user to send again|Invalid order format, please send again, bot cancelled|Invalid order format, please send again, bot cancelled|


## Prototyping
### O$P$ Mobile Application

We plan to launch a mobile application with similar functionality to our Telegram Bot with certain extensions. You can find a demonstration of what we hope to see from it below.
| Login Page | Home Page  |
| ---------- | ---------- |
|![sample Login Page](https://res.cloudinary.com/jianoway/image/upload/v1623863754/homepageGif_wtx6xh.gif)|![Sample Home Page](https://res.cloudinary.com/jianoway/image/upload/v1623863761/uiGif_sb9kka.gif)|


### Telegram Bot (@OwePay_bot)

Currently, we are hosting our Telegram Bot via Heroku so it should be up 24/7. You can test out it’s features by messaging it directly on Telegram. (@OwePay_bot)


## Software Engineering Principles

As with many other projects, ours utilises Object-Oriented Programming (OOP) to structure and design our code. 

Below you can find some UML diagrams for your reference.
![UML 1](https://res.cloudinary.com/jianoway/image/upload/v1624114145/startPrivateUMI_h25isz.png)
![UML 1](https://res.cloudinary.com/jianoway/image/upload/v1624114139/startGroup_UML_ncnqol.png)
