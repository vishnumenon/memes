from __future__ import unicode_literals
from textblob import TextBlob
from pymongo import MongoClient

client = MongoClient()
# connect to database
db = client['local']

# Loop through all memes' individual databases
for coll in ['ratingsmemes', 'aestheticmemes', 'obamamemes', 'emojimemes', 'nessiememes', 'rickrollmemes', 'switcharoomemes', 'wotmemes']:
    collection = db[coll]
    polarities = []
    subjectivities = []
    # For each comment in the database
    for comment in collection.find():
        # Remove unicode characters that were causing problems for TextBlob
        fixedBody = comment["body"].replace("\"", "'").replace("\n", "").encode('ascii', 'ignore')
        # create the TextBlob object
        blob = TextBlob(fixedBody)
        # Store the polarity and the sentiment of the comment
        polarities.append(blob.sentiment.polarity)
        subjectivities.append(blob.sentiment.subjectivity)
    # Print out averages for each meme
    print coll + ": avg pol: " + str(sum(polarities) / float(len(polarities))) + "; avg subj: " + str(sum(subjectivities) / float(len(subjectivities))) + "\n"
