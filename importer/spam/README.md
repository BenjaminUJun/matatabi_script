# Module Name
- spam importer

# Input Dataset
- raw email data 

# Description 
- The script imports daily spam mail data on a MATATABI table. The table definition is available on "schema" directory.

# Usage
- one shot

```shell:
# python spam-parse.py <MAIL DATA DIRECTORY> <YYYYMMDD> 
```

- cron

```
* 11 * * * ~/put-spam-hdfs.sh
```


