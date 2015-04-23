#!/bin/bash

# Description: put spam into hdfs

spam_directroy=$1
date=$2

/usr/bin/python <PATH>/spam-parse.py $spam_directory $date
/usr/local/hive-0.11.0/bin/hive -S -e "LOAD DATA LOCAL INPATH '<PATH>/spam-analyze/${spam_directory}/${date}.output' OVERWRITE INTO TABLE <SPAM TABLE NAME> partition (dt='${date}', sv='${spam_directory}');" > /dev/null

