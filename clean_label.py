# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.f

from __future__ import unicode_literals
import json
import io
import spacy
import textacy
import cld2
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import BallTree
from numpy import array, ndarray
import pickle
import os.path
import random
import sys
from textstat.textstat import textstat

# Create the classifier for identifying potential memes
def generate_meme_title_corpus():
    global names_cv, names_tfidf_transformer, clf, target_names

    # Array to hold valid meme names from the meme db
    target_names = []
    # iterate through entries in memes.json
    for line in open("memes.json"):
        meme = json.loads(line)["meme"]
        # clean meme titles to match the cleaning done on comments
        title = textacy.preprocess.preprocess_text(meme, no_punct=True, fix_unicode=True, lowercase=True, no_urls=True, no_emails=True)
        # Discard memes that are just a URL or just an email, and save all others
        if title not in ["url", "*url*", "*email*", "email"]:
            target_names.append(title)
    # Create a vectorizer that makes bag-of-words vectors
    names_cv = CountVectorizer()
    # Create a TF-IDF transformer to give more importance to rare words
    names_tfidf_transformer = TfidfTransformer()

    # Fit transformer with collected target names, and fit tf-idf
    training_data = names_cv.fit_transform(target_names)
    training_data_tfidf = names_tfidf_transformer.fit_transform(training_data)

    # Create BallTree for quick nearest-neighbor lookups, using leaf-size=100 for speed purposes
    clf = BallTree(training_data_tfidf.toarray(), leaf_size=100)

# Use the generated Ball Tree to find the meme nearest the given text in the vector space
def get_nearest_meme_title(text):
    # Use the pre-fit Count Vectorizer to find the BOW for a random text using the meme titles' lexicon,
    # then apply tf-idf
    new_input = names_cv.transform([text])
    new_tfidf = names_tfidf_transformer.transform(new_input)
    # query the ball tree to find the meme title that is closest
    dist, [[ind]] = clf.query(new_tfidf.toarray(), k=1)
    # return it iff it is a sufficiently close match and matched with a valid meme
    if dist < 0.5 and ind != 0:
        return target_names[ind]

def process_comment(comment):
    # Clean the comment by removing punctuation, lowercase-ing, and stripping urls/emails to make statistics about the text more meaningful
    text = textacy.preprocess.preprocess_text(comment["body"], no_punct=True, fix_unicode=True, lowercase=True, no_urls=True, no_emails=True)
    # Detect language
    isReliable, textBytesFound, details = cld2.detect(text.encode("utf8"))
    lang = details[0][1]
    # Throw out any comments that are definitively non-english
    if isReliable and lang != "en": return None
    # Find nearest meme
    meme = get_nearest_meme_title(text)
    # Overwrite body with cleaned body
    comment["body"] = text
    # Store word count, length, and lexicon-size to potentially use as predictive variables
    comment["length"] = len(text)
    comment["wordCount"] = len(text.split())
    if(comment["wordCount"] > 1):
        # Store flesch score for sufficiently long comments
        comment["flesch"] = textstat.flesch_reading_ease(text)
    comment["lexiconSize"] = textstat.lexicon_count(text, True)
    # Filter out comments that are _extremely_ unlikely to contain memes, based on word counts
    # and Flesch score -- thresholds picked during data explanation
    if meme is None and comment["wordCount"] > 20 and comment["flesch"] < 60 : return None
    comment["isMeme"] = False
    if meme is not None:
        # Store possible meme if there is a strong guess from out DB
        comment["isMeme"] = True
        comment["memeGuess"] = meme
    # Return cleaned & processed comment
    return comment


generate_meme_title_corpus()

# Allow for multiple input files, separated by commas
files = sys.argv[1].split(",")
for f in files:
    rr = open(f)
    # Open output file
    with io.open(sys.argv[2], 'w', encoding='utf-8') as output:
        for line in rr:
            # Load json comment and discard useless keys
            comment = json.loads(line)
            comment = {k: comment[k] for k in ['body', 'score', 'gilded', 'controversiality', 'subreddit', 'created_utc']}
            # Process comment
            processed = process_comment(comment)
            # Save all valid processed comments
            if processed is not None: output.write(json.dumps(processed, ensure_ascii=False)+"\n")
    rr.close()
