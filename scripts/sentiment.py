import lxml
import requests
import time
import sys
import progress_bar as PB
import training_classifier as tcl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os.path
import pickle
from statistics import mode
from nltk.classify import ClassifierI
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder as BCF
import itertools
from nltk.classify import NaiveBayesClassifier
from flask import jsonify

YOUTUBE_IN_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&pageToken={pageToken}&videoId={videoId}&key={key}'
YOUTUBE_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&videoId={videoId}&key={key}'
key = 'AIzaSyByv3h2cu6tYVMpYLJviAoGaNYWfy8Xt5o'

def commentExtract(videoId):
	print ("Comments downloading")
	page_info = requests.get(YOUTUBE_LINK.format(videoId = videoId, key = key))
	print("page status is " + str(page_info.status_code))
	while page_info.status_code != 200:
		if page_info.status_code != 429:
			print ("Comments disabled")
			sys.exit()
			return "nocomment"

		time.sleep(20)
		page_info = requests.get(YOUTUBE_LINK.format(videoId = videoId, key = key))

	page_info = page_info.json()

	comments = []
	co = 0;
	print(len(page_info['items']))
	for i in range(len(page_info['items'])):
		comments.append(page_info['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
		co += 1
		print(co)
		# if co == count:
		# 	PB.progress(co, count, cond = True)
		# 	print ()
		# 	return comments

	#PB.progress(co, count)
	# INFINTE SCROLLING
	while 'nextPageToken' in page_info:
		temp = page_info
		page_info = requests.get(YOUTUBE_IN_LINK.format(videoId = videoId, key = key, pageToken = page_info['nextPageToken']))

		while page_info.status_code != 200:
			time.sleep(20)
			page_info = requests.get(YOUTUBE_IN_LINK.format(videoId = videoId, key = key, pageToken = temp['nextPageToken']))
		page_info = page_info.json()

		for i in range(len(page_info['items'])):
			comments.append(page_info['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
			co += 1
			print(co)
			if co == 101:
			# 	PB.progress(co, count, cond = True)
				print ("done")
				return comments
		#PB.progress(co, count)
	#PB.progress(count, count, cond = True)
	print ()

	return comments

def features(words):
	temp = word_tokenize(words)

	words = [temp[0]]
	for i in range(1, len(temp)):
		if(temp[i] != temp[i-1]):
			words.append(temp[i])

	scoreF = BigramAssocMeasures.chi_sq

	#bigram count
	n = 150

	bigrams = BCF.from_words(words).nbest(scoreF, n)

	return dict([word,True] for word in itertools.chain(words, bigrams))

class VoteClassifier(ClassifierI):
	def __init__(self, *classifiers):
		self.__classifiers = classifiers

	def classify(self, comments):
		votes = []
		for c in self.__classifiers:
			v = c.classify(comments)
			votes.append(v)
		con = mode(votes)

		choice_votes = votes.count(mode(votes))
		conf = (1.0 * choice_votes) / len(votes)

		return con, conf

def sentiment(comments):

	if not os.path.isfile('/home/faizollah/mysite/classifier.pickle'):
		tcl.training()

	fl = open('/home/faizollah/mysite/classifier.pickle','rb')
	classifier = pickle.load(fl)
	fl.close()

	pos = 0
	neg = 0
	for words in comments:
		comment = features(words)
		sentiment_value, confidence = VoteClassifier(classifier).classify(comment)
		if sentiment_value == 'positive':# and confidence * 100 >= 60:
			pos += 1
		else:
			neg += 1

	#print ("Positive sentiment : ", (pos * 100.0 /len(comments)) )
	#print ("Negative sentiment : ", (neg * 100.0 /len(comments)) )
	psent = (pos * 100.0 /len(comments))
	nsent = (neg * 100.0 /len(comments))
	return psent, nsent
