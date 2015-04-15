# Module Name
Twitter Search Logger

# Input Dataset

twitter search result (JSON format)

# Output Data

one line JSON list.

# Description of the module

Twitter で任意の文字列を検索をした結果を一行毎のJSON形式で hdfs に入れます。
cron(8) 等で定期的に実行される事を期待しています。

# usage 
## first set up

1. use virtualenv.  
`% vertualenv YOUR_ENV_NAME`
  - Modify virtualenv settings for shell scripts  
  `% sed -i -r -e 's/VIRTUALENV_NAME/YOUR_ENV_NAME/' *.sh`

1. Modify backup directory settings  
`% sed -i -r -e `s/DATA_BACKUP_DIR/YOUR_BACKUP_DIRECTORY/' *.sh`

1. install python librarys
`% python setup.py`

1. Install [jq](http://stedolan.github.io/jq/)

1. Create import directory on hdfs

1. Add Hive table
  - Modify Hive table location  
  `% sed -i -r -e 's/HIVE_TABLE_PATH/YOUR_HIVE_TABLE_PATH/' HiveTable.sql`
  - Create Hive table  
  `% hive -f HiveTable.sql`

1. Modify hdfs import directory settings  
`% sed -i -r -e 's/HDFS_IMPORT_DIR/YOUR_HDFS_IMPORT_DIR/' cron.sh

1. Modify Twitter search setting  
`% sed -i -r -e 's/#security #incident #ddos #vulnerability/YOUR SEARCH TARGETS/' cron.sh`

1. Create Twitter account for search.
  - Add your application and create consumer key and secret key on Twitter.
  - modify key settings.

```sh
sed -i -r -e 's/TWITTER_CONSUMER_KEY/YOUR_CONSUMER_KEY/' *.py
sed -i -r -e 's/TWITTER_CONSUMER_SECRET/YOUR_CONSUMER_SECRET/' *.py
sed -i -r -e 's/TWITTER_ACCESS_KEY/YOUR_ACCESS_KEY/' *.py
sed -i -r -e 's/TWITTER_ACCESS_SECRET/YOUR_ACCESS_SECRET/' *.py
```

## assign cron(8)

use cron(8) like this:

```
*/15 * * * * some_directory.../TwitterSearchLogger/cron.sh
50 23 * * * some_directory.../TwitterSearchLogger/cron-daily.sh
```


