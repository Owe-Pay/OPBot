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
        - [Scanning Receipts](#scanning-receipts)
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
          - [Testing the *startPrivate* function of *owepaybot.py*](#testing-the-startprivate-function-of-owepaybotpy-)
          - [Testing the *startGroup* function of *owepaybot.py*](#testing-the-startgroup-function-of-owepaybotpy-)
          - [Testing the *help* function of *owepaybot.py*](#testing-the-help-function-of-owepaybotpy-)
          - [Testing the *button* function of *owepaybot.py*](#testing-the-button-function-of-owepaybotpy-)
          - [Testing the *messageContainsNewOrder* functions of *owepaybot.py*](#testing-the-messagecontainsneworder-function-of-owepaybotpy-)
          - [Testing the *splitEvenlyKeyboardMarkup* function of *HELPME/helperFunctions.py*](#testing-the-splitevenlykeyboardmarkup-function-of-helpmehelperfunctionspy-)
          - [Testing the *splitUnevenlyKeyboardMarkup* function of *HELPME/helperFunctions.py*](#testing-the-splitunevenlykeyboardmarkup-function-of-helpmehelperfunctionspy-)
        - [Integration Testing](#integration-testing)
           - [Testing the *groupMemberScanner* function of *owepaybot.py*](#testing-the-groupmemberscanner-function-of-owepaybotpy-)
           - [Testing the *waitingForSomeNames* function of *owepaybot.py*](#testing-the-waitingforsomenames-function-of-owepaybotpy-)
           - [Testing the *getCreditors* function of *owepaybot.py*](#testing-the-getcreditors-function-of-owepaybotpy-)
           - [Testing the *getDebtors* function of *owepaybot.py*](#testing-the-getdebtors-function-of-owepaybotpy-)
           - [Testing the *splitDifferentAmounts* function of *owepaybot.py*](#testing-the-splitdifferentamounts-function-of-owepaybotpy-)
           - [Testing the *newOrderSplitEvenly* function of *owepaybot.py*](#testing-the-newordersplitevenly-function-of-owepaybotpy-)
           - [Testing the *newOrderSplitUnevenly* function of *owepaybot.py*](#testing-the-newordersplitunevenly-function-of-owepaybotpy-)
        - [System Testing](#system-testing)
           - [Testing *Start Command* via Private Message](#testing-start-command-via-private-message)
           - [Testing *Start Command* via Group Message](#testing-start-command-via-group-message)
           - [Testing *help Command*](#testing-help-command)
           - [Testing Inline Query](#testing-inline-query)
           - [Testing Order Formatting](#testing-order-formatting)
    - [Limitations and Constraints]
      - [Cloud Hosting on Heroku](#cloud-hosting-on-heroku)
      - [Scanning of Receipts](#scanning-of-receipts)
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
   
### User Setup

   ![User Setup gif](https://res.cloudinary.com/jianoway/image/upload/v1626965154/user_setup_yksgcl.gif)
   
   1. Start a private conversation with our bot (@OwePay_bot)
   
   2. Send the /start command
   
   3. Click on ‘Register’ to get registered in our database  

### Group Setup
	
   ![Group Setup gif](https://res.cloudinary.com/jianoway/image/upload/v1626865206/group_setup_tl2q9g.gif)
   
   1. Add the bot (@OwePay_bot) to the group
   
   2. Send the /start@OwePay_bot command
   
   3. Click on ‘Register’ to get your group registered in our database
   
   4. Start splitting!

### Splitting bills

| Split Evenly | Split Unevenly|
| ----------   | ----------    |
|<img src="/demos/split evenly cut final.gif?raw=true">| <img src="/demos/split unevenly cut finals.gif?raw=true">)|
	
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
	
### Checking your Debtors

![whoowesme gif](https://res.cloudinary.com/jianoway/image/upload/v1627209292/whoowesme_gif_optz_ilfpbl.gif)

   1. Send the /whoowesme command to @OwePay_bot via private message
   
   2. The bot will send a list of the people who still owe you money organised by the bills they are associated with along with the option next to each person to notify them about the outstanding debt or to settle the debt. Please only press settle if you have guaranteed the bill has been settled.

### Checking your Creditors

![whomeowes gif](https://res.cloudinary.com/jianoway/image/upload/v1627209299/whomeowes_gif_optz_bgimxn.gif)
  
   1. Send the /whoomeowes command to @OwePay_bot via private message
   
   2. The bot will send a list of the people whom you still owe money to organised by the bills they are associated with along with the option to settle the debt. Please only press settle if you have guaranteed the bill has been settled.

	
### Getting Help in a Group
	
   1. Send the /help@OwePay_bot command
   
   2. The bot will send a list of commands that you can use with our bot as well as detailed instructions on how to use the bot

### Getting Help via Private message
	
   1. Send the /help command
   
   2. The bot will send a list of commands that you can use with our bot as well as detailed instructions on how to use the bot 

### Scanning Receipts

![scan receipt gif](https://res.cloudinary.com/jianoway/image/upload/v1627209288/scan_receipt_gif_optz_soldo7.gif)

   In conjunction with our Split Unevenly, our /scanreceipt function is able to help digitise your receipts into a format that you can copy and paste to send our bot when creating unevenly split orders! Unfortunately, our algorithm is rather inaccurate and we are not able to effectively scan receipts :(
   
   1. Send the /scanreceipt command via Private Message
   
   2. The bot will prompt you to send a picture of a receipt
   
   3. Send in the picture of the receipt and the bot will reply with the digitised receipt
   
# Developer Guide

With this developer guide, we hope that collaborating with our project will be something a person with the relevant python skillset will be able to easily start on.

## Setup
   
All of our code can be found on our [GitHub](https://github.com/Owe-Pay/OPBot). Feel free to leave comments if you feel like there is anything we should work on! In the event that you have yet to install Git on your machine, please look to this guide [here](https://github.com/git-guides/install-git) for instructions on how to do so.
   
### Telegram Bot
	
The codebase for the Telegram Bot is written in mainly Python and we will require multiple plugins in order to run our bot for development.

### 1. Install Python
   
As of time of writing, we’re currently using Python 3.9.5 for development. You can download Python from their official website [here](https://www.python.org/downloads/). In the event that you are experiencing difficulties, try to follow this guide [here](https://realpython.com/installing-python).

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

1. [Pipenv](https://pypi.org/project/pipenv/)
   
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
	
2. [Python-Telegram-Bot](https://github.com/python-telegram-bot/python-telegram-bot)
   
   Python-Telegram-Bot is a wrapper tool that helps us to control and interact with our bot and is the backbone of our bot. Please try to familiarize yourself with it’s API and wrappers as a fundamental understanding of their classes is crucial for developing the codebase for O$P$.
   ```
   pip install python-telegram-bot
   ```
	
3. [Logging](https://pypi.org/project/logging/)
   
   Nothing much to say here. Just to create error logs for us to view later on.
   ```
   pip install logging
   ```
	
4. [Cryptography](https://pypi.org/project/cryptography/)
	
   This package allows us to conceal certain keys and tokens we wouldn’t want prying eyes to see. It is also a dependency for some of our other packages like python-telegram-bot.
   ```
   pip install cryptography
   ```

5. [Pytest](https://docs.pytest.org/en/6.2.x/)
	
   A very useful package that forms the backbone of our testing environment
	
   ```
   pip install pytest
   ```
	
6. [Flaky](https://pypi.org/project/flaky/)
	
   This package helps to rerun Pytest tests for some of the more gimmicky tests that might not pass on the first try.
	
   ```
   pip install flaky
   ```
7. [Tabulate](https://pypi.org/project/tabulate/)
   
   This package helps to make printing of tables prettier. Mostly for aesthetic purposes only.	
   ```
   pip install tabulate
   ```
8. [Pymysql](https://pypi.org/project/PyMySQL/)
	
   This package allows us to create MySQL queries with our Python functions in order to access our backend MySQL database.
	
   ```
   pip install pymsysql
   ```
9. [os-sys](https://pypi.org/project/os-sys/)
	
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
	
### **Design of Tests**

The tests designed are hopefully sufficient to catch out all bugs and leave no cases unaccounted for. We will be designing them with the mindset of the trying to capture all possible inputs and how will our functions and system react when given these inputs either directly fed from the User or passed in as a result of another function,
	
### **Unit Testing**

Unit Tests would involve testing the functionality of individual functions used in our code so as to ensure that our code is safe and relatively bug-free.

### **Testing the *startPrivate* function of *owepaybot.py*** 🔬
	
The main purpose of this test is to test the functionality of the /start command in a private message setting.

#### **Stubs used**

* privateUpdate: The Update object passed into the startPrivate function when /start is called by the user

* contextWithMarkup: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_markup)

| Test Case| Expected| Result           | 
| ---------|---------| :---------------:| 
| Using the /start command in a Private Message Setting |The correct /start message for users is displayed. |✅|
| Using the /start command with an invalid user ID |BadRequest: Chat not found error caught.BadRequest: Chat not found error caught|✅|



### **Testing the *startGroup* function of *owepaybot.py*** 🔬
	
The main purpose of this test is to test the functionality of the /start command in a group chat setting.

#### **Stubs used**

* groupUpdate: The Update object passed into the startPrivate function when /start is called by the user

* contextWithMarkup: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_markup)

| Test Case| Expected| Result           | 
| ---------|---------| :---------------:| 
| Using the /start command in a Group Setting |The correct /start message for groups is displayed. |✅|
| Using the /start command with an invalid group ID |BadRequest: Chat not found error caught.BadRequest: Chat not found error caught|✅|

### **Testing the *help* function of *owepaybot.py*** 🔬
	
#### **Stubs used**
	
* test_bot: A bot to simulate the functionality of a Telegram bot without actually running one

* userHelpUpdate: An Update object to simulate the Update that is received when the help command is issued by a user via private message

* groupHelpUpdate: An Update object to simulate the Update that is received when the help command is issued by a user via group

* wrongHelpCommandPrivateUpdate: An Update object to simulate the Update that is received when the help command is issued by a user via private message but the chat_id is invalid

* wrongHelpCommandGroupUpdate: An Update object to simulate the Update that is received when the help command is issued by a user via group but the chat_id is invalid

* tempContext: A Context object to simulate the functionality of an actual Context object

| Test Case       | Expected    | Result|
| ---------       |-------------| :----:|
| Using the /help command in a Group Setting | The correct /help message for groups is displayed. | ✅ |
| Using the /help command in a Private Message Setting | The correct /help message for users is displayed. | ✅ |
| Using the /help command with an invalid group ID   | BadRequest: Chat not found error caught. | ✅ |
| Using the /help command with an invalid user ID | BadRequest: Chat not found error caught. | ✅ |


### **Testing the *button* function of *owepaybot.py*** 🔬
	
#### **Stubs used**

* user_register_callback_query: A Callback Query object that is used to simulate the event when a Callback Query is sent out after the Register button is pressed by a User via private message

* user_dont_register_callback_query: A Callback Query object that is used to simulate the event when a Callback Query is sent out after the Don’t Register button is pressed by a User via private message

* group_register_callback_query: A Callback Query object that is used to simulate the event when a Callback Query is sent out after the Register button is pressed by a User via group

* group_register_callback_query: A Callback Query object that is used to simulate the event when a Callback Query is sent out after the Don’t Register button is pressed by a User via group

* tempContext: A Context object to simulate the functionality of an actual Context object

| Test Case | Expected | Result          |
| --------- |-------------| :----------------:|
| Register button via Private Message| Correct CallbackQuery is caught when the user presses the Register button via Private Message | ✅ | 
| Don't Register button via Private Message | Correct CallbackQuery is caught when the user presses the Don't Register button via Private Message | ✅|
| Register button via Group | Correct CallbackQuery is caught when the user presses the Register button in a Group | ✅ | 
| Don't Register button via Group | Correct CallbackQuery is caught when the user presses the Don't Register button in a Group | ✅|

### **Testing the *messageContainsNewOrder* function of *owepaybot.py*** 🔬

The main purpose of this test is to test if the two messageContains functions are able to return the expected output

#### **Stubs used**

* containsSplitNewOrderUpdate: An Update object simulating a user sending a message in a group setting that has text containing the ‘New Order:’

* tempContext: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text)

| Test Case | Expected | Result          | 
| --------- |-------------| :-----------------:|
| Check if message contains 'New Order:' accurately | Returns a Message | ✅ |
| Correct Message is returned | Text and Message ID is as expected | ✅ |
| User's state is updated | User's state in the UserGroupRelational table is updated to 'neworder' | ✅ |

### **Testing the *splitEvenlyKeyboardMarkup* function of *HELPME/helperFunctions.py*** 🔬

The main purpose of this test is to test if the splitEvenlyKeyboardMarkup function returns the expected InlineKeyboardMarkup given a certain input.

#### **Stubs used**

* testsplitevenlykeyboardmarkup: A hardcoded version of the expected InlineKeyboardMarkup object with the expected buttons and their respective callback data.

| Test Case | Expected | Result          | 
| --------- |-------------| :-----------------:|
| Function returns the expected InlineKeyboardMarkup | The InlineKeyboardMarkup returnes with the expected InlineKeyboardButtons and formatting | ✅ |


### **Testing the *splitUnevenlyKeyboardMarkup* function of *HELPME/helperFunctions.py*** 🔬

The main purpose of this test is to test if the splitUnevenlyKeyboardMarkup function returns the expected InlineKeyboardMarkup given a certain input.

#### **Stubs used**

* splitUnevenlyReplyMarkupForTestManual: A hardcoded version of the expected InlineKeyboardMarkup object with the expected buttons and their respective callback data.

| Test Case | Expected | Result          | 
| --------- |-------------| :-----------------:|
| Function returns the expected InlineKeyboardMarkup | The InlineKeyboardMarkup returnes with the expected InlineKeyboardButtons and formatting | ✅ |

### **Integration Testing**

Integration Tests would involve testing whether different parts of our software work together. In our case, we will be testing the integration of our different functions and how they work together along with the integration of our Telegram Bot and backend MySQL database.

### **Testing the *groupMemberScanner* function of *owepaybot.py*** 🔬
	
The main purpose of this test is to test the ability of our bot to catch messages in the group setting in for various processes such as catching order names or orders themselves based on the state of the users in the group.

Due to the nature of the groupMemberScanner requiring certain conditions for certain tests to run e.g the group has to already have been added, we will be setting up these test environments within each of the tests before resetting the testing environment before the next test as seen by use of the massDelete function.

#### **Stubs used**

* notAddedUpdate: The update object to simulate the case where a user sends a message into the group

* tempContext: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, **kwargs)

| Test Case | Expected | Result          | Remarks |
| --------- |-------------| :-----------------:| --------|
| Group has yet to be added to the database | Returns message for the case when a group has yet to be added | ✅ |
| Group has been added to the database but the user has yet to be added to the database | The user is added to the database and is added to the group in the database| ✅ | Nothing is returned as the user could be issuing a command/starting an order in this messsage |
| Group has been added to the database and user has been added to the database but the user has yet to be added to the group in the database | The user is added to the group in the database | ✅ | Nothing is returned as the user could be issuing a command/starting an order in this messsage |
| User and Group both added completely and User has state 'splitevenly' | Returns the message for when function is executed with user with state 'splitevenly' | ✅ |
| User and Group both added completely and User has state 'splitunevenly' | Returns the message for when function is executed with user with state 'splitunevenly' | ✅ |
| User and Group both added completely and User sends message via a Telegram Bot | Returns the message for when the function is executed with the message being via a Telegram Bot | ✅ | 

### **Testing the *waitingForSomeNames* function of *owepaybot.py*** 🔬

The main purpose of this test is to test the ability of our bot to produce the correct message with the correct keyboard markup, with the keyboard markup being constructed using the details of other users in the group.

#### **Stubs used**

* orderUpdate: The update object to simulate the case where a user sends a message into the group containing the order amount

* splitEvenlyReplyMarkupTestManual: A InlineKeyboardMarkup object that contains the expected InlineKeyboardButtons with their respective callback data

* tempContext: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_markup) 

| Test Case | Expected | Result          | Remarks |
| --------- |-------------| :-----------------:| --------|
| User sends message contain order amount | A Message with the expected InlineKeyboardMarkup, text and Chat ID is returned | ✅ | Due to the Message's InlineKeyboardMarkup depending on the other members of the Telegram Group, we tested both the function to create the ReplyMarkup (splitEvenlyKeyboardarkup) as well as a manual iteration of the InlineKeyboardMarkup| 

### **Testing the *getCreditors* function of *owepaybot.py*** 🔬

The main purpose of this test is to test the ability of our bot to produce the correct message with the correct keyboard markup, with the keyboard markup being constructed using the details of other users in the group.

#### **Stubs used**

* getCreditorUpdate: The update object to simulate the case where a user requests for their list of creditors from the bot in a private message setting

* formattedKeyboardMarkupOfCreditors: The InlineKeyboardMarkup object containing the expected InlineKeyboardButtons and their respective callback data.

* contextNoMarkup: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text)

* contextWithMarkup: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_markup)


| Test Case | Expected | Result          |
| --------- |-------------| :-----------------:|
| User not added to database | User will be sent message prompting them to register with us first | ✅ |
| User is added to database but does not owe anyone money | User will be sent message informing them they aren't in debt with anyone | ✅ |
| User is added to database and owes other users money | The correct Message will be sent to the user with all the User's debts in the InlineKeyboardMarkup | ✅ |

### **Testing the *getDebtors* function of *owepaybot.py*** 🔬

The main purpose of this test is to test if the getDebtors is able to return the correct Message given different states of the user and group.

#### **Stubs used**

* getDebtorUpdate: The update object to simulate the case where a user requests for their list of creditors from the bot in a private message setting

* formattedKeyboardMarkupOfDebtors: The InlineKeyboardMarkup object containing the expected InlineKeyboardButtons and their respective callback data.

* contextNoMarkup: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text)

* contextWithMarkup: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_markup)
Markup: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_markup)


| Test Case | Expected | Result          |
| --------- |-------------| :-----------------:|
| User not added to database | User will be sent message prompting them to register with us first | ✅ |
| User is added to database but is not owed any money | User will be sent message informing them they aren't owed any money| ✅ |
| User is added to database and is owed money by other users | The correct Message will be sent to the user with all the User's credits in the InlineKeyboardMarkup | ✅ |

### **Testing the *splitDifferentAmounts* function of *owepaybot.py*** 🔬

The main purpose of this test is to test if the splitDifferentAmounts function returns the expected Message object given a certain input

#### **Stubs used**

* orderUpdate: An Update object simulating a user sending a message in a group setting that has text containing the order name

* splitUpdate: An Update object simulating a user sending a message in a group setting that has text containing the list of item*s to split

* splitUnevenlyReplyMarkupForTestUsingFunction: An InlineKeyboardMarkup generated using the HELPME/helperFunctions.splitUnevenlyKeyboardMarkup function

* splitUnevenlyReplyMarkupForTestManual: A hardcoded version of the expected InlineKeyboardMarkup

* nameCatcherContext: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_to_message_id)

* tempContext: A Context object to simulate the functionality of an actual Context object with the send_message method that takes in (chat_id, text, reply_markup)

| Test Case | Expected | Result          |
| --------- |-------------| :-----------------:|
| User is splitting unevenly and has sent in the order list | A Message with the expected Text and InlineKeyboardMarkup is returned | ✅ |


### **Testing the *newOrderSplitEvenly* function of *owepaybot.py*** 🔬

The main purpose of this test is to test if the newOrderSplitEvenly is able to return the correct Message and changes the User's state appropriately.

#### **Stubs used**

* orderUpdate: An Update object simulating the Callback Query when the user presses the "Split Evenly" button

* tempContext: A Context object to simulate the functionality of an actual Context object with the editMessageText method that takes in (chat_id, message_id, text)

| Test Case | Expected | Result          |
| --------- |-------------| :-----------------:|
| User presses the Split Evenly button | The bot edits the message to give the correct message asking for the user to send in the order amount as well as the user's state being changed to 'splitevenly'| ✅ |


### **Testing the *newOrderSplitUnevenly* function of *owepaybot.py*** 🔬

The main purpose of this test is to test if the newOrderSplitEvenly is able to return the correct Message and changes the User's state appropriately.

#### **Stubs used**

* orderUpdate: An Update object simulating the Callback Query when the user presses the "Split Unevenly" button

* tempContext: A Context object to simulate the functionality of an actual Context object with the editMessageText method that takes in (chat_id, message_id, text)

| Test Case | Expected | Result          |
| --------- |-------------| :-----------------:|
| User presses the Split Unevenly button | The bot edits the message to give the correct message asking for the user to send in the list of items to be split as well as the user's state being changed to 'splitunevenly'| ✅ |

### System Testing

System Tests would involve testing whether the system would function properly on day to day usage. In our case, we will be testing whether any bugs arise when the system is subjected to heavy user load among other tests.

### Testing *start Command* via Private Message

| Test Case | Description | Expected           | Result             |
| --------- |-------------| -------------------| :-----------------:|
|/start once| To test basic functionality of the /start command|Bot sends user register message| ✅ |
|/start twice in a row without registering|To test basic functionality of the /start function given multiple /start inputs|Bot sends user register message after each /start command| ✅ |
|/start once, user presses register button, /start again user presses register button|To test basic functionality of the /start function given multiple /start inputs with registration|Bot sends user register message after first /start command and sends user already registered after second /start command| ✅ |

### Testing *start Command* via Group Message

| Test Case | Description | Expected           | Result             |
| --------- |-------------| -------------------| :-----------------:|
|/start once|To test basic functionality of the /start command|Bot sends group register message| ✅ |
|/start twice in a row without registering|To test basic functionality of the /start function given multiple /start inputs|Bot sends group register message after each /start command|  ✅ |
|/start once, user presses register button, /start again user presses register button|To test basic functionality of the /start function given multiple /start inputs with registration|Bot sends group register message after first /start command and sends group already registered after second /start command| ✅ |

### Testing *help Command*

| Test Case | Description | Expected           | Result             |
| --------- |-------------| -------------------| :-----------------:|
|/help in group|To test basic functionality of the /help command in groups|Bot sends help message| ✅ |
|/help in private message|To test basic functionality of the /help command in private message|Bot sends help message| ✅ |

### Testing Inline Query

| Test Case | Description | Expected           | Result             |
| --------- |-------------| -------------------| :-------------------:|
|@OwePay_bot 123.00|To test if inline queries can handle a standard 2 decimal place float|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00| ✅ |
|@OwePay_bot 0123.00|To test if inline queries can handle a standard 2 decimal place float with an unnecessary 0|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00| ✅ |
|@OwePay_bot 123|To test if inline queries can handle a standard integer|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00| ✅ |
|@OwePay_bot 0123|To test if inline queries can handle a standard integer with an unnecessary 0|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00| ✅ |
|@OwePay_bot 123.00000|To test if inline queries can handle a standard 5 decimal place float|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00| ✅ |
|@OwePay_bot 00123.00912|To test if inline queries can handle a standard 5 decimal place float with rounding and 2 unnecessary 0’s|InlineResultArticles:<br />Split evenly: $123.01<br />Split unevenly: $123.01| ✅ |
|@OwePay_bot .112|To test if inline queries can handle standard 3 decimal place float without a number prefixing the period|InlineResultArticles:<br />Split evenly: $0.11<br />Split unevenly: $0.11| ✅ |
|@OwePay_bot $123.00|To test if inline queries can handle a standard 2 decimal place float  with $ sign at the front. |InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00| ✅ |
|@OwePay_bot $0123.00|To test if inline queries can handle a standard 2 decimal place float with an unnecessary 0  with $ sign at the front.|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00| ✅ |
|@OwePay_bot $123|To test if inline queries can handle a standard integer  with $ sign at the front.|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00| ✅ |
|@OwePay_bot $0123|To test if inline queries can handle a standard integer with an unnecessary 0  with $ sign at the front.|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00| ✅ |
|@OwePay_bot $123.00000|To test if inline queries can handle a standard 5 decimal place float  with $ sign at the front.|InlineResultArticles:<br />Split evenly: $123.00<br />Split unevenly: $123.00| ✅ |
|@OwePay_bot $00123.00912|To test if inline queries can handle a standard 5 decimal place float with rounding and 2 unnecessary 0’s  with $ sign at the front.|InlineResultArticles:<br />Split evenly: $123.01<br />Split unevenly: $123.01| ✅ |
|@OwePay_bot $.112|To test if inline queries can handle standard 3 decimal place float without a number prefixing the period  with $ sign at the front.|InlineResultArticles:<br />Split evenly: $0.11<br />Split unevenly: $0.11| ✅ |
|@OwePay_bot $123.10.1|To test if inline queries can recognise invalid amount|InlineResultArticle:<br />$123.10.1 is not a valid amount.| ✅ |
|@OwePay_bot 123d|To test if inline queries can recognise invalid amount|InlineResultArticle:<br />123d is not a valid amount.| ✅ |
|@OwePay_bot 123.1d|To test if inline queries can recognise invalid amount|InlineResultArticle:<br />123.1d is not a valid amount.| ✅ |
|@OwePay_bot abcd|To test if inline queries can recognise invalid amount|InlineResultArticle:<br />abcd is not a valid amount.| ✅ |

### Testing Order Formatting

| Test Case | Description | Expected           | Result             |
| --------- |-------------| -------------------| :-------------------:|
|Chicken rice - 5<br />Coke - 2|To test if the order list catcher can catch a correct order format|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice- 5<br />Coke- 2|To test if the order list catcher can catch a correct order format with no space between the item names and dashes|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice -5<br />Coke -2|To test if the order list catcher can catch a correct order format with no space between the dash and the item price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice-5<br />Coke-2|To test if the order list catcher can catch a correct order format with no space between the item name and the dash and the item price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice - 5<br />Coke -2|To test if the order list catcher can catch a correct order format with no space between the dash and the item price for one of the items only|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice- 5<br />Coke - 2|To test if the order list catcher can catch a correct order format with no space between the item name and the dash for one of the items only|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice-5<br />Coke - 2|To test if the order list catcher can catch a correct order format with no space between the item name and the dash and the price for one of the items only|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice - $5<br />Coke - $2|To test if the order list catcher can catch a correct order format with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice- $5<br />Coke- $2|To test if the order list catcher can catch a correct order format with no space between the item names and dashes with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice -$5<br />Coke -$2|To test if the order list catcher can catch a correct order format with no space between the dash and the item price with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice-$5<br />Coke-$2|To test if the order list catcher can catch a correct order format with no space between the item name and the dash and the item price with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice - $5<br />Coke -$2|To test if the order list catcher can catch a correct order format with no space between the dash and the item price for one of the items only with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice- $5<br />Coke - $2|To test if the order list catcher can catch a correct order format with no space between the item name and the dash for one of the items only with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice-$5<br />Coke - $2|To test if the order list catcher can catch a correct order format with no space between the item name and the dash and the price for one of the items only with a $ sign in front of each price|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice - $5<br />Coke - 2|To test if the order list catcher can catch a correct order format with a $ sign in front of one of the prices only|Order List:<br />Chicken rice ($5.00)<br />Coke ($2.00)| ✅ |
|Chicken rice -$5Coke - 2|To test if the order list catcher can recognise an invalid syntax and request for user to resend order|Invalid order format, please send again| ✅ |
|Chicken rice - $5Coke - 2<br /><br />Followed by /cancel|To test if the order list catcher can recognise an invalid syntax and request for user to resend order and cancelling the order request will stop the bot from continually prompting for the user to send again| Invalid order format, please send again | ✅ |

## Feature Limitations and Constraints

### Cloud Hosting on Heroku

   * Downtime of Bot
      * Due to the free service nature of Heroku, there are times that Heroku is down or takes a while to respond due to various issues such as ping and server load. This causes some inconsistency when relying on Heroku to host our Telegram bot as there are times that the bot will take a little over 10 seconds to 'start' which can be detrimental to the User Experience
      * A possible solution to this would be utilising Heroku's paid plans which would allow the bot to have better uptime and priority in the server. However, this is an unlikely solution as the bot is not profitable to begin with so investing into a paid plan would not make economical sense.

   * Security on Heroku
      * Currently, we do not encrypt any of our token and API keys without any end-to-end encryption. This means that anyone with our CloudDB token is able to access the database and edit it. This is quite dangerous for the functionality of our bot but fortunately, we do not store any critical information from our users.
      * A possible way to solve this would be to use the cryptography API to encrypt our sensitive keys so that they won't be compromised.

### Scanning of Receipts
   * Inaccuracy of Scanned Receipt
      * We have utilised Google Cloud Vision API to digitise and read documents (in this case receipts). It can recognise a variety of text types and is the cornerstone for our receipt scanning feature to work and referenced [lutzkuen's receipt parser](https://github.com/lutzkuen/receipt-parser) for the algorithm.
      * We underestimated the complexity of receipt scanning on the whole as after reviewing the many different types of receipt formats, it became difficult to consistently be able to detect the item's name and the price. This was further complicated by receipts with the price having a discount next to the original price, leaving our algorithm confused as to which price is the price assigned to the item, causing one of the prices to be ignored (usually the price further away from the item's name). As a result of this, it has caused our algorithm to be rather inaccurate when parsing the receipt with large gaps between the expected and actual result. Depending on the receipt, sometimes it would be more accurate but most of the time it was not.
      * A possible way to fix this would be to incorporate Machine Learning into the algorithm where the algorithm gradually learns to better read receipts but this is way beyond our depth at this time.
 
### Mobile Application
   * Lack of time to develop
      * Setting out, we had planned the mobile application to be the main feature of our product, with us including Flutter in our main techstack. Unfortunately, by Milestone 2, we had just finished our bot's main features and felt we lacked the time to develop a proper up-and-running mobile application. The application would have aimed to synergise with the features of our bot, using it to notify users and settle debts as well since the basic functions to execute these actions are already in place we could have ran them via the application.

### Telegram Bot
   * Restricted User Interface Expression
      * Telegram's Bot API has been wonderful to work with, especially with the wrapper classes from python-telegram-bot. However, when it came to designing functional buttons for our keyboards or designing customised messaged from our bot, it was rather restrictive with buttons only being able to be below the message instead of a side-by-side. This User Interface (UI) restriction is evident in the admittedly clumsy design of the message sent to the user using the /whoowesme or /whomeowes commands where we used placeholder buttons to display the relevant text fields.
      * Designing of custom buttons was also troublesome as we could not choose how wide we wanted our buttons to be individually, with each button in a single row having the same width. This made it difficult to add buttons with longer text as sometimes the text would be truncated and overall looks unprofessional with two obviously differing text length buttons having the same width.
   * Group Member Retrieval
      * As of time of writing, Telegram's Bot API does not support any way for the bot to consistently retrieve the members of a group it has been added to. Hence, we had to manually monitor users in the group by them entering/leaving the group as well as their messages using our groupMemberScanner function.
      * This leads to a breach of privacy as we are actively parsing every single message in the group in order to setup our database with the users in the group. However, we do not store any of these messages sent by the user and do not use the contents of their messages in any meaningful way aside from the ones directed towards the bot.

### Geographical Restriction
   * Dollar Limitation
      * Currently, our bot only supports the '$' currency system and is not customisable to fit other countries. Additional, the local prevailing taxes are unlikely to be the same in other countries
      * A possible solution would be to have a command to set the country, with different countries having different profiles with their localised currency symbol as well as their common taxes.

## Prototyping

### O$P$ Mobile Application

We plan to launch a mobile application with similar functionality to our Telegram Bot with certain extensions. You can find a demonstration of what we hope to see from it below.

| Login Page | Home Page  |
| ---------- | ---------- |
|![Sample Login Page](https://res.cloudinary.com/jianoway/image/upload/v1623863754/homepageGif_wtx6xh.gif)|![Sample Home Page](https://res.cloudinary.com/jianoway/image/upload/v1623863761/uiGif_sb9kka.gif)|


### Telegram Bot (@OwePay_bot)

Currently, we are hosting our Telegram Bot via Heroku so it should be up 24/7. You can test out it’s features by messaging it directly on Telegram. (@OwePay_bot)


## Software Engineering Principles

### Immutability

Our values declared by our functions are immutable where possible, allowing us to predict the behaviour of our program with higher accuracy. An example of this would be the splitEvenlyKeyboardMarkup where define keyboardHolder as a list, an immutable data type for Python.

   ![SWEP Immutability](https://res.cloudinary.com/jianoway/image/upload/v1626336857/Screenshot_2021-07-15_at_4.14.12_PM_bhxw4j.png)

### Object-Oriented Programming (OOP)

Our codebase uses a the python-telegram-bot API as our main tool to create the bot. It is a wrapper that has many pre-determined wrapper classes to allow us to easily abstract data from and predict their outcomes. This allowed us to use a more functional based approach since most of the relevant Classes have already been delcared and we did not require many new classes to design our bot.

However, with that said we did use OOP principles which can be seen in the flow of logic of the program.

Below you can find some UML diagrams for your reference.
![UML 1](https://res.cloudinary.com/jianoway/image/upload/v1624114145/startPrivateUMI_h25isz.png)
![UML 1](https://res.cloudinary.com/jianoway/image/upload/v1624114139/startGroup_UML_ncnqol.png)
