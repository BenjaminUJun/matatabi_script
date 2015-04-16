#!/bin/bash

## querylog to HDFS
date=`date --date '0 days ago' "+%Y%m%d"`
array=("test")

for server in "${array[@]}"
do
   ./put-querylog-hdfs.sh $server $date |& grep -v "INFO Configuration " | grep -v "SLF4J"  > /dev/null
done
