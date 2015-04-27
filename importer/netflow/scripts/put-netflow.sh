# DESCRIPTION :
# This script convert netflow log to a csv format file.
# USAGE : $sh put-netflow.sh <YYYYMMDD> <NETFLOW TABLE NAME>
#!/bin/sh

# remove temporally file
rm -f ./tmp/$1.csv

for dataFile in `ls NETFLOW_DATA_DIRECTORPY/nfcapd.$1*`
do 
# convert nfcapd file into csv format
NFDUMP_PATH -r $dataFile -o csv |tail -n +4 >> ./tmp/$1.csv
done

# compress csv file 
lzop -f -U ./tmp/$1.csv
# import compressed file on the hive table
hive -S -e "load data local inpath './tmp/$1.csv.lzo' overwrite into table NETFLOW_TABLE_NAME partition(dt='$1');"
rm -f ./tmp/$1.csv

# convert text data on the hive table into rcfile format
hive -S \
 -hiveconf hive.exec.compress.intermediate=true \
 -hiveconf hive.exec.compress.output=true \
 -hiveconf mapred.output.compression.type=BLOCK \
 -hiveconf mapred.output.compression.codec=org.apache.hadoop.io.compress.LzoCodec \
 -hiveconf hive.exec.dynamic.partition=true \
 -hiveconf hive.exec.dynamic.partition.mode=nonstrict \
 -e "insert overwrite table $2_rcfile partition(dt) select * from $2 where dt='$1' DISTRIBUTE by dt;"
