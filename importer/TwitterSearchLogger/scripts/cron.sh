#!/bin/bash

search_targets="#security #incident #ddos #vulnerability"
log_dir="logs"; mkdir -p $log_dir
hdfs_save_dir_base="HIVE_TABLE_PATH"

cd `dirname $0`
source $HOME/.bashrc # for hadoop settings
source ./VIRTUALENV_NAME/bin/activate

today=`date +%Y%m%d`
nowTime=`date +%Y%m%d%H%M%S`

function copy_to_hdfs() {
	source_file="$1"
	destination_directory="$2"
	new_file_name="$3"
	hdfs dfs -mkdir -p $destination_directory
	#echo hdfs dfs -put $source_file "$destination_directory/$new_file_name"
	hdfs dfs -put $source_file "$destination_directory/$new_file_name"
}

for search_string in $search_targets
do
	escaped_search_string=`echo $search_string | sed -e 's/#//g'`
	log_file="$log_dir/search_result_linejson-$escaped_search_string-$nowTime.json"
	error_log_file="$log_dir/search_result_linejson-$escaped_search_string-$nowTime.error"
	hdfs_save_dir="$hdfs_save_dir_base/dt=$today/search=$escaped_search_string"
	new_file_name="$nowTime.json"
	if python ./TwitterSearchLogger.py $search_string > $log_file 2> $error_log_file; then
		gzip -9 $log_file
		copy_to_hdfs $log_file".gz" $hdfs_save_dir $new_file_name".gz"
		hive -e "ALTER TABLE twitter_search_log ADD IF NOT EXISTS PARTITION(dt='${today}', search='${escaped_search_string}')" > /dev/null
	else
		echo script error on twitter search "'"$sarch_string"'". details are:
		cat $error_log_file
	fi
	#rm -f $log_file $error_log_file
done
