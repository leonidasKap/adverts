from pymongo import MongoClient;
import userAggregator;

def printFirstN(cursor, n):
	for i in range(n):
		print cursor[i];

if __name__ == "__main__":
	c = MongoClient('localhost', 27017);
	db = c['mydb'];
	aggregateUsers(db, 1000000); # this will limit the processing pipeline to the first 1000000 documents

	converted = db.prefs.find({"campaigns": {"$elemMatch": {"activity":"conversion"}} });
	nonConverted = db.prefs.find({"campaigns": {"$not": {"$elemMatch": {"activity":"conversion"}}} });

	print 'Converted : ', converted.count();
	print countActivities(converted);
	print 'Non Converted: ', nonConverted.count();
	print countActivities(nonConverted);

	# store the activities per campaign for a particular user in a new collection
	prefsFreq = countActivitiesPerUser(db);
	# count how many users have been involved in x distinct campaigns
	print 'The number of users with:';
	for i in range(20):
		print i, ' campaigns: ', prefsFreq.find({"campaignCount": i}).count();



