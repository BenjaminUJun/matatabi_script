# -*- coding: utf-8 -*-
import sys
import os
import datetime
import time
import re
import email
from email import utils
from email.parser import HeaderParser

def parse_file(file_path, output):
	print file_path 
	print output
	try:
		f = open(file_path, 'r')
		msg = email.message_from_file(f)
		f.close()
	except:
		return


	parser = email.parser.HeaderParser()
	headers = parser.parsestr(msg.as_string())

	for h in headers.items():
		if h[0] == "Received":
			# get date
			received = h[1].split(";")
			print received
			if len(received) < 2:
				continue

			date = received[1].strip()
			d = utils.parsedate(date)
			if d:
				date = int(time.mktime(d))
			received_origin = received[0]
			received = received[0].split(" ")

			# regexp for ip addr
			re_addr = re.compile("^(\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(\d|[01]?\d\d|2[0-4]\d|25[0-5])$")
			re_addr2 = re.compile("^\((\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(\d|[01]?\d\d|2[0-4]\d|25[0-5])\)$")
			re_addr3 = re.compile("^(\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(\d|[01]?\d\d|2[0-4]\d|25[0-5])\(")
			fqdn = ""

			if received[0].find("from") != -1:
				if received[1].find("[") >= 0:
					# for parse
					received.insert(1, "")
					received[2] = "(" + received[2] + ")"
				elif re_addr.match(received[1]):
					# for parse
					received.insert(1, "")
					received[2] = "([" + received[2] + "])"
				elif re_addr2.match(received[1]):
					# for parse
					received.insert(1, "")
					received[2] = received[2].replace("(","([").replace(")","])") 
				elif re_addr3.match(received[1]):
					# for parse
					received.insert(1, "")
					received[2] = "([" + received[2].split("(")[0] + "])"
				else:
					fqdn = received[1].strip("()[]\n")
			else:
				continue

			# get ptr and ipaddr
			ptr = ""
			ipaddr = ""

			if len(received) > 3 and received[2].find("(") >= 0 and fqdn != "unknown":
				if received[2].find("[") == -1:
					ptr = received[2].strip("()\n")
				if received[3].find("[") >= 0:
					ipaddr = received[3].strip("()[]\n")
				else:
					re_addr = re.compile("\[(.+)\]")
					search = re_addr.search(received[2])
					if search:
						ipaddr = search.group(1)

			output.write("%s %s %s %s %s\n" % (date,ipaddr,fqdn,ptr,file_path))

def parse_all_file(dir_path, mtime, output):
    file_list = []
    print dir_path
    for path, sbdir, files in os.walk(dir_path):
        dir_list = os.listdir(path)
	print dir_list
        for dir_elem in dir_list:
            abstruct_path = os.path.join(path, dir_elem)
            if os.path.isfile(abstruct_path):
                file_list.append((abstruct_path, time.strftime('%Y%m%d',(time.localtime(os.path.getmtime(abstruct_path))))))

    file_list = sorted(file_list, key=lambda a: a[1], reverse=True)
    file_list = filter(lambda a: a[1] == mtime, file_list)

    if len(file_list) == 0: return mtime
    with open(output, 'w') as output:
        for path in file_list:
            parse_file(path[0], output)
    return file_list[0][1]

def write_pid(pidfile):
    if not pidfile:
        return False
    if os.path.isfile(pidfile) is True:
        return False

    pid = os.getpid()
    fp = open(pidfile, "w")
    try:
        fp.write(str(pid))
    	return True
    finally:
        fp.close()

if __name__ == '__main__':
	spam_directory = sys.argv[1]
	date = sys.argv[2]

	try:
		print "try"
		spam_analyze = './tmp/spam_intermediate_data/'
		pidfile = spam_analyze + 'spam.pid' 
		if write_pid(pidfile) is True:
			latest = parse_all_file(spam_directory, date, spam_analyze + date + ".output")
	finally:
		os.remove(pidfile)

