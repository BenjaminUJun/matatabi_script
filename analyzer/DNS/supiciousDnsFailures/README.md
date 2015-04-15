# Module Name
- suspiciousDnsFailures

# Module File Name
- findSuspiciousDnsFailures.py

# Input Dataset
- DNS dataset on Hive/Presto

# Output
- List of IP addresses with common DNS failures. This suspicious behavior is usual for botnets using DGA to find the C&C server. The results are stored in the 'suspiciousdnsfailures' hive table.

- This algorithm is strongly inspired from the following paper but relies on community mining instead of tri-nonnegative matrix factorization: 
Nan Jiang, Jin Cao, Yu Jin, Li Erran Li, and Zhi-Li Zhang. 2010. Identifying suspicious activities through DNS failure graph analysis. In Proceedings of the The 18th IEEE International Conference on Network Protocols (ICNP '10). IEEE Computer Society, Washington, DC, USA, 144-153. 

# Execution

```
# python findSuspiciousDnsFailures.py sflow_or_netflow_table [year month day]
```
