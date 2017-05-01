from textblob import TextBlob
from pymongo import MongoClient
import sys
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import json
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# Connect to MongoDB
client = MongoClient()
db = client['local']

# List of words that are too common or are meaningless in the context of their meme
stopwords = set(STOPWORDS)
stopwords.update(["gt", "amp", "youtube", "dQw4w9WgXcQ", "thanks", "obama", "Obama", "Obama'", "Obama '", "reddit", "nessie"])

# For generating b&w wordclouds
def black_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "#000000"

# Loop through all the meme collections
for coll in ['ratingsmemes', 'aestheticmemes', 'obamamemes', 'emojimemes', 'nessiememes', 'rickrollmemes', 'switcharoomemes', 'wotmemes']:
    # print status
    print("Stared reading for: " + coll)
    collection = db[coll]
    body = ""
    # Aggregate all bodies, stripped of newlines and weird characters
    for comment in collection.find():
        fixedBody = comment["body"].replace("\"", "'").replace("\n", "").encode('ascii', 'ignore')
        body += fixedBody + ' '
    # Print status again
    print("generating WC for: " + coll)
    # Configure & generate wordcloud
    wc = WordCloud(width=800, height=800, background_color=None, color_func=black_color_func, mode="RGBA", max_words=500, stopwords=stopwords, prefer_horizontal=1)
    wc.generate(body)
    # Write wordcloud to file
    wc.to_file(coll+"-cloud.png")
