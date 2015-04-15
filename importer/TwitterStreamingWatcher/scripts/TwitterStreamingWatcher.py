#!/usr/bin/env python
#-*- coding:utf-8 -*-

from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from tweepy.api import API
import json
import sys
import signal
import os
import daemon

PID_FILE_NAME="stream_bot.pid"

def get_oauth():
    consumer_key = 'TWITTER_CONSUMER_KEY'
    consumer_secret = 'TWITTER_CONSUMER_SECRET'
    access_key = 'TWITTER_ACCESS_KEY'
    access_secret = 'TWITTER_ACCESS_SECRET'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth

class Listener(StreamListener):
    def __init__(self):
	super(Listener, self).__init__()
	self.output_files = []
	self.output_filenames = []

    def CloseOutputFiles(self):
	i = 0
	for filename in self.output_filenames:
		i += 1
		if filename == "-":
			continue
		if len(self.output_files) > i:
			self.output_files[i].close()
    def OpenOutputFiles(self):
	self.output_files = []
	for filename in self.output_filenames:
		if filename == "-":
			self.output_files.append(sys.stdout)
		else:
			self.output_files.append(open(filename, "a"))

    def SetOutputFilenames(self, output_filenames=None):
	self.CloseOutputFiles()
	if output_filenames is None:
		output_filenames = []
	self.output_filenames = output_filenames
	self.OpenOutputFiles()

    def ReloadOutputFiles(self):
	self.CloseOutputFiles()
	self.OpenOutputFiles()

    """ Let's stare abstractedly at the User Streams ! """
    def on_status(self, status):
	dump_text = json.dumps(status._json) + "\n"
	if self.output_files is None:
		print dump_text
		sys.stdout.flush()
		return
	for file in self.output_files:
		file.write(dump_text)
		file.flush()

listener = Listener()

def SigHupHandler(signum, frame):
	listener.ReloadOutputFiles()

if __name__ == '__main__':
    signal.signal(signal.SIGHUP, SigHupHandler)
    auth = get_oauth()
    listener.SetOutputFilenames(sys.argv[1:])
    stream = Stream(auth, listener, secure=True)
    daemon.daemonize(PID_FILE_NAME)
    stream.userstream()
