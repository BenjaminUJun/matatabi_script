# Module Name

mulc0de

# Input Dataset

(mulc0de)[http://malc0de.com/database/] table data.

# Output Data

one line JSON list.

# Description of the module

(mulc0de database)[http://malc0de.com/database/]から取得したデータを一行毎のJSON形式で hdfs に入れます。

# usage 
## first set up

1. install python modules

```sh
pip install requests
```

1. Modify hive shcema table name  

```sh
% sed -i -r -e 's/MALC0DE_TABLE_NAME/YOUR_TABLE_NAME/' schema/*.sql
% sed -i -r -e 's/MALC0DE_TABLE_NAME/YOUR_TABLE_NAME/' scripts/*.py
% sed -i -r -e 's/MALC0DE_TABLE_NAME/YOUR_TABLE_NAME/' scripts/*.sh
```

1. Modify backup directory settings  
`% sed -i -r -e `s/DATA_BACKUP_DIR/YOUR_BACKUP_DIRECTORY/' scripts/*.sh`

1. Create import directory on hdfs at YOUR_HIVE_TABLE_PATH

1. Add Hive table
  - Modify Hive table location  
  `% sed -i -r -e 's/HIVE_TABLE_PATH/YOUR_HIVE_TABLE_PATH/' schema/*.sql`
  - Create Hive table  
  `% hive -f HiveTable.sql`

1. Modify hdfs import directory settings  

```sh
% sed -i -r -e 's/HIVE_TABLE_PATH/YOUR_HIVE_TABLE_PATH/' scripts/*.sh
% sed -i -r -e 's/HIVE_TABLE_PATH/YOUR_HIVE_TABLE_PATH/' scripts/*.py
```
## assign cron(8)

use cron(8) like this:

```
0 * * * * some_directory.../malc0de/scripts/cron.sh
```


