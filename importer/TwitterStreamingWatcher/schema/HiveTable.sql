DROP TABLE IF EXISTS TWITTER_STREAMING_TABLE_NAME;
CREATE EXTERNAL TABLE TWITTER_STREAMING_TABLE_NAME
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
partitioned by (dt string)
ROW FORMAT SERDE 'com.proofpoint.hive.serde.JsonSerde'
location 'hdfs:///HIVE_TABLE_PATH';
