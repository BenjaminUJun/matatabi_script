import sys
from pyhive import presto
import datetime
import matplotlib.pylab as plt
import pandas as pd

# Find NTP amplifiers from netflow data
def find_amplifiers():
    
    # Find NTP amplifiers and keep ip in Hive Table
    req = "create table ntp_amplifiers as "
    req += "select sa from netflow where sp=123 and pr='UDP' and ibyt/ipkt=468 group by sa"

    cursor = presto.connect('localhost').cursor()
    cursor.execute(req)


# Find DDoS victims from netflow data
def find_victims():

    # Request the data
    req = "select da, sum(ibyt) as vol from netflow where sa in (select sa from ntp_amplifiers ) group by da order by vol desc"
    cursor = presto.connect('localhost').cursor()
    cursor.execute(req)
    res = cursor.fetchall()

    for i in range(3):
        print res[i]
        plot_traffic_volume(res[i])

# Plot the traffic volume for the given IP
def plot_traffic_volume(ip):

    # Request the data
    req = "select ts, ibyt from netflow where sa = '{0}' or da = '{0}'".format(ip)
    cursor = presto.connect('localhost').cursor()
    cursor.execute(req)
    res = cursor.fetchall()

    # Pre-process for ploting
    data = pd.DataFrame(res,columns=["ts", "bytes"])
    data.index = pd.to_datetime(data.pop("ts"), unit="s")
    data = data.resample('H',how="sum")
    ix = pd.DatetimeIndex(start=data.index[0]-datetime.timedelta(0.5), end=data.index[-1]+datetime.timedelta(0.5), freq='H')
    data = data.reindex(ix)
    data.bytes = data.bytes.fillna(0)

    # Plot the data
    plt.figure()
    data.plot(lw=2)
    plt.grid(True)
    plt.savefig("traffic_volume_%s.png" % ip)
    plt.close()

# Main program
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "usage: {0} [amp|vic]".format(sys.argv[0])
        quit()

    if sys.argv[1] == "amp":
        find_amplifiers()

    if sys.argv[1] == "vic":
        find_victims()
