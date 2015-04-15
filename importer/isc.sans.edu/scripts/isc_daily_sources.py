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

# Initialisation of the SANS ISC URL and directory where data will be downloaded (make sure this directory exist)

ipList = "https://isc.sans.edu/feeds/daily_sources"
downloadDirectory = "../data/"


def downloadIPList():
    """
    Download the ipList to the given directory
    """
    
    tmpFile = downloadDirectory+"dl_"+str(datetime.datetime.today()).replace(" ","_")
    urllib.urlretrieve(ipList, tmpFile)

    return tmpFile


def strip0(num):
    """
    Remove 0 in front of numbers
    """
    if num == "000":
        return "0"
    else:
        return num.lstrip("0")


def convert2csv(inputFilename):
    """
    Convert the given file to CSV format and write the output to 'outputFilename'
    """
    
    inputFile = open(inputFilename,"r")
    outputFilename = ""
    outputFile = None

    for line in inputFile:
        if line.startswith("#"):    # Header
            if line.startswith("# updated "):
                tmp = line.split(" ")[2]
                tmp = tmp.split("-")
                date = datetime.date(int(tmp[0]),int(tmp[1]),int(tmp[2]))-datetime.timedelta(1)
                dt = "%04d%02d%02d" % (date.year,date.month,date.day)
                outputFilename = downloadDirectory+dt+".csv"
                if os.path.exists(outputFilename):
                    sys.stderr.write("Error: This data have been already processed? %s\n" % outputFilename)
                    outputFilename+= "_"+str(int(random.random()*1000000))
                
                outputFile = open(outputFilename,"w")

        else:
            (ip, port, proto, reports, targets, firstseen, lastseen) = line.split()
            ipPart = ip.split(".")
            ip = "%s.%s.%s.%s" % (strip0(ipPart[0]),strip0(ipPart[1]),strip0(ipPart[2]),strip0(ipPart[3]))
            hostname = ""
            if int(targets)>19:
            	try: 
                	hostname = socket.gethostbyaddr(ip)[0]
            	except Exception as e:
			pass
                	#print "%s, IP=%s " % (e,ip)

            outputFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (ip, port, proto, reports, targets, firstseen, lastseen, hostname))

    outputFile.close()
    inputFile.close()

    return (outputFilename, dt)
    


if __name__ == "__main__":
    ###
    ### Main function gets the current IP list and upload it to the Hive database
    ###
    
    tmpFilename = downloadIPList()
    (csvFilename, dt) = convert2csv(tmpFilename)

    # upload data to the Hive server

    try:
        transport = TSocket.TSocket('localhost', 10000)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
 
        client = ThriftHive.Client(protocol)
        transport.open()

        client.execute("create table if not exists isc_daily_sources (source_ip string, target_port int, protocol int,  reports bigint, targets bigint, first_seen string, last_seen string, hostname string) partitioned by(dt string) row format delimited fields terminated by '\t'");
        client.execute("load data local inpath '{csvFile}' overwrite into table isc_daily_sources partition (dt='{date}')".format(csvFile=csvFilename,date=dt))
        transport.close()

    except Thrift.TException, tx:
        sys.stderr.write('%s\n' % (tx.message))


