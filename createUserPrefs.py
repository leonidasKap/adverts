from pymongo import MongoClient;

if __name__ == "__main__":
	c = MongoClient('localhost', 27017);
	db = c['mydb'];
	a = db.adverts.distinct('campaign');
	print a[0]
#	for campaign in a:
#		print campaign;
	db.command({
		"aggregate":"adverts",
		"pipeline":[
			{"$limit": 10000},
			{"$group": {"_id" : "$user_id", "campaings": {"$push" : "$campaign"}}}
		],
		"allowDiskUse":True
	});
#	b = db.adverts.aggregate(
#		[{"$group": {"_id" : "$user_id", "campaings": {"$push" : "$campaign"}}}]
#		);
#	print b[0];
