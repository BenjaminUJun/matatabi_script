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

StateFileName = "State_malc0de.pickle"

def StateSave(filename, data):
	fp = open(filename, "w")
	fcntl.lockf(fp, fcntl.LOCK_EX)
	pickle.dump(data, fp)
	fcntl.lockf(fp, fcntl.LOCK_UN)
	fp.close()

def StateLoad(filename):
	if not os.path.exists(filename):
		return []
	fp = open(filename, "r")
	fcntl.lockf(fp, fcntl.LOCK_SH)
	obj = pickle.load(fp)
	fcntl.lockf(fp, fcntl.LOCK_UN)
	fp.close()
	return obj

def HttpGet(url):
	return requests.get(url).text

# "<a href="XXX">YYY</a>" -> YYY
def SplitHref(html):
	m = re.search(r'<a\s+.*?>(.+?)</a>', html)
	return m.group(1)

def HtmlToMalc0deDatabase(buf):
	obj_list = []
	buf = buf.replace("\r\n", "").replace("\n", "").replace("\r", "")
	for block in re.finditer(r'<tr\s+class="class1">(.+?)</tr>', buf):
		target = block.group(0)
		target = target.replace('<br/>', "")
		tmp_list = []
		for tr in re.finditer(r'<td>(.+?)</td>', target):
			tmp_list.append(tr.group(1))
		if len(tmp_list) < 7:
			continue
		block_obj = {}
		block_obj["date"] = tmp_list[0]
		block_obj["domain"] = tmp_list[1]
		block_obj["ip"] = SplitHref(tmp_list[2])
		block_obj["CC"] = SplitHref(tmp_list[3])
		block_obj["ASN"] = SplitHref(tmp_list[4])
		block_obj["AS name"] = SplitHref(tmp_list[5])
		block_obj["md5"] = SplitHref(tmp_list[6])
		obj_list.append(block_obj)
	return obj_list

def FilterNewList(old_list, obj_list):
	old_dic = {}
	for old_obj in old_list:
		old_dic[old_obj['md5']] = old_obj
	new_list = []
	for obj in obj_list:
		if obj['md5'] not in old_dic:
			new_list.append(obj)
	return new_list

if __name__ == '__main__':
	old_list = StateLoad(StateFileName)
	buf = HttpGet("http://malc0de.com/database/")
	obj_list = HtmlToMalc0deDatabase(buf)
	new_list = FilterNewList(old_list, obj_list)
	StateSave(StateFileName, obj_list)
	if len(new_list) > 0:
		print json.dumps(new_list)
