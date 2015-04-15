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
import datetime

output_file_prefix = ""
output_file = {}

def GetOutputFile(date):
	if date in output_file:
		return output_file[date]
	f = open("%s_%s.line_json" % (output_file_prefix, date), "a")
	output_file[date] = f
	return f

if __name__ == '__main__':
	re_clear_domain = re.compile("/.*")
	re_clear_path = re.compile(".*?/")
	output_file_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	if len(sys.argv) > 1:
		output_file_prefix = sys.argv[1]
	output_file_prefix = "%s" % (output_file_prefix, )
	for line in sys.stdin:
		obj = json.loads(line)
		obj['ASName'] = obj['AS name']
		obj['date'] = obj['date'].replace('-', '')
		del obj['AS name']
		date = obj['date']
		obj['dt'] = date.replace('-', '')
		del obj['date']
		if len(date) > 8:
			date = date[:8]
		obj['url'] = obj['domain']
		obj['path'] = re_clear_path.sub('/', obj['domain'], 1)
		obj['domain'] = re_clear_domain.sub('', obj['domain'])
		f = GetOutputFile(date)
		if f is None:
			print "FATAL: output file for %s is not opend"
			sys.exit(1)
		f.write(json.dumps(obj))
		f.write("\n")
	for date in output_file:
		f = output_file[date]
		f.close()
		dstdir = "HIVE_TABLE_PATH"
		filename = "%s_%s.line_json" % (output_file_prefix, date)
		print "hdfs dfs -mkdir -p \"%s/dt=%s\"" % (dstdir, date)
		print "hdfs dfs -put %s \"%s/dt=%s/%s\"" % (filename, dstdir, date, filename)
		print "hive -e \"ALTER TABLE MALC0DE_TABLE_NAME ADD IF NOT EXISTS PARTITION(dt='%s');\"" % (date, )
