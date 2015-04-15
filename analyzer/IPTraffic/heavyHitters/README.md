# Module Name
- heavyHitters

# Module File Name
- findHeavyHitters.py

# Input Dataset
- Netflow or sflow data set on Hive/Presto

# Output
- List of IP addresses sending an unusually high nunber of packets or bytes detected in the given netflow/sflow table. The results are stored in the 'suspiciousheavyhitters' hive table.

# Execution

```
# python findHeavyHitters.py sflow_or_netflow_table [year month day]
```
