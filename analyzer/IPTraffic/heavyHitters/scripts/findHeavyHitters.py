import sys
import os 
import datetime

import numpy as np
import pandas as pd
from pyhive import presto

from hive_service import ThriftHive
from hive_service.ttypes import HiveServerException
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

outputDirectory = "data/"

def confidence(pkt,avgpkt,stdpkt,byt,avgbyt,stdbyt):
  """
  Find the confidence level of a host sending 'pkt' packets and 'byt' bytes, knowing its usual packet and byte rate (i.e. average and standard deviation)
  """
  
  if pkt > avgpkt+10*stdpkt or byt > avgbyt+10*stdbyt:
    return "HIGH"
  elif pkt > avgpkt+5*stdpkt or byt > avgbyt+5*stdbyt:
    return "MED"
  elif pkt > avgpkt+3*stdpkt or byt > avgbyt+3*stdbyt:
    return "LOW"
  else:
    return ""
 
def scrub(table_name):
    """
    Avoid injection with the table name
    """
    return ''.join( chr for chr in table_name if chr.isalnum() ) 



def findHeavyHitters(table,today=datetime.date.today(),verbose=False):
  """
  Find heavy hitters in the given traffic (table) and store the results in the 'suspiciousheavyhitters' Hive table.
  """
  
  histNbDay = 15 
  date  = "%d%02d%02d" % (today.year, today.month, today.day)
  dates = list("%d%02d%02d" % (x.year, x.month, x.day) for x in pd.date_range(today-datetime.timedelta(histNbDay),today-datetime.timedelta(1)))
  table = scrub(table)

  ## set some variables regarding the input data
  if table.startswith("netflow"):
    dataType = "netflow"
    endpointTypes = [("dstip","da"),("srcip","sa")]
    req0 = "select {endpoint}, sum(ipkt) nbpkt, sum(ibyt) nbbyte from {table} where dt=%s group by {endpoint}"  
    req1 = "select {genericLabel}, avg(nbpkt) as avgpkt, stddev_samp(nbpkt) as stdpkt, avg(nbbyt) as avgbyt, stddev_samp(nbbyt) as stdbyt from(select {endpointType} as {genericLabel}, dt, sum(ipkt) as nbpkt, sum(ibyt) as nbbyt from {table} where {endpointType} IN ({suspiciousIP}) and dt IN ({dates}) group by {endpointType}, dt order by {endpointType}, dt) group by {genericLabel}"
  elif table.startswith("sflow"):
    dataType = "sflow"
    endpointTypes = [("dstip","dstip"),("srcip","srcip"),("dstip","dstip6"),("srcip","srcip6")] 
    req0 = "select {endpoint}, count(*) nbpkt, sum(ipsize) nbbyte from {table} where dt=%s and {endpoint}<>'' group by {endpoint}"
    req1 = "select {genericLabel}, avg(nbpkt) as avgpkt, stddev_samp(nbpkt) as stdpkt, avg(nbbyt) as avgbyt, stddev_samp(nbbyt) as stdbyt from(select {endpointType} as {genericLabel}, dt, count(*) as nbpkt, sum(ipsize) as nbbyt from {table} where {endpointType} IN ({suspiciousIP}) and dt IN ({dates}) group by {endpointType}, dt order by {endpointType}, dt) group by {genericLabel}" 
  else:
    sys.stderr.write("Data type unknown!")
    sys.exit(-1) 


  outputFile = open("%s/suspiciousheavyhitters_%s_%s.txt" % (outputDirectory,table,date), "w")
  cursor = presto.connect('localhost').cursor()
  for genericLabel, endpointType in endpointTypes:
    if verbose: sys.stdout.write("Looking for %s heavy hitters... (%s,%s)\n" % (date,table,genericLabel))
    suspiciousIP = set()
    # get today's data
    formatedReq = req0.format(endpoint=endpointType,table=table)
    cursor.execute(formatedReq, [date])
    res = cursor.fetchall()

    if len(res)==0:
	continue

    data = pd.DataFrame(res,columns=[genericLabel, "nbpkt", "nbbyt"])
    data.index = data.pop(genericLabel)

    # find today's heavy hitter
    for aggType in ["nbpkt","nbbyt"]:
       suspiciousIP.update(data.ix[data[aggType]>data[aggType].mean()+3*data[aggType].std()].index.tolist())

    # check in past data if they had similar behavior
    if verbose: sys.stdout.write("Retrieve past data...\n")
    suspiciousIP = list(suspiciousIP)
    for i in range(len(suspiciousIP))[::100]:
        susIP = suspiciousIP[i:i+100]
    	formatedReq1 = req1.format(genericLabel=genericLabel, endpointType=endpointType, table=table, suspiciousIP=str.translate(str(list(susIP)),None,"u[]"), dates=str.translate(str(dates),None,"u[]"))
    	cursor.execute(formatedReq1)
    	res = cursor.fetchall()

        if verbose: sys.stdout.write("Register suspicious IPs...\n")
        for ip, avgpkt, stdpkt, avgbyt, stdbyt in res:
          currData = data.ix[ip]
          if genericLabel == "dstip":
             dstip = ip
             srcip = ""
          else:
             dstip = "" 
             srcip = ip
          try:
            if currData["nbpkt"] > avgpkt+3*stdpkt or currData["nbbyt"] > avgbyt+3*stdbyt :
              outputFile.write("%s\t%s\t%s\t%s\t%s\t\n" % (srcip,dstip,currData["nbpkt"],currData["nbbyt"],confidence(currData["nbpkt"],avgpkt,stdpkt,currData["nbbyt"],avgbyt,stdbyt)))
          except TypeError:
            if verbose: sys.stdout.write("!!Warning!! no past data for %s (avgpkt=%s, stdpkt=%s, avgbyt=%s, stdbyt=%s)\n" % (ip, avgpkt, stdpkt, avgbyt, stdbyt))
            outputFile.write("%s\t%s\t%s\t%s\t%s\t\n" % (srcip,dstip,currData["nbpkt"],currData["nbbyt"],"MED"))
            continue

  outputFile.close()

  # Store results in Hive 
  try:
      transport = TSocket.TSocket('localhost', 10000)
      transport = TTransport.TBufferedTransport(transport)
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
 
      client = ThriftHive.Client(protocol)
      transport.open()

      client.execute("create table if not exists suspiciousheavyhitters (srcip string, dstip string, pkt bigint, byte bigint, confidence string) partitioned by(dt string, dataSrc string) row format delimited fields terminated by '\t'");
      client.execute("load data local inpath '{dir}/suspiciousheavyhitters_{table}_{date}.txt' overwrite into table suspiciousheavyhitters partition (dt='{date}', dataSrc='{table}')".format(table=table,date=date,dir=outputDirectory))
      transport.close()

  except Thrift.TException, tx:
      sys.stderr.write('%s\n' % (tx.message))


if __name__ == "__main__":
    
  if len(sys.argv) < 2:
    print "usage: python %s TABLE [year month day]" % (sys.argv[0])
    sys.exit(-1)

  if len(sys.argv) > 2:
    today = datetime.date(int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
  else:
    today = datetime.date.today()

  table = scrub(sys.argv[1])
  
  findHeavyHitters(table,today)


