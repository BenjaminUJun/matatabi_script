#!/bin/sh

DIST_DIR=`dirname $0`/../

SERVER_NAME=mail.example.com
MY_TABLE_NAME=spam
SPAM_DATA_DIRECTORPY=/data/spam/
SPAM_DATA_ANALYSIS_DIRECTORY=/tmp/spam_analysis

cd $DIST_DIR

# modify settings
sed -i -r -e "s@SPAM_TABLE_NAME@$MY_TABLE_NAME@" schema/*.sql
sed -i -r -e "s@SPAM_TABLE_NAME@$MY_TABLE_NAME@" scripts/put-spam-hdfs.sh
sed -i -r -e "s@SPAM_DATA_DIRECTORY@$SPAM_DATA_DIRECTORY@" scripts/put-spam-hdfs.sh
sed -i -r -e "s@SERVER_NAME@$SERVER_NAME@" scripts/put-spam-hdfs.sh

# create hive schema
hive -f schema/HiveTable.sql
