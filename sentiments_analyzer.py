#Python 3.5

# __author__ = "Mark Conley"
# Sentiment Analyzer

import pymongo
import json
from pymongo import MongoClient

#client = MongoClient('mongodb://localhost:27017/')
client = MongoClient('localhost', 27017)
db = client.Sentiments

positive_words = set(line.strip() for line in open(r'positive words.txt', 'r'))
negative_words = set(line.strip() for line in open(r'negative words.txt', 'r'))

labeled_reviews = []

for review in db.UnlabeledReview.find():
	sentiment = 0
	split_review = db.UnlabeledReviewAfterSplitting.find_one({'id' : review['id']})

	for words in split_review['review']:
		sentiment += 1 if words['word'] in positive_words else 0
		sentiment -= 1 if words['word'] in negative_words else 0

	category = 'positive' if sentiment >= 0 else 'negative'
	labeled_reviews.append({'_id' : review['id'], 'review' : review['review'], 'category' : category })



categorization_file = 'LabeledReviews.json'
with open(categorization_file, 'w') as outfile:
	json.dump(labeled_reviews, outfile)
