from pymongo import MongoClient;
def groupUsers(db):
	b = db.command({
		"aggregate":"adverts",
		"pipeline":[
			{"$limit": 10000},
			{"$group": {"_id" : "$user_id", "campaings": {"$push" : "$campaign"}}}
		],
		"cursor": {},
		"allowDiskUse":True
	});
	print type(b);

def aggregateUsers(db, n):
	db.adverts.aggregate(
		[
            {"$limit": n},
            {"$group": {"_id" : "$user_id",
				"campaigns": {"$push" : {"campaign":"$campaign", "activity":"$activity"}}}},
			{"$out": "prefs"}
        ],
		allowDiskUse=True,
		cursor = {}
	);

def printFirstN(cursor, n):
	a = 0;
	for user in cursor:
		print user;
		a=a+1;
		if a == n:
			break;

def countActivities(converted):
	activities = {'impression':0,'click':0,'retargeting':0,'conversion':0};
	for item in converted:
		for camp in item['campaigns']:
			activities[camp['activity']]+=1;
	converted.rewind(); # restore the cursor to its initial state
	return activities;

def countActivitiesPerUser(db):
	# recreate collection with preference frequencies
	if 'prefsFreq' in db.collection_names():
		db.prefsFreq.drop();

	db.create_collection('prefsFreq');
	rawPrefs = db.prefs.find();
	for user in rawPrefs:
		uniqueCampaigns = {};
		# you can put the number of campaigns in a seperate field
		print user;
		for camp in user['campaigns']:
			if camp['campaign'] not in uniqueCampaigns:
				uniqueCampaigns[camp['campaign']]={camp['activity']: 1};
			elif camp['activity'] not in uniqueCampaigns[camp['campaign']]:
				uniqueCampaigns[camp['campaign']][camp['activity']]=1;
			else:
				uniqueCampaigns[camp['campaign']][camp['activity']]+=1;

		db.prefsFreq.insert({
				"_id": user['_id'],
				"campaigns" : uniqueCampaigns,
				"campaignCount" : len(uniqueCampaigns)
			});
	return db.prefsFreq;

if __name__ == "__main__":
	c = MongoClient('localhost', 27017);
	db = c['mydb'];
	# aggregateUsers(db, 1000000);
	converted = db.prefs.find({"campaigns": {"$elemMatch": {"activity":"conversion"}} });
	nonConverted = db.prefs.find({"campaigns": {"$not": {"$elemMatch": {"activity":"conversion"}}} });

	print 'Converted : ', converted.count();
	print countActivities(converted);
	print 'Non Converted: ', nonConverted.count();
	print countActivities(nonConverted);

	# store the activities per campaign for a particular user in a new collection
	prefsFreq = countActivitiesPerUser(db);
	# count how many users have more x distinct campaigns
	print 'The number of users with:';
	for i in range(10):
		print i, ' campaigns: ', prefsFreq.find({"campaignCount": {"$gte" : i}}).count();



