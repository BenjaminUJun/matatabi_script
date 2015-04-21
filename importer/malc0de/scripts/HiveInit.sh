#!/bin/sh

DIST_DIR=`dirname $0`/../

MY_TABLE_NAME=malc0de
MY_BACKUP_DIRECTORY=$DIST_DIR/backup
mkdir -p $MY_BACKUP_DIRECTORY
MY_HIVE_TABLE_PATH=/malc0de

cd $DIST_DIR

apt-get install python-pip
pip install requests

# modify settings
sed -i -r -e "s/MALC0DE_TABLE_NAME/$MY_TABLE_NAME/" schema/*.sql
sed -i -r -e "s/MALC0DE_TABLE_NAME/$MY_TABLE_NAME/" scripts/*.py
sed -i -r -e "s/MALC0DE_TABLE_NAME/$MY_TABLE_NAME/" scripts/cron.sh

sed -i -r -e "s|DATA_BACKUP_DIR|$MY_BACKUP_DIRECTORY|" scripts/cron.sh

# make hdfs directory
hdfs dfs -mkdir -p $MY_HIVE_TABLE_PATH

# create hive schema
sed -i -r -e "s|HIVE_TABLE_PATH|$MY_HIVE_TABLE_PATH|" schema/*.sql
hive -f schema/HiveTable.sql

# apply hive table path to scripts
sed -i -r -e "s|HIVE_TABLE_PATH|$MY_HIVE_TABLE_PATH|" scripts/cron.sh
sed -i -r -e "s|HIVE_TABLE_PATH|$MY_HIVE_TABLE_PATH|" scripts/*.py
