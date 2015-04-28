#!/bin/bash

# Description: put spam into hdfs

date=$1

/usr/bin/python spam-parse.py SPAM_DATA_DIRECTORY $date
/usr/local/hive-0.11.0/bin/hive -S -e "LOAD DATA LOCAL INPATH 'SPAM_DATA_ANALYSIS_DIRECTORY/${date}.output' OVERWRITE INTO TABLE SPAM_TABLE_NAME partition (dt='${date}', sv='SERVER_NAME');" > /dev/null

