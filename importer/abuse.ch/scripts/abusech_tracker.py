#!/usr/bin/python

import urllib
import sys
import os
import datetime
import random
import socket

from hive_service import ThriftHive
from hive_service.ttypes import HiveServerException
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

# Initialisation of trackers name, URL and directories where data will be downloaded (make sure these directories exist)
allTrackerName = ["palevo","zeus","spyeye","feodo"]
allIpList = ["https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist","https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist","https://spyeyetracker.abuse.ch/blocklist.php?download=ipblocklist","https://feodotracker.abuse.ch/blocklist/?download=ipblocklist"]
allDownloadDirectory = ["abusech/palevo/","abusech/zeus/","abusech/spyeye/","abusech/feodo/"]


def downloadIPList(ipList,downloadDirectory):
    """
    Download the ipList to the given directory
    """
    
    
    tmpFile = downloadDirectory+"dl_"+str(datetime.datetime.today()).replace(" ","_")
    urllib.urlretrieve(ipList, tmpFile)

    return tmpFile


def convert2csv(inputFilename,outputFilename):
    """
    Convert the given file to CSV format and write the output to 'outputFilename'
    """
    
    inputFile = open(inputFilename,"r")
    if os.path.exists(outputFilename):
        sys.stderr.write("Error: This data have been already processed? %s\n" % outputFilename)
        outputFilename+= "_"+str(int(random.random()*1000000))
                
    outputFile = open(outputFilename,"w")
   
    for line in inputFile:
        if line.startswith("#"):    #Skip the header
            continue
        else:
            ip = line.strip()
            hostname = ""
            try: 
                hostname = socket.gethostbyaddr(ip)[0]
            except Exception as e:
		pass
                #print "%s, IP=%s " % (e,ip)

            outputFile.write("%s\t%s\n" % (ip, hostname))

    outputFile.close()
    inputFile.close()

    return outputFilename

if __name__ == "__main__":
    ###
    ### Main function gets the current C&C list and upload it to the Hive database
    ###
    
    yesterday = datetime.date.today() - datetime.timedelta(1)
    dt = "%04d%02d%02d" % (yesterday.year,yesterday.month,yesterday.day)

    for tracker, ipList, dlDirectory in zip(allTrackerName,allIpList,allDownloadDirectory):
        print "Processing %s ..." % tracker

        tmpFilename = downloadIPList(ipList,dlDirectory)
        outputFilename = dlDirectory+dt+".csv"
        csvFilename = convert2csv(tmpFilename,outputFilename)

        # upload data to the Hive server

        try:
            transport = TSocket.TSocket('localhost', 10000)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
 
            client = ThriftHive.Client(protocol)
            transport.open()

            client.execute("create table if not exists abusech_%s_tracker (cc_ip string, hostname string) partitioned by(dt string) row format delimited fields terminated by '\t'" % tracker);
            client.execute("load data local inpath '{csvFile}' overwrite into table abusech_{tracker}_tracker partition (dt='{date}')".format(csvFile=csvFilename,date=dt,tracker=tracker))
            transport.close()

        except Thrift.TException, tx:
            sys.stderr.write('%s\n' % (tx.message))


