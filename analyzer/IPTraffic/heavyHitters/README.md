# Module Name
- heavyHitters

# Module File Name
- findHeavyHitters.py

# Input Dataset
- Netflow or sflow data set on Hive/Presto

# Output
- List of IP addresses sending an unusually high nunber of packets or bytes detected in the given netflow/sflow table.

# Hive Command
- select srcip,count(*) as "number" from <sflow Table Name> where dt='<date>' and udpdstport=123 group by srcip order by "number" desc limit 10;

# Execution

```
# python findHeavyHitters.py sflow_or_netflow_table [year month day]
```
