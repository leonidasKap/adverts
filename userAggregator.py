# Accepts a mongo database with a collection called adverts and a limit on how many
# entries to process. It groups the campaigns and the corresponding browsing activities per the user.
# For each user the created document follows the format below
# {_id : user_id,
# campaigns: [{campaign1 : activity1}, {campaign1 : activity2}, {campaign2 : activity1} ]}
# Results are stored in a collection called prefs.
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

# Accepts a cursor to the prefs collection.
# Returns a dictionary with the frequency of each activity.
def countActivities(converted):
	activities = {'impression':0,'click':0,'retargeting':0,'conversion':0};
	for item in converted:
		for camp in item['campaigns']:
			activities[camp['activity']]+=1;
	converted.rewind(); # restore the cursor to its initial state
	return activities;

# Accepts a database containing the prefs collection.
# Returns a cursor to a new collection called prefsFreq 
# which contains a document per user in the following format:
# {_id : user_id,
# campaigns: {campaign1 : {activity1: frequency}, campaign2 :{activity1: frequency}}
def countActivitiesPerUser(db):
	# recreate collection with preference frequencies
	if 'prefsFreq' in db.collection_names():
		db.prefsFreq.drop();

	db.create_collection('prefsFreq');
	rawPrefs = db.prefs.find();
	limit = 100;
	xCount = 1;
	documents = [];
	for user in rawPrefs:
		uniqueCampaigns = {};
		for camp in user['campaigns']:
			if camp['campaign'] not in uniqueCampaigns:
				uniqueCampaigns[camp['campaign']]={camp['activity']: 1};
			elif camp['activity'] not in uniqueCampaigns[camp['campaign']]:
				uniqueCampaigns[camp['campaign']][camp['activity']]=1;
			else:
				uniqueCampaigns[camp['campaign']][camp['activity']]+=1;
		if xCount % limit == 0:
			db.prefsFreq.insert(documents);
			xCount = 1;
			documents = [];
		else:
			documents.append({
				"_id": user['_id'],
				"campaigns" : uniqueCampaigns,
				"campaignCount" : len(uniqueCampaigns)
			});
			xCount+=1;
	db.prefsFreq.insert(documents);
	return db.prefsFreq;