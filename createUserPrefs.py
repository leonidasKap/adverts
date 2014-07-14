from pymongo import MongoClient;

if __name__ == "__main__":
	c = MongoClient('localhost', 27017);
	db = c['mydb'];
	# a = db.adverts.distinct('campaign');
	b = db.adverts.aggregate([
		{"$group": {"_id" : "$os", "timePerOs": {"$min" : "$timestamp"}}},
		{"$group": {"_id":1, "min": {"$min": "$timePerOs"}}}
	]);
	print b;
