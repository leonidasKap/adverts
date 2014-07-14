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
                        {"$limit": 5},
                        {"$group": {"_id" : "$user_id",
				"campaigns": {"$push" : {"campaign":"$campaign", "activity":"$activity"}}}}
                ],
		allowDiskUse=True,
		cursor = {}
	);
	print type(c);
	for user in list(c):
		print(user);
