import os
import sklearn
from sklearn.datasets import load_files

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix

from sklearn.feature_extraction.text import CountVectorizer
import nltk

import pickle

class Classifier:

	def __init__(self, review_list):

		self.moviedir = os.getcwd() + '/txt_sentoken'
		# loading all files. 
		self.movie = load_files(self.moviedir, shuffle=True, encoding='ISO-8859-1')
		self.review_list = review_list

	def Training(self):

		# split data into training and test sets
		docs_train, docs_test, y_train, y_test = train_test_split(self.movie.data, self.movie.target, 
		                                                          test_size = 0.10, random_state = 12)
		# initialize CountVectorizer
		# using the most common 5000 words
		movieVzer = CountVectorizer(min_df=2, tokenizer=nltk.word_tokenize, max_features=5000)

		# fit and tranform using training text 
		docs_train_counts = movieVzer.fit_transform(docs_train)

		# convert raw frequency counts into TF-IDF values
		movieTfmer = TfidfTransformer()
		docs_train_tfidf = movieTfmer.fit_transform(docs_train_counts)

		# using the fitted vectorizer and transformer, tranform the test data
		docs_test_counts = movieVzer.transform(docs_test)
		docs_test_tfidf = movieTfmer.transform(docs_test_counts)

		# build a classifier using Multinominal Naive Bayes model
		# train a multimoda Naive Bayes classifier (fitting)
		clf = MultinomialNB()
		clf.fit(docs_train_tfidf, y_train)

		# save the model
		filename = 'finalized_model.pkl'

		with open(filename, 'wb') as fout:
			pickle.dump((movieVzer, movieTfmer, clf), fout)

		# Predict the Test set results, find accuracy
		y_pred = clf.predict(docs_test_tfidf)

		# accuracy
		print(sklearn.metrics.accuracy_score(y_test, y_pred))

		# making the Confusion Matrix
		cm = confusion_matrix(y_test, y_pred)
		print(cm)

	def Categorize(self):

		pos = 0
		neg = 0

		with open('finalized_model.pkl', 'rb') as f:
			movieVzer, movieTfmer, clf = pickle.load(f)

		# clean movie reviews from website
		reviews_new = self.review_list

		reviews_new_counts = movieVzer.transform(reviews_new)         # turn text into count vector
		reviews_new_tfidf = movieTfmer.transform(reviews_new_counts)  # turn into tfidf vector

		# have classifier make a prediction
		pred = clf.predict(reviews_new_tfidf)

		# record the results
		for review, category in zip(reviews_new, pred):
			if self.movie.target_names[category] == 'pos':
				pos += 1
			else:
				neg += 1
		print()
		print("Predicted sentiment")
		print("Positive: " + str(pos))
		print("Negative: " + str(neg))
		print()

#if __name__ == "__main__":
	#Classifier([]).Training()
