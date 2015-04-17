# Module Name
- SSL flow analzyer

# Module File Name
- ssl\_dailyvolume_sflow.rb
- ssl\_dailyvolume_netflow.rb
- ssl\_dailysrclist_netflow.rb


# Input Dataset
- sflow/netflow data set on Hive/Presto

# Output
- ssl\_dailyvolume_sflow.rb
	- output the number of daily SSL flow in sflow dataset during given days

```
====<SFLOW TABLE NAME>====
20150406 1
20150407 3
20150408 2
20150409 3
20150410 4
20150411 2
20150412 2
20150413 3
20150414 6
==========================
```

- ssl\_dailyvolume_netflow.rb
	- output the number of daily SSL flow in netflow dataset during given days

```
====<NETFLOW TABLE NAME>====
20150406 1
20150407 3
20150408 2
20150409 3
20150410 4
20150411 2
20150412 2
20150413 3
20150414 6
==========================
```

- ssl\_dailysrclist_netflow.rb
	- output list of SSL speaker's IP in the given date

```
====<NETFLOW TABLE NAME>====
<Source IPv4 Address> <#flow>
==========================
```

# Usage
- ssl\_dailyvolume_sflow.rb

```
# ruby ssl_dailyvolume_sflow.rb <sflow table name> <days>
```

- ssl\_dailyvolume_netflow.rb

```
# ruby ssl_dailyvolume_netflow.rb <netflow table name> <days>
```

- ssl\_dailysrclist_netflow.rb


```
# ruby ssl_dailyvolume_netflow.rb <netflow table name> <date>
```



