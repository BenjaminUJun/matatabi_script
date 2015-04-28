#!/bin/sh

DIST_DIR=`dirname $0`/../

MY_TABLE_NAME=sflow

cd $DIST_DIR

# modify settings
sed -i -r -e "s@SFLOW_TABLE_NAME@$MY_TABLE_NAME@" schema/*.sql
sed -i -r -e "s@SFLOW_TABLE_NAME@$MY_TABLE_NAME@" scripts/put-sflow.sh

# create hive schema
hive -f schema/HiveTable.sql
