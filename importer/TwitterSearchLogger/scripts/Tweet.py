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

status_update_url = "https://api.twitter.com/1.1/statuses/update.json"

def GetOAuthSession():
	consumer_key = 'TWITTER_CONSUMER_KEY'
	consumer_secret = 'TWITTER_CONSUMER_SECRET'
	access_key = 'TWITTER_ACCESS_KEY'
	access_secret = 'TWITTER_ACCESS_SECRET'
	return OAuth1Session(consumer_key, consumer_secret, access_key, access_secret)

if __name__ == '__main__':
	twitter = GetOAuthSession()
	text = sys.stdin.read()
	data = {
		'status': text
	}
	twitter.post(status_update_url, data=data)
