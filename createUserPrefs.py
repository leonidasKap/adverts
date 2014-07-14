from pymongo import MongoClient;

if __name__ == "__main__":
	c = MongoClient('localhost', 27017);
	db = c['mydb'];
	a = db.adverts.distinct('campaign');
	print a[0]
#	for campaign in a:
#		print campaign;
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
#	print type(db.adverts.find({"timestamp":{"$gte": 1398949007, "$lt": 1398950007} }));
	c = db.adverts.aggregate(
		[
                        {"$limit": 5},
                        {"$group": {"_id" : "$user_id", "campaigns": {"$push" : "$campaign"}}}
                ],
		allowDiskUse=True,
		cursor = {}
	);
	print type(c);
	for user in list(c):
		print(user);
#	TODO: create a cursor out of the result set b
