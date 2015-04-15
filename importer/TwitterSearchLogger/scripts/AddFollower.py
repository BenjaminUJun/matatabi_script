#!/usr/bin/env python
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
import re

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

def ReadHitUsers(file_name):
	fp = open(file_name, "r")
	pattern = re.compile('"(\S+)"')
	users = {}
	while True:
		line = fp.readline()
		if line is None or line == '':
			break
		match_result = pattern.search(line)
		if match_result is None:
			continue
		user_name = match_result.group(1)
		if user_name in users:
			users[user_name] += 1
		else:
			users[user_name] = 1
	fp.close()
	return users

def SortUsers(user_map):
	sorted_user_name_list = []
	for key, _ in sorted(user_map.items(), key=lambda x: x[1], reverse=True):
		sorted_user_name_list.append(key)
	return sorted_user_name_list

def ReadAllFriendScreenName(twitter):
	cursor = "-1"
	friend_screen_name_url = "https://api.twitter.com/1.1/friends/list.json"
	friend_screen_name_list = []
	while cursor != "0":
		target_url = "%s?cursor=%s" % (friend_screen_name_url, cursor)
		req = twitter.get(target_url)
		if req.status_code != 200:
			print "req.status_code != 200 (%d): %s" % (req.status_code, req.text)
			return []
		obj = json.loads(req.text)
		cursor = obj['next_cursor_str']
		for user in obj['users']:
			friend_screen_name_list.append(user['screen_name'])
	return friend_screen_name_list

def FilterAlreadyFollowedUsers(followed_user_list, target_user_list):
	result = []
	for target_user in target_user_list:
		hit = False
		for followed_user in followed_user_list:
			if followed_user == target_user:
				hit = True
				break
		if hit:
			continue
		result.append(target_user)
	return result

def AddFriend(twitter, screen_name):
	api_url = "https://api.twitter.com/1.1/friendships/create.json"
	data = {'screen_name': screen_name, 'follow': True}
	req = twitter.post(api_url, data=data)
	if req.status_code != 200:
		print "follow %s failed: %s" % (screen_name, req.text)
		return False
	return True

if __name__ == '__main__':
	screen_name_list_file_name = "screen_name_list.txt"
	if len(sys.argv) > 1:
		screen_name_list = sys.argv[1]
	users = ReadHitUsers(screen_name_list)
	sorted_users = SortUsers(users)
	twitter = GetOAuthSession()
	followed_users = ReadAllFriendScreenName(twitter)
	target_users = FilterAlreadyFollowedUsers(followed_users, sorted_users)[:20]
	for screen_name in target_users:
		print "following %s..." % (screen_name, )
		AddFriend(twitter, screen_name)
		time.sleep(10)
