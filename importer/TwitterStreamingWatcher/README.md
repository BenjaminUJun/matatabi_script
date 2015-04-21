# Module Name
Twitter Streaming Watcher

# Input Dataset

twitter stream result (JSON format)

# Output Data

one line JSON list.

# Description of the module

TwitterSearchLogger が daily で follow しているタイムラインを、そのまま読み取って hive に入れます。
cron(8) 等で定期的にlogを更新して hive に書き込むためのscript (cron.sh) が書かれています。
cron.sh では

 - daemon が動いていなければ起動
 - log ファイルをローテートさせて、古いlogファイルの中身を hive に書き込む

ということをします。

# usage 
## first set up

1. You must setup TwitterSearchLogger module before TwitterStreamingWatcher

1. use virtualenv.  
`% virtualenv YOUR_ENV_NAME`
  - Modify virtualenv settings for shell scripts  
  `% sed -i -r -e 's/VIRTUALENV_NAME/YOUR_ENV_NAME/' *.sh`

1. Modify backup directory settings  
`% sed -i -r -e 's|DATA_BACKUP_DIR|YOUR_BACKUP_DIRECTORY|' *.sh`

1. install python librarys
`% python setup.py`

1. Create import directory on hdfs

1. Modify hive shcema table name  

```sh
% sed -i -r -e 's/TWITTER_STREAMING_TABLE_NAME/YOUR_TABLE_NAME/' schema/*.sql
% sed -i -r -e 's/TWITTER_STREAMING_TABLE_NAME/YOUR_TABLE_NAME/' scripts/*.py
% sed -i -r -e 's/TWITTER_STREAMING_TABLE_NAME/YOUR_TABLE_NAME/' scripts/*.sh
```

1. Add Hive table
  - Modify Hive table location  
  `% sed -i -r -e 's|HIVE_TABLE_PATH|YOUR_HIVE_TABLE_PATH|' HiveTable.sql`
  - Create Hive table  
  `% hive -f HiveTable.sql`

1. Modify hdfs import directory settings  
`% sed -i -r -e 's|HIVE_TABLE_PATH|YOUR_HIVE_TABLE_PATH|' cron.sh

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
55 23 * * * some_directory.../TwitterStreamingWatcher/scripts/cron.sh
```


