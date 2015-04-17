#!/bin/sh

MY_ENV_NAME=virtualenv
BASE_DIR=`dirname $0`/../
cd $BASE_DIR
MY_BACKUP_DIRECTORY=$BASEDIR/backup
mkdir $MY_BACKUP_DIRECTORY
MY_HIVE_TABLE_PATH=/twitter/streaming
MY_TABLE_NAME=twitter_streaming

# install required packages
apt-get install python-virtualenv

# initialize virtualenv
vertualenv $YOUR_ENV_NAME

sed -i -r -e "s/VIRTUALENV_NAME/$MY_ENV_NAME/" *.sh

# Modify backup directory settings  
sed -i -r -e "s|DATA_BACKUP_DIR|$MY_BACKUP_DIRECTORY|" *.sh

# install python librarys
python scripts/setup.py install

# Create import directory on hdfs
hdfs dfs -mkdir -p $MY_HIVE_TABLE_PATH

# Modify hive shcema table name  

sed -i -r -e "s/TWITTER_STREAMING_TABLE_NAME/$MY_TABLE_NAME/" schema/*.sql
sed -i -r -e "s/TWITTER_STREAMING_TABLE_NAME/$MY_TABLE_NAME/" scripts/*.py
sed -i -r -e "s/TWITTER_STREAMING_TABLE_NAME/$MY_TABLE_NAME/" scripts/*.sh

# Add Hive table
#  Modify Hive table location  
sed -i -r -e "s|HIVE_TABLE_PATH|$MY_HIVE_TABLE_PATH|" schema/HiveTable.sql
# Create Hive table  
hive -f schema/HiveTable.sql

# Modify hdfs import directory settings  
sed -i -r -e "s|HIVE_TABLE_PATH|$MY_HIVE_TABLE_PATH|" scripts/cron.sh

echo Hive table created. Unfortunetry, You have more job.
echo You need create twitter BOT account and get consumer key, consumer secret, access key, access secret. and modify your scripts

#sed -i -r -e 's/TWITTER_CONSUMER_KEY/YOUR_CONSUMER_KEY/' *.py
#sed -i -r -e 's/TWITTER_CONSUMER_SECRET/YOUR_CONSUMER_SECRET/' *.py
#sed -i -r -e 's/TWITTER_ACCESS_KEY/YOUR_ACCESS_KEY/' *.py
#sed -i -r -e 's/TWITTER_ACCESS_SECRET/YOUR_ACCESS_SECRET/' *.py

