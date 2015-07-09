#!/bin/sh

DIST_DIR=`dirname $0`/../

NFDUMP_PATH=/usr/sbin/nfdump
MY_TABLE_NAME=netflow
NETFLOW_DATA_DIRECTORPY=/tmp/data/netflow/

cd $DIST_DIR

# modify settings
sed -i -r -e "s@NETFLOW_TABLE_NAME@$MY_TABLE_NAME@" schema/*.sql
sed -i -r -e "s@NETFLOW_TABLE_NAME@$MY_TABLE_NAME@" scripts/put-netflow.sh
sed -i -r -e "s@NETFLOW_DATA_DIRECTORY@$NFDUMP_PATH@" scripts/put-netflow.sh
sed -i -r -e "s@NFDUMP_PATH@$NFDUMP_PATH@" scripts/put-netflow.sh

# create hive schema
hive -f schema/HiveTable.sql
