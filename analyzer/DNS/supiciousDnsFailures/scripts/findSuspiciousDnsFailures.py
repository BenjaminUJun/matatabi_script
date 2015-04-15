import sys
import networkx as nx
from networkx.algorithms import bipartite
from pyhive import presto
import pickle
import numpy as np
from collections import Counter
import community
import datetime

from hive_service import ThriftHive
from hive_service.ttypes import HiveServerException
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

ignoredDomains = set(["\.sophosxl\.net\.","\.mcafee\.com\.","\.in-addr\.arpa\.","\.ip6\.arpa\.","\.spamhaus\.org\.","whoami\.akamai\.net\.","\.mailshell\.net\.","\.rbl\.jp\."])

outputDirectory = "data/"

def makeGraph(table,dt):
  """
  Build the entire failure graph with all DNS errors found in the table at the given date.
  """
    
  sys.stderr.write("Build the graph. ")
  # Get DNS failed requests
  req0 = "select dst, dns_question from %s where dns_rcode!='NOERROR' and ( dns_question like '%% A' or dns_question like '%% AAAA' ) and dt='%s' " % (table,dt);

  # Ignored certain request (antivirus,...)
  for fqdn in ignoredDomains:
    req0 += " and  not regexp_like(dns_question, '(?i).*%s .*') " % fqdn 

  #print req0
  cursor = presto.connect('localhost').cursor()
  cursor.execute(req0)

  #Make the corresponding failure graph
  G = nx.Graph()
  count = 0
  for data in cursor:
    addr = data[0]
    if data[1] is None:
      continue
    ques = data[1].split()[0]

    G.add_node(addr,bipartite=0)
    G.add_node(ques,bipartite=1)
    G.add_edge(addr,ques)
  
  return G



def trimGraph(G,degree):
  """
  Remove nodes from the graph 'G' whose degree is lower than 'degree'
  """
  
  remove = [node for node,degree in G.degree().items() if degree < degree]
  G.remove_nodes_from(remove)
  return G

def saveGraph(G,filename):
  """
  Store the graph 'G' in a pickle file
  """
    
  with open(filename,"wb") as fp:
    pickle.dump(G,fp)

def loadGraph(filename):
  """
  Load the graph stored in the given pickle file
  """
  with open(filename,"rb") as fp:
    return pickle.load(fp)

def communityMining(G, minCommSize=10):
  """
  Find communities in the graph 'G' with more than 'minCommSize' nodes.
  """
  count = 0
  dendrogram = community.generate_dendrogram(G)
  firstPartition = community.partition_at_level(dendrogram,0)
  
  sys.stderr.write("Prune sparse clusters. ")
  #remove early small communities 
  sparseComm = set([k for k,v in Counter(firstPartition.values()).iteritems() if v<minCommSize])
  nodes = [node for node in G.nodes() if firstPartition[node] in sparseComm]
  G.remove_nodes_from(nodes)

  sys.stderr.write("Find communities. ")
  # Partition again the graph and report big communities:
  dendrogram = community.generate_dendrogram(G)
  partition = community.partition_at_level(dendrogram,len(dendrogram)-2)
  allfqdns =  set(n for n,d in G.nodes(data=True) if d['bipartite']==1)
  allHosts = set(n for n,d in G.nodes(data=True) if d['bipartite']==0)
  size = float(len(set(partition.values())))
  communities = []
  
  bigComm = [k for k,v in Counter(partition.values()).iteritems() if v>minCommSize]
  for com in bigComm :
    comfqdns = [nodes for nodes in allfqdns if partition[nodes] == com]
    comHosts = [nodes for nodes in allHosts if partition[nodes] == com]
    comm = G.subgraph(comfqdns+comHosts) 
    if comm.order() < minCommSize :
        sys.stderr("Remove small community (This shouldn't happen here?)\n")
        continue

    communities.append(comm)
    
  return communities 


def printCommunities(comm):
  """
  Print characteristics of the given communities.
  """
  
  print "Found %s communities" % len(comm) 

  for commId, G in enumerate(comm):
    comfqdns =  set(n for n,d in G.nodes(data=True) if d['bipartite']==1)
    comHosts = set(n for n,d in G.nodes(data=True) if d['bipartite']==0)
    nbfqdn = len(comfqdns)
    nbHost = len(comHosts)

    degfqdn = np.mean(map(G.degree,comfqdns))
    degHost = np.mean(map(G.degree,comHosts))

    dhr,dfr = dominantRatio(G)

    print "#%s\t %s fqdns (degree: %s, entropy: %s), %s hosts (degree: %s, entropy: %s)" % (commId,nbfqdn,degfqdn,dfr,nbHost,degHost,dhr)

def printCommunity(G):
    """
    List all members of the given community.
    """
    
    for node in G.nodes():
        print node


def plotCommunity(G,label=False):
  """
  Plot the given community with networkx plotting functions.
  """
  
  allHosts = set(n for n,d in G.nodes(data=True) if d['bipartite']==0)
  allfqdns = set(n for n,d in G.nodes(data=True) if d['bipartite']==1)
  pos = nx.spring_layout(G)

  nx.draw_networkx_nodes(G,pos,allHosts,node_color="b",node_shape="s")
  nx.draw_networkx_nodes(G,pos,allfqdns,node_color="r")
  if label:  nx.draw_networkx_labels(G,pos)
  nx.draw_networkx_edges(G,pos)
    

def dominantRatio(G):
  """
  Compute the dominant ratio of a community.
  """
  
  allHosts = set(n for n,d in G.nodes(data=True) if d['bipartite']==0)
  allfqdns = set(n for n,d in G.nodes(data=True) if d['bipartite']==1)

  A = bipartite.biadjacency_matrix(G,allHosts,allfqdns)
  
  p = A/np.sum(A)

  pf = np.sum(p,0)
  ph = np.sum(p,1)

  #compute dhr
  if np.size(ph) == 1:
      dhr = 0
  else:
      dhr = -np.sum(np.multiply(ph,np.log(ph)))/np.log(np.size(ph))

  #compute ddr
  if np.size(pf) == 1:
      dfr = 0
  else:
      dfr = -np.sum(np.multiply(pf,np.log(pf)))/np.log(np.size(pf))


  return dhr, dfr



def allDominantRatio(comm,minCommSize=100):
    """
    Compute the dominant ratio for all comunities with more than 'minCommSize' nodes.
    """
  
    allDr = np.zeros((2,len(comm)))

    for i, G in enumerate(comm):
        if G.order() < minCommSize:
          allDr[:,i] = np.nan
        else:
          allDr[:,i] = dominantRatio(G)

    return allDr


def reportCommunities(table,dt,comm):
    """
    Output the detected communities to the suspiciousdnsfailures Hive table
    """
    
    sys.stderr.write("Report suspicious IPs.\n")
    outputFile = open("%s/suspiciousdnsfailures_%s_%s.txt" % (outputDirectory,table,dt), "w")

    for commId, G in enumerate(comm):

        comfqdns =  set(n for n,d in G.nodes(data=True) if d['bipartite']==1)
        degrees = bipartite.degree_centrality(G,comfqdns)
        
        for e in G.edges():
            # Compute all fields to store in the DB
            if G.node[e[0]]["bipartite"] == 0 and  G.node[e[1]]["bipartite"] == 1: 
                srcip = e[0]
                fqdn  = e[1]
            elif  G.node[e[0]]["bipartite"] == 1 and  G.node[e[1]]["bipartite"] == 0:
                srcip = e[1]
                fqdn  = e[0]
            else:
                sys.stderr.write("Error: Invalid edge (%s)\n" % e)

            degree = degrees[e[0]]+degrees[e[1]]/2.0

            conf = "LOW"
            if degree > 0.66:
                conf = "HIGH"
            elif degree > 0.33:
                conf = "MED"

            outputFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n" % (fqdn,srcip,commId,G.order(),degree,conf,table))

    outputFile.close()

    # Store results in Hive 
    try:
      transport = TSocket.TSocket('localhost', 10000)
      transport = TTransport.TBufferedTransport(transport)
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
 
      client = ThriftHive.Client(protocol)
      transport.open()

      client.execute("create table if not exists suspiciousdnsfailures (fqdn string, srcip string, clusterid int, clustersize bigint, degree double, confidence string, table string) partitioned by(dt string) row format delimited fields terminated by '\t'");
      client.execute("load data local inpath '{dir}/suspiciousdnsfailures_{table}_{date}.txt' into table suspiciousdnsfailures partition (dt='{date}')".format(date=dt,dir=outputDirectory,table=table))


#create table suspiciousdnsfailuresIP_dns_pcaps (ip1 string, ip2 string, fqdn_overlap int) partitioned by (dt string);

      #client.execute("insert table suspiciousdnsfailuresIP partition (dt='{date}') select t1.srcip, t2.srcip, count(*)  from suspiciousdnsfailures as t1 join suspiciousdnsfailures as t2 on (t1.clusterid=t2.clusterid and t1.fqdn=t2.fqdn and t1.dt='{date}' and t2.dt='{date}') where t1.srcip!=t2.srcip and t1.table='{table}' and t2.table='{table}' group by t1.srcip, t2.srcip".format(table=table,date=dt))
      #transport.close()

    except Thrift.TException, tx:
      sys.stderr.write('%s\n' % (tx.message))

        
        

def detectSuspiciousRequests(table, today=datetime.date.today(),minCommSize=10):
  """
  Detect suspicious groups of IP addresses with similar DNS failures in the given Hive table.
  """

  date  = "%d%02d%02d" % (today.year, today.month, today.day)

  # Get data from Presto and make the graph
  G = makeGraph(table, date)

  # Find clusters
  comm = communityMining(G,minCommSize)

  # Write results to the Hive database
  reportCommunities(table,date,comm)


def scrub(table_name):
    """
    Avoid injection with the table name
    """
    return ''.join( chr for chr in table_name if chr.isalnum() ) 


if __name__ == "__main__":

  if len(sys.argv) < 2:
    print "usage: python %s TABLE [year month day]" % (sys.argv[0])
    sys.exit(-1)

  if len(sys.argv) > 2:
    today = datetime.date(int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
  else:
    today = datetime.date.today()

  table = scrub(sys.argv[1])
  
  detectSuspiciousRequests(table,today)