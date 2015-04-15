# Module Name
Twitter Search Logger

# Input Dataset

twitter search result

## Hive table definition

```sql
DROP TABLE IF EXISTS twitter_search_log;
CREATE EXTERNAL TABLE twitter_search_log
(
  text STRING,
  retweeted BOOLEAN,
  id_str STRING,
  retweet_count INT,
  created_at STRING,
  entities struct <
    urls: array <
      struct < url: STRING, expanded_url: STRING >
    >,
    hashtags: array <
      struct < text: STRING >
    >
  >,
  user struct <
    name: STRING,
    screen_name: STRING,
    description: STRING,
    lang: STRING,
    created_at: STRING,
    followers_count: INT,
    friends_count: INT,
    location: STRING,
    profile_image_url: STRING,
    url: STRING
  >
)
partitioned by (dt string, search string)
ROW FORMAT SERDE 'com.proofpoint.hive.serde.JsonSerde'
location 'hdfs:///user/hadoop/iimura/twitter/search';
```
  
# 何をするものか

Twitter で任意の文字列を検索をした結果を一行毎のJSON形式で hdfs に入れます。
cron(8) 等で定期的に実行される事を期待しています。

# set up

1. use virtualenv.
`% vertualenv ENV_NAME`

2. next, run setup.py
`% python setup.py`

3. modify hdfs import directory settings
`% sed -i -r -e 's/HDFS_IMPORT_DIR/YOUR_HDFS_IMPORT_DIR/' cron.sh

4. Create Twitter account for search.
4.1 Add your application and create consumer key and secret key on Twitter.
4.2 modify key settings.

`% sed -i -r -e 's/TWITTER_CONSUMER_KEY/YOUR_CONSUMER_KEY/' *.py`
`% sed -i -r -e 's/TWITTER_CONSUMER_SECRET/YOUR_CONSUMER_SECRET/' *.py`
`% sed -i -r -e 's/TWITTER_ACCESS_KEY/YOUR_ACCESS_KEY/' *.py`
`% sed -i -r -e 's/TWITTER_ACCESS_SECRET/YOUR_ACCESS_SECRET/' *.py`

# usage

use cron(8) like this:
```
*/15 * * * * some_directory.../TwitterSearchLogger/cron.sh
50 23 * * * some_directory.../TwitterSearchLogger/cron-daily.sh
```


