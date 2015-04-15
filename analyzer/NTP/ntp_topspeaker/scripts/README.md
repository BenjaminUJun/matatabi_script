# Module Name
- ntp_topspeaker

# Module File Name
- ntp_topspeaker.rb

# Input Dataset
- sflow data set on Hive/Presto which imported by 

# Output
- output top 10 NTP speakers in the given sflow table and date (YYYYMMDD)

# Hive Command
- select srcip,count(*) as "number" from <sflow Table Name> where dt='<date>' and udpdstport=123 group by srcip order by "number" desc limit 10;

# Execution

```
# ruby ntp_topspeaker.rb <sflow table name> <YYYYMMDD>
```
