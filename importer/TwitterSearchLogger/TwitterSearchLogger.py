#!/Usr/bin/env python
#-*- coding:utf-8 -*-

from requests_oauthlib import OAuth1Session
import json
import sys
import os
import signal
import urllib
import pickle
import posixfile
import fcntl
import time

StateFileName = "TwitterSearchLoggerState.pickle"
#MaxSearchDepth = 100
MaxSearchDepth = 100
MaxRecentTweetIDLength = 400*15*2

def StateSave(filename, data):
	fp = open(filename, "w")
	fcntl.lockf(fp, fcntl.LOCK_EX)
	pickle.dump(data, fp)
	fcntl.lockf(fp, fcntl.LOCK_UN)
	fp.close()

def StateLoad(filename):
	if not os.path.exists(filename):
		return {}
	fp = open(filename, "r")
	fcntl.lockf(fp, fcntl.LOCK_SH)
	obj = pickle.load(fp)
	fcntl.lockf(fp, fcntl.LOCK_UN)
	fp.close()
	return obj

def GetOAuthSession():
	consumer_key = 'TWITTER_CONSUMER_KEY'
	consumer_secret = 'TWITTER_CONSUMER_SECRET'
	access_key = 'TWITTER_ACCESS_KEY'
	access_secret = 'TWITTER_ACCESS_SECRET'
	return OAuth1Session(consumer_key, consumer_secret, access_key, access_secret)

def TwitterSearch(search_string, max_depth, recent_id_list):
	query = "?q=%s" % (urllib.quote(search_string), )
	twitter = GetOAuthSession()
	search_result = []
	for count in range(0, max_depth):
		search_url = "https://api.twitter.com/1.1/search/tweets.json%s" % (query, )
		req = twitter.get(search_url)
		if req.status_code != 200:
			#print "status_code is not 200. (%d)" % (req.status_code, )
			break
		result = json.loads(req.text)
		if 'search_metadata' not in result or 'next_results' not in result['search_metadata']:
			break
		query = result['search_metadata']['next_results']
		id_hit = False
		for tweet in result['statuses']:
			if tweet['id'] in recent_id_list:
				id_hit = True
				break
			search_result.append(tweet)
		if id_hit == True:
			break
		time.sleep(0.3)
	return search_result

def GetTweetIDList(tweet_list):
	id_list = []
	for tweet in tweet_list:
		id_list.append(tweet['id'])
	return id_list

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'usage: %s "search string"' % (sys.argv[0], )
		exit(1)
	search_string = sys.argv[1]
	state = StateLoad(StateFileName)
	if search_string not in state:
		state[search_string] = []
	tweet_list = TwitterSearch(search_string, MaxSearchDepth, state[search_string])
	state[search_string].extend(GetTweetIDList(tweet_list))
	if len(state[search_string]) > MaxRecentTweetIDLength:
		state[search_string] = state[search_string][-MaxRecentTweetIDLength:]
	StateSave(StateFileName, state)
	for one_tweet in tweet_list:
		print json.dumps(one_tweet)
