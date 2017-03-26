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

meme_lexicon = set()

def generate_meme_title_corpus():
    global names_cv, names_tfidf_transformer, clf, target_names

    target_names = []
    for line in open("memes.json"):
        meme = json.loads(line)["meme"]
        title = textacy.preprocess.preprocess_text(meme, no_punct=True, fix_unicode=True, lowercase=True, no_urls=True, no_emails=True)
        if title not in ["url", "*url*", "*email*", "email"]:
            target_names.append(title)
            meme_lexicon.update(title.split())
    names_cv = CountVectorizer()
    names_tfidf_transformer = TfidfTransformer()

    training_data = names_cv.fit_transform(target_names)
    training_data_tfidf = names_tfidf_transformer.fit_transform(training_data)

    clf = BallTree(training_data_tfidf.toarray(), leaf_size=100)


def get_nearest_meme_title(text):
    new_input = names_cv.transform([text])
    new_tfidf = names_tfidf_transformer.transform(new_input)
    dist, [[ind]] = clf.query(new_tfidf.toarray(), k=1)
    if dist < 0.5 and ind != 0:
        return target_names[ind]

def process_comment(comment):
    text = textacy.preprocess.preprocess_text(comment["body"], no_punct=True, fix_unicode=True, lowercase=True, no_urls=True, no_emails=True)
    isReliable, textBytesFound, details = cld2.detect(text.encode("utf8"))
    lang = details[0][1]
    if isReliable and lang != "en": return None
    meme = get_nearest_meme_title(text)
    comment["body"] = text
    comment["length"] = len(text)
    comment["wordCount"] = len(text.split())
    if(comment["wordCount"] > 1):
        comment["flesch"] = textstat.flesch_reading_ease(text)
    comment["lexiconSize"] = textstat.lexicon_count(text, True)
    if meme is None and comment["wordCount"] > 20 and comment["flesch"] < 60 : return None
    comment["isMeme"] = False
    if meme is not None:
        comment["isMeme"] = True
        comment["memeGuess"] = meme
    return comment

generate_meme_title_corpus()


files = sys.argv[1].split(",")
for f in files:
    rr = open(f)
    with io.open(sys.argv[2], 'w', encoding='utf-8') as output:
        for line in rr:
            comment = json.loads(line)
            comment = {k: comment[k] for k in ['body', 'score', 'gilded', 'controversiality', 'subreddit', 'created_utc']}
            processed = process_comment(comment)
            if processed is not None: output.write(json.dumps(processed, ensure_ascii=False)+"\n")
    rr.close()
