from __future__ import unicode_literals
from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pprint
import numpy as np
from sklearn import svm
import random

client = MongoClient()
# Connect to database of identified memes
db = client['local']
collection = db['memeids']

# Transforms to create BOW/Tf-Idf feature vectors
vectorizer = CountVectorizer(min_df=2)
transformer = TfidfTransformer(smooth_idf=False)
# Create links for storing processed data
corpus = []
allY = []
memeIndices = []
nonMemeIndices = []
for index, comment in enumerate(collection.find()):
    # Store body of text and corresponding tag
    corpus.append(comment['body'])
    allY.append(1 if comment['isMeme'] else 0)
    # Store indices for sampling later
    if comment['isMeme']:
        memeIndices.append(index)
    else:
        nonMemeIndices.append(index)

# Transform each comment into a Bag of Words representation with a tf-idf transform applied
bow = vectorizer.fit_transform(corpus)
allX = transformer.fit_transform(bow).toarray()

# Shuffle indices to randomize selection
random.shuffle(memeIndices)
random.shuffle(nonMemeIndices)

X = []
y = []

# Count out an even number of meme and non-meme data samples, to avoid making the classifier biased
# by the relative volume of non-memes
for i in range(len(memeIndices)):
    memeIndex = memeIndices[i]
    nonMemeIndex = nonMemeIndices[i]
    X.append(allX[memeIndex])
    y.append(allY[memeIndex])
    X.append(allX[nonMemeIndex])
    y.append(allY[nonMemeIndex])

# Shuffle/randomize the order of the training data
combined = list(zip(X, y))
random.shuffle(combined)
X[:], y[:] = zip(*combined)

# Split data into 1/6th test and 5/6th training
testX = X[:len(X)/6]
testY = y[:len(X)/6]
trainX = X[len(X)/6:]
trainY = y[len(X)/6:]

# Train SVM
clf = svm.SVC(decision_function_shape='ovr')
clf.fit(trainX, trainY)

# True positives, False positives, True negatives, False negatives
tp = 0.0
fp = 0.0
tn = 0.0
fn = 0.0
# Go through training data, increment correct value based on each classification
for i in range(len(testY)):
    pred = clf.predict(testX[i])
    actual = testY[i]
    if pred == 1 and pred == actual:
        tp += 1.0
    elif pred == 1 and pred != actual:
        fp += 1.0
    elif pred == 0 and pred == actual:
        tn += 1.0
    elif pred == 0 and pred != actual:
        fn += 1.0

# Print out performance statistics
print(str(tp) + ", " + str(fp) + ", " + str(tn) + ", " + str(fn))
print("Accuracy: " + str((tp + tn) / (tp + tn + fp + fn)))
print("Precision: " + str((tp) / (tp + fp) if (tp + fp) > 0 else 0))
print("Recall: " + str((tp) / (tp + fn) if (tp + fn) > 0 else 0))
