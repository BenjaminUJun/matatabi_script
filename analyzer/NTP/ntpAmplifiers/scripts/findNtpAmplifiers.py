import sys
import os 
import datetime

import pandas as pd
from pyhive import presto

from hive_service import ThriftHive
from hive_service.ttypes import HiveServerException
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

outputDirectory = "data/"


def scrub(table_name):
    """
    Avoid injection with the table name
    """
    return ''.join( chr for chr in table_name if chr.isalnum() ) 

 

def findNtpAmplifiers(table,today=datetime.date.today(),verbose=False):
  """
  Find NTP amplifiers in the given traffic (table) and store the results in the 'ntpamplifiers' Hive table.
  """
  
  date  = "%d%02d%02d" % (today.year, today.month, today.day)
  table = scrub(table)


  ## set some variables regarding the input data
  if table.startswith("netflow"):
    dataType = "netflow"
    req0 = "select sa, sum(ibyt), sum(ipkt) from %s where sp=123 and dt='%s' and pr='UDP' and ibyt/ipkt=468 group by sa" % (table,date)
  elif table.startswith("sflow"):
    dataType = "sflow"
    req0 = "select srcip, sum(ipsize), count(*) from %s where udpsrcport=123 and ipprotocol=17 and ipsize=468 and dt='%s' group by srcip" % (table,date)
  else:
    sys.stderr.write("Data type unknown!")
    sys.exit(-1) 


  cursor = presto.connect('localhost').cursor()
  if verbose: sys.stdout.write("Looking for %s NTP amplifiers... (%s)\n" % (date,table))
    
  # get today's data
  cursor.execute(req0)
  res = cursor.fetchall()

  if len(res)==0:
	return

  data = pd.DataFrame(res,columns=["srcip", "nbbyt", "nbpkt"])

  # add the confidence score:
  data["confidence"] = "LOW"
  data.loc[data.nbpkt>=100,"confidence"] = "MED"
  data.loc[data.nbpkt>=1000,"confidence"] = "HIGH"

  outputFile = open("%s/ntpamplifiers_%s_%s.txt" % (outputDirectory,table,date),"w")
  data.to_csv(outputFile,sep="\t",header=False,cols=["srcip","nbbyt","nbpkt","confidence"],index=False)
  outputFile.close()

  # Store results in Hive 
  try:
      transport = TSocket.TSocket('localhost', 10000)
      transport = TTransport.TBufferedTransport(transport)
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
 
      client = ThriftHive.Client(protocol)
      transport.open()

      client.execute("create table if not exists ntpamplifiers (srcip string, byte bigint,  pkt bigint, confidence string) partitioned by(dt string, dataSrc string) row format delimited fields terminated by '\t'");
      client.execute("load data local inpath '{dir}/ntpamplifiers_{table}_{date}.txt' overwrite into table ntpamplifiers partition (dt='{date}', dataSrc='{table}')".format(table=table,date=date,dir=outputDirectory))
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
  
  findNtpAmplifiers(table,today)


