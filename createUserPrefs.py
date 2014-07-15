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
	return activities;

if __name__ == "__main__":
	c = MongoClient('localhost', 27017);
	db = c['mydb'];
	# aggregateUsers(db, 50000);
	converted = db.prefs.find({"campaigns": {"$elemMatch": {"activity":"conversion"}} });
	nonConverted = db.prefs.find({"campaigns": {"$not": {"$elemMatch": {"activity":"conversion"}}} });

	print countActivities(converted);
	print countActivities(nonConverted);
	n = 3;
	print ' Converted : ',converted.count();
	converted.rewind();
	nonConverted.rewind();
	db.create_collection('prefsFreq');
	for user in nonConverted:
		uniqueCampaigns = {};
		for camp in user['campaigns']:
			if camp['campaign'] not in uniqueCampaigns:
				uniqueCampaigns[camp['campaign']]={camp['activity']: 1};
			else:
				uniqueCampaigns[camp['campaign']][camp['activity']]+=1;

		db.prefsFreq.insert({
				"_id": user['_id'],
				"campaigns" : uniqueCampaigns
			});

	# printFirstN(converted, n);
	print ' Non Converted: ',nonConverted.count();
	#printFirstN(nonConverted, n);

