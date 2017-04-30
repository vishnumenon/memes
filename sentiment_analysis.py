from __future__ import unicode_literals
from textblob import TextBlob
from pymongo import MongoClient

client = MongoClient()
db = client['local']
# connect to database
collection = db['ratingsmemes']   # or aestheticmemes, obamamemes

print("body,gilded,created_utc,subreddit,score,controversiality,polarity,subjectivity")
for comment in collection.find():
    # carry out sentiment analysis
    fixedBody = comment["body"].replace("\"", "'").replace("\n", "").encode('ascii', 'ignore')
    blob = TextBlob(fixedBody)
    # Print out in STATA-readable csv format for statistical analysis
    print("\"{0}\",{1!s},{2},{3},{4!s},{5!s},{6!s},{7!s}".format(fixedBody, comment["gilded"], comment["created_utc"], comment["subreddit"], comment["score"], comment["controversiality"], blob.sentiment.polarity, blob.sentiment.subjectivity))
