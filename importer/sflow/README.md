# Module Name
- sflow importer

# Input Dataset
- compressed (.tar.gz) sflow data file colleceted by sflowtools

# Description 
- The script imports daily sflow data which collected by sflowtools on a MATATABI table. The table definition is available on "schema" directory.


# Usage
- one shot

```shell:
# ruby put-sflows sflow_data_20150101.txt.gz 20150101 <SFLOW TABLE NAME>
```

- cron

```
* 11 * * * ~/put-sflow.sh
```


