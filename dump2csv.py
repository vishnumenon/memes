from __future__ import unicode_literals
import json
import sys
import io

input = sys.argv[1]

# Column headers
print("body,gilded,created_utc,subreddit,score,controversiality")
for line in open(input):
    comment = json.loads(line)
    # Print out each line of CSV, with the body's contents stripped of newlines because STATA struggled to deal with CSVs that had newlines in fields
    print("\"{0}\",{1!s},{2},{3},{4!s},{5!s}".format(comment["body"].replace("\"", "'").replace("\n", ""), comment["gilded"], comment["created_utc"], comment["subreddit"], comment["score"], comment["controversiality"]))
