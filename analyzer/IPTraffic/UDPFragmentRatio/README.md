# Module Name
- UDP Fragmentation Analyzer

# Module File Name
- udp-fragment-daily.rb

# Descriptoin
- The module analzyes ratio of fragmented UDP flows in daily sflow dataset.

# Input Dataset
- sflow data set on MATATABI

# Output
- output fragmented UDP flow ratio in the give date and sflow dataset

```
<date>,<total flow>,<udp flow>,<fragmented udp flow>,<fragment ratio (fragmented udp flow/udp flow * 100 [%])>
20150412,2011664,597507,962,0.161
```

# Hive Command
- select srcip,count(*) as "number" from <sflow Table Name> where dt='<date>' and udpdstport=123 group by srcip order by "number" desc limit 10;

# Usage
- single shot running 

```
# ruby udp-fragment-daily.rb <sflow table name> <YYYYMMDD>
```

- use cron(8)

```
1 11 * * * ~/cron.sh
```


