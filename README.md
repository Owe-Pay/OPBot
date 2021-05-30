# O$P$

Introduction

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

* As the person who usually helps to pay first for food when ordering in deliveries for my hostel mates, I wish I had a way to easily visualise who is in debt with me.

* As the person who mainly orders food for my hostel level mates, I want presets that accomodate for common additional fees such as Goods and Services Charge (GST) and service charge. 

* As a student who tags on to food orders, I want to have a system that keeps track of how much I still owe to people and the breakdown of the debt.

* As a person who goes out to eat with friends , I want a simple system to create new orders to be repaid and update the status of my debts. 

* As a person who eats out with friends, I want a system that tracks the food items bought without the need for manually inputting the data, which reduces inconvenience for me.

Development Plan:

We have decided to start by implementing our Telegram Bot and our MySQL database to store user information for us to manage and use for our Telegram Bot.

**Telegram Bot (@OwePay_bot)**

![New User Registration](https://res.cloudinary.com/jianoway/image/upload/v1622368793/O_P_-_First_Time_Registration_Fixed_mdpff8.jpg)
*Figure 1: Registration process for Users and Groups*

1. Registration
   1. /start will initiate the bot and ask users to register.
   1. Users and groups will have the option of choosing if they wish to register with us in order to give users control over their private data. We have implemented this feature by using Inline Keyboard Buttons that appear under the registration message.
   1. Registration for groups and individuals would be a different process. Using the Telegram Bot API allows us to register groups and individuals separately and we will be able to use a relational database to link users to the groups they belong to.
   1. After Users and Groups are registered, we will store their unique chat_ids in our database 
   1. Due to the nature of Telegram Bots, for our bot to message the user, the user will have had to have messaged our bot first. Hence, to ensure our Notification feature works we will have a column dedicated to keeping track if a registered user is Notifiable.




![New Order Flow](https://res.cloudinary.com/jianoway/image/upload/v1622368925/O_P_-_TeleBot_New_Order_Flow_qfpbtr.jpg)
