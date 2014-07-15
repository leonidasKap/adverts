# Installation

You can manage your cloud service https://manage.windowsazure.com/@kapsokalgmail.onmicrosoft.com
Given the azure vm host: leonidas.cloudapp.net
take the following steps

- create /data/db as root
- install mongodb
- sudo mongo
- create a database called mydb

- now cd into the directory with the data
$ ls | xargs -n1 mongoimport --db mydb --collection adverts --type csv --fields campaign,user_id,timestamp,city,browser,os,device,domain,activity  --stopOnError --file

install anaconda for windows from
http://continuum.io/downloads


# Start mongod Processes http://docs.mongodb.org/manual/tutorial/manage-mongodb-processes/#start-mongod-processes

By default, MongoDB stores data in the /data/db directory. On Windows, MongoDB stores data in C:\data\db. On all platforms, MongoDB listens for connections from clients on port 27017.
See.
$ sudo lsof -i :27017

	COMMAND  PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
	mongod  6454 mongod    8u  IPv4  23931      0t0  TCP localhost:27017 (LISTEN)

To install the pymongo client on windows do:

	$ pip install pymongo

Query only for the first 10 results so you have a manageable dataset to work with.
Setup port forwarding to leonidas.cloudapp.net. Enter in source 27017 and in destination localhost:27017

Then open a python cmd prompt:

>>> from pymongo import MongoClient
>>> c = MongoClient('localhost', 27017);
>>> c.test_database
Database(MongoClient('localhost', 27017), u'test_database')
>>> c['mydb']
Database(MongoClient('localhost', 27017), u'mydb')
>>> print c['mydb'].adverts.find({"os": "Windows 7", "user_id":"5289f2a340596b70c832adac"})
<pymongo.cursor.Cursor object at 0x00000000035826D8>
>>>
>>> print list(c['mydb'].adverts.find({"os": "Windows 7", "user_id":"5289f2a340596b70c832adac"}));
[{u'city': u'crawley', u'domain': u'b50c3954bbca951077209ad91913e280', u'user_id': u'5289f2a340596b70c832adac', u'campaign': u'51dac16cc25908069f801c7
0', u'timestamp': 1398949007L, u'activity': u'impression', u'device': u'pc', u'_id': ObjectId('53bbfefc9d01fbcff21d51b1'), u'os': u'Windows 7', u'brow
ser': u'IE'}]
>>>

Print the contents returned from mongo
>>> for item in c['mydb'].adverts.find({"os": "Windows 7", "user_id":"5289f2a340596b70c832adac"}):
...      print item['city']; # item is a dict (i.e. dictionary) type. 
...
crawley

Count items in a timestamp range 
>>> print c['mydb'].adverts.find({"timestamp":{"$gte": 1398949007, "$lt": 1398950007} }).count();
121804

Find items in a timestamp range
>>> items = c['mydb'].adverts.find({"timestamp":{"$gte": 1398949007, "$lt": 1398950007} });


# Python on CentOS
To setup python pip and virtualenv side by side with the system's 2.6 follow:
https://www.digitalocean.com/community/tutorials/how-to-set-up-python-2-7-6-and-3-3-3-on-centos-6-4

Setting up a virtual environment for affectv
https://www.digitalocean.com/community/tutorials/common-python-tools-using-virtualenv-installing-with-pip-and-managing-packages
$ virtualenv affectv # creates the virtual environment
$ source affectv/bin/activate # activates the virtual environment

Installing numpy
follow : https://gist.github.com/fyears/7601881#file-note-md
$ pip install numpy

Scipy needs the following:
$ yum install atlas atlas-devel lapack-devel blas-devel
from http://www.linuxquestions.org/questions/linux-software-2/instruction-for-installing-lapack-and-lapack-devel-on-centos-6-5-a-4175509481/

Then you can do 
$ pip install scipy


Installing matplotlib
Before that you need to install the system level dependencies 
$ yum install freetype-devel
$ yum install libpng-devel

Then you should be able to do:
$ pip install matplotlib
Otherwise you will see 
requires:
 freetype: no  [pkg-config information for 'freetype2' could

                        not be found.

# MongoDB queries in mongo utility

## How to get the distinct number of users for a particular campaign
db.adverts.distinct("user_id", {campaign : "518ac5df0189603420c6ffe6"}).length

## How to count the number of distinct users 
 db.adverts.aggregate([{$group : {_id : "$user_id"} }, {$group: {_id:1, count: {$sum : 1 }}}],{allowDiskUse:true})

## How to find the distinct campaigns
a=db.adverts.distinct('campaign');

## How to find the min and max timestamp

The following finds the max
$ db.adverts.aggregate([{$group : {_id : "$os", timePerOs: {$max : "$timestamp"}}},{$group: {_id:1, max: {$max: "$timePerOs"}}}])

{ "_id" : 1, "max" : NumberLong(1399160081) }

The following finds the min

$ db.adverts.aggregate([{$group : {_id : "$os", timePerOs: {$min : "$timestamp"}}},{$group: {_id:1, min: {$min: "$timePerOs"}}}])

{ "_id" : 1, "min" : NumberLong(1398898959) }

to verify the min and max 
$ db.adverts.find({"timestamp":{"$gte": 1398898959, "$lte": 1399160081} }).count()
gives 4672976

## How to find the frequency of activity "click" for user i on campaign j

First of all build an index on campaign so you can speed up queries
$ db.adverts.ensureIndex({campaign: 1})

In mongo cli you can collect all campaigns for each user. The following runs fine in mongodb cli
$ db.adverts.aggregate([{"$group": {"_id" : "$user_id", "campaings": {"$push" : "$campaign"}}}],{allowDiskUse:true});
Let me do the same in python, I have problems passing {allowDiskUse:true} so I 'll try
db.runCommand.
db.runCommand has problems, see:
failed: exception: aggregation result exceeds maximum document size
I fixed it finally

## How do I push the campaign and activity for each campaign ?

## How do I speed up the aggregation of users against their campaign ?
First create a list of all indexes.
$ db.adverts.getIndexes()
Then create a joined index of user_id and campaign, that didn't speed up things massively


=============

Ideas for Affectv

Describe how you can put everything behind a server. The best demo would be to upload a file and see it analyzed. 
The problem will be port forwarding. I don't think port 80 is open

I think part-m-00000 is missing -> verify it by search for something from this part-m-00000 dataset.


suppose you want to answer the behavioural modeling.
Take all campaigns 
- For each user create a vector of its activities for each campaign he didn't convert. For the campaigns he didn't have any activity say unknown
- For each conversion of the same user create another vector identical to the first


