python-mysql-gcm
======================
[![Build Status](https://secure.travis-ci.org/geeknam/python-gcm.png?branch=master)](http://travis-ci.org/geeknam/python-gcm)

Python client for Google Cloud Messaging for Android (GCM)

Google GCM doc
------------
RTFM [here](http://developer.android.com/guide/google/gcm/gcm.html)
        
Project Description
------------
This is a Fork of python-gcm [https://github.com/geeknam/python-gcm].
Python-gcm library by geeknam is a single part of the Server Application you need to send messages with Google Cloud Messaging.
With this fork you can create the database to store deviceIds and you'll have the ability to send broadcast messages to all devices.

Setup
------------
* create a mysql database and import the script setup_mysql.sql (this script will create mysql tables for you!)
* open the file gcm/gcm_setup.py and change settings with your mysql and GCM credentials

Usage
------------
Now, your database has 2 tables:
* Push_Android          (you've to collect devices registration Id here)
* Push_Android_Check    (utility table to prevent too much push!)

You can register your device by manually insert registrationId into Push_Android table or you can implement your registration logic.
You can now execute ./send_test_push.py to send a test push to your device!

If you execute ./push_gcm.py the script will check Push_Android_Check table and if it will find a record with 'on' status, the push will be sent to all enabled devices.


