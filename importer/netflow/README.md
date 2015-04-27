# Module Name
- netflow importer

# Input Dataset
- binary netflow data captured by nfcapd (URL: http://nfdump.sourceforge.net/)
	- file name format: nfcapd.< YYYYMMDDHHMM >

# Description 
- The script imports daily netflow data which is gathered by nfcapd on a MATATABI table. The script use nfdump tool in the data conversion. The table definition is available on "schema" directory.


# Usage
- one shot (impport netflow files which gathered at the 1st argument date < YYYYMMDD >) 

```shell: 
# sh put-netflow.sh <YYYYMMDD>
```

- cron

```
* 11 * * * ~/put-sflow.sh `date --date '1 days ago' "+\%Y\%m\%d"`
```


