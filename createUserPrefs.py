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
#	TODO: create a cursor out of the result set b
