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

if __name__ == "__main__":
	c = MongoClient('localhost', 27017);
	db = c['mydb'];
	c = db.adverts.aggregate(
		[
                        {"$limit": 500000},
                        {"$group": {"_id" : "$user_id",
				"campaigns": {"$push" : {"campaign":"$campaign", "activity":"$activity"}}}},
			{"$out": "prefs"}
                ],
		allowDiskUse=True,
		cursor = {}
	);
	c = db.prefs.find({"campaigns": {"$not": {"$elemMatch": {"activity":"conversion"}}} });
	print c;
	a = 0;
	for user in list(c):
		print(user);
		a=a+1;
		if a == 10:
			break;
