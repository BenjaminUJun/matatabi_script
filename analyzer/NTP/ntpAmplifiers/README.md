# Module Name
- ntpAmplifiers

# Module File Name
- findNtpAmplifiers.py

# Input Dataset
- Netflow or sflow data set on Hive/Presto

# Output
- List of IP addresses sending 468 bytes NTP packets, which is the typical size for the NTP monlist option used for amplification attacks. The results are stored in the 'ntpamplifiers' hive table.

# Execution

```
# python findNtpAmplifiers.py sflow_or_netflow_table [year month day]
```
