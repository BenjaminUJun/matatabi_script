ADD JAR /home/hadoop/downloads/json-hive-serde-1.0.jar;
DROP TABLE IF EXISTS MALC0DE_TABLE_NAME;
CREATE EXTERNAL TABLE MALC0DE_TABLE_NAME (
domain string,
url string,
path string,
cc string,
ip string,
asname string,
asn string,
md5 string
)
partitioned by (dt string)
ROW FORMAT SERDE 'com.proofpoint.hive.serde.JsonSerde'
location 'hdfs:///HIVE_TABLE_PATH';
