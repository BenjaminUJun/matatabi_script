#!/bin/bash

# Description: put bind9 querylog into hdfs
# ARGS
# $1: sv
# $2: dt

SV=$1
DT=$2
DATADIR=../data/

hive -S -e "alter table querylog add partition (dt='${DT}', sv='${SV}');"
for dataFile in `ls ${DATADIR}/*`
do
 cat $dataFile | lzop | hadoop fs -put - /user/hive/warehouse/querylog/dt=${DT}/sv=${SV}/`basename $dataFile`.lzo
done

