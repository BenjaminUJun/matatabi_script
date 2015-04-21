# Module Name
Twitter Search Logger

# Input Dataset

twitter search result (JSON format)

# Output Data

one line JSON list.

# Description of the module

Twitter で任意の文字列を検索をした結果を一行毎のJSON形式で hdfs に入れます。
cron(8) 等で定期的に実行される事を期待しています。
cron では、15分程度おきに実行される cron.sh と、一日に一回実行される cron-daily.sh が用意されています。
cron.sh では指定された文字列(ハッシュタグ等)で検索を行い、その結果を log に取りつつ hive に入れます。
cron-daily.sh ではそれらのlogを使って新しいユーザをフォローしたり、
その日に見かけた一番多いURLのTOP10やTOP3をtwitter等に書き込みます。
また、その日の分の log はバックアップ用のディレクトリへ移動します。

# usage 
## first set up

1. use virtualenv.  
`% virtualenv YOUR_ENV_NAME`
  - Modify virtualenv settings for shell scripts  
  `% sed -i -r -e 's/VIRTUALENV_NAME/YOUR_ENV_NAME/' *.sh`

1. Modify backup directory settings  
`% sed -i -r -e 's|DATA_BACKUP_DIR|YOUR_BACKUP_DIRECTORY|' *.sh`

1. install python librarys
`% python setup.py`

1. Install [jq](http://stedolan.github.io/jq/)

1. Create import directory on hdfs

1. Modify hive shcema table name  

```sh
% sed -i -r -e 's/TWITTER_SEARCH_TABLE_NAME/YOUR_TABLE_NAME/' schema/*.sql
% sed -i -r -e 's/TWITTER_SEARCH_TABLE_NAME/YOUR_TABLE_NAME/' scripts/*.py
% sed -i -r -e 's/TWITTER_SEARCH_TABLE_NAME/YOUR_TABLE_NAME/' scripts/*.sh
```

1. Add Hive table
  - Modify Hive table location  
  `% sed -i -r -e 's|HIVE_TABLE_PATH|YOUR_HIVE_TABLE_PATH|' HiveTable.sql`
  - Create Hive table  
  `% hive -f HiveTable.sql`

1. Modify hdfs import directory settings  
`% sed -i -r -e 's|HIVE_TABLE_PATH|YOUR_HIVE_TABLE_PATH|' cron.sh

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

1. If you need mew to (NECOMATter)[]
  - Create NECOMATter account for TwitterSearch bot.
  - Create NECOMATter API key.
  - modify mew settings.
```sh
sed -i -r -e 's/NECOMATTER_URI/NECOMATTER_URI/' cron-daily.sh
sed -i -r -e 's/NECOMATTER_USER_NAME/NECOMATTER_USER_NAME/' cron-daily.sh
sed -i -r -e 's/NECOMATTER_API_KEY/NECOMATTER_API_KEY/' cron-daily.sh
sed -i -r -e 's/^#MEW //' cron-daily.sh
```


## assign cron(8)

use cron(8) like this:

```
*/15 * * * * some_directory.../TwitterSearchLogger/scripts/cron.sh
50 23 * * * some_directory.../TwitterSearchLogger/scripts/cron-daily.sh
```


