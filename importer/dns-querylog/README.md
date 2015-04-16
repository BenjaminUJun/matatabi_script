# Module Name
- bind9 querylog importer

# Input Dataset
- plain text data file colleceted by bind9

# Description 
- The script imports querylog data collected by bind9 and store on a HDFS, refered by Hive table. The table definition is available on "schema" directory.

# Usage
- one shot

```shell:
# ./scripts/put-querylog-hdfs.sh <PARTITION NAME> <YYYYMMDD>
```

- cron

```
* 11 * * * scripts/cron.sh
```


