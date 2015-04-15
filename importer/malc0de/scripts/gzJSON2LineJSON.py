#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests # pip install requests
import re
import json
import sys
import os
import signal
import pickle
import posixfile
import fcntl
import time
from pyhive import presto
import gzip

def ReadGZFile(filename):
	f = gzip.open(filename, 'rb');
	content = f.read()
	f.close()
	return content

def LoadJSON_GZ(filename):
	content = ReadGZFile(filename)
	if "u'" in content:
		return eval(content)
	return json.loads(content)

if __name__ == '__main__':
	for filename in sys.argv[1:]:
		obj_list = LoadJSON_GZ(filename)
		for obj in obj_list:
			print json.dumps(obj)

