#!/bin/sh

MY_ENV_NAME=virtualenv
BASE_DIR=`dirname $0`/../
cd $BASE_DIR
MY_BACKUP_DIRECTORY=$BASE_DIR/backup
mkdir -p $BASE_DIR/backup
MY_HIVE_TABLE_PATH=/twitter/search
MY_TABLE_NAME=twitter_search
MY_SEARCH_TARGETS="#security #incident #ddos #vulnerability"

# install required modules
apt-get install python-virtualenv
apt-get install jq

(cd scripts; virtualenv $MY_ENV_NAME)
source scripts/$MY_ENV_NAME/bin/activate
sed -i -r -e "s/VIRTUALENV_NAME/$MY_ENV_NAME/" scripts/[a-z]*.sh

# Modify backup directory settings  
sed -i -r -e "s|DATA_BACKUP_DIR|$MY_BACKUP_DIRECTORY|" scripts/[a-z]*.sh

# install python librarys
python scripts/setup.py install
# why this need? (setup.py install failed requests)
pip install requests

# Create import directory on hdfs
hdfs dfs -mkdir -p $MY_HIVE_TABLE_PATH

# Modify hive shcema table name  
sed -i -r -e "s/TWITTER_SEARCH_TABLE_NAME/$MY_TABLE_NAME/" schema/*.sql
sed -i -r -e "s/TWITTER_SEARCH_TABLE_NAME/$MY_TABLE_NAME/" scripts/*.py
sed -i -r -e "s/TWITTER_SEARCH_TABLE_NAME/$MY_TABLE_NAME/" scripts/[a-z]*.sh

# Add Hive table
#  Modify Hive table location  
sed -i -r -e "s|HIVE_TABLE_PATH|$MY_HIVE_TABLE_PATH|" schema/HiveTable.sql
# Create Hive table  
hive -f schema/HiveTable.sql

# Modify hdfs import directory settings  
sed -i -r -e "s|HIVE_TABLE_PATH|$MY_HIVE_TABLE_PATH|" scripts/[a-z]*.sh

# Modify Twitter search setting  
sed -i -r -e "s/#security #incident #ddos #vulnerability/$MY_SEARCH_TARGETS/" scripts/[a-z]*.sh

# create NECOMAtter account

MATATABI_SCRIPTS_DIR=$BASE_DIR/../
NECOMATTER_DIR=$MATATABI_SCRIPTS_DIR/NECOMAtter
NECOMATTER_TOOLS_DIR=$NECOMATTER_DIR/tools

NECOMATTER_USER_NAME="twitterSearchBOT"
$NECOMATTER_TOOLS_DIR/user_add.py $NECOMATTER_USER_NAME 'abcde'
NECOMATTER_API_KEY=`$NECOMATTER_TOOLS_DIR/create_or_get_api_key.py $NECOMATTER_USER_NAME`
NECOMATTER_HOST=localhost:8000

# apply NECOMAtter account settings
sed -i -r -e "s|NECOMATTER_HOST|$NECOMATTER_HOST|" scripts/cron-daily.sh
sed -i -r -e "s|NECOMATTER_USER_NAME|$NECOMATTER_USER_NAME|" scripts/cron-daily.sh
sed -i -r -e "s|NECOMATTER_API_KEY|$NECOMATTER_API_KEY|" scripts/cron-daily.sh
sed -i -r -e "s|^#MEW ||" scripts/cron-daily.sh


echo Hive table created. Unfortunetry, You have more job.
echo You need create twitter BOT account and get consumer key, consumer secret, access key, access secret. and modify your scripts

#sed -i -r -e 's/TWITTER_CONSUMER_KEY/YOUR_CONSUMER_KEY/' scripts/*.py
#sed -i -r -e 's/TWITTER_CONSUMER_SECRET/YOUR_CONSUMER_SECRET/' scripts/*.py
#sed -i -r -e 's/TWITTER_ACCESS_KEY/YOUR_ACCESS_KEY/' scripts/*.py
#sed -i -r -e 's/TWITTER_ACCESS_SECRET/YOUR_ACCESS_SECRET/' scripts/*.py
