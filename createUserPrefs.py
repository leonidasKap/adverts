from pymongo import MongoClient;

if __name__ == "__main__":
	c = MongoClient('localhost', 27017);
	db = c['mydb'];
	b = db.command({
		"aggregate":"adverts",
		"pipeline":[
			{"$limit": 10000},
			{"$group": {"_id" : "$user_id", "campaings": {"$push" : "$campaign"}}}
		],
		"cursor": {},
		"allowDiskUse":True
	});
#	TODO: create a cursor out of the result set b
	print type(b);
	c = db.adverts.aggregate(
		[
                        {"$limit": 50000},
                        {"$group": {"_id" : "$user_id",
				"campaigns": {"$push" : {"campaign":"$campaign", "activity":"$activity"}}}},
			{"$out": "prefs"}
                ],
		allowDiskUse=True,
		cursor = {}
	);
	print type(c);
	a = 0;
	for user in list(c):
		print(user);
		a=a+1;
		if a == 10:
			break;
