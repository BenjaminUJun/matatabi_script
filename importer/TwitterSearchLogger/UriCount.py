#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import re
import requests

def URICount(fp):
	words = {}
	url_regex = re.compile("://")
	chomp_str = u'\u2026'.encode('utf-8')
	while True:
		line = fp.readline()
		if line is None or line == "":
			break
		line = line.replace("\\n", " ")
		for word in re.split('[\s#]', line):
			if url_regex.search(word) is None:
				continue
			if chomp_str in word:
				continue
			if word not in words:
				words[word] = 1
			else:
				words[word] += 1
	return words

def DictionarySort(dic):
        sorted_list = []
        for key, value in sorted(dic.items(), key=lambda x: x[1], reverse=True):
                sorted_list.append((key, value))
        return sorted_list

if __name__ == '__main__':
	words = URICount(sys.stdin)
	sorted_list = DictionarySort(words)[:10]
	for tp in sorted_list:
		orig_uri = tp[0].decode('utf-8')
		count = tp[1]
		summary_text = "{0} {1}".format(count, orig_uri.encode('utf-8'))
		try:
			r = requests.get(orig_uri, timeout=2)
			url = r.url
			if url != orig_uri:
				summary_text = "{0} {1}".format(count, url)
		except requests.exceptions.RequestException as e:
			#msg = e.message
			#summary_text += " {0}".format(msg)
			pass
		summary_text += "  "
		print summary_text
