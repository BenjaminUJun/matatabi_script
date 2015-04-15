#!/bin/bash

hdfs_save_dir_base="HIVE_TABLE_PATH"
backup_dir="DATA_BACKUP_DIR"

cd `dirname $0`
source $HOME/.bashrc
#source ./VIRTUALENV_NAME/bin/activate

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


mkdir -p log
tmp_file=log/"$nowTime".json
python ./malc0de.py > $tmp_file
if test -s $tmp_file; then
	gzip -9 $tmp_file
	gzip_file=$tmp_file".gz"
	hdfs_save_dir="$hdfs_save_dir_base/dt=$today"
	new_file_name="$nowTime.json.gz"
	./gzJSON2LineJSON.py log/*.gz | ./LineJSON2DateLineJson.py > put.sh
	source put.sh > log/"$nowTime"_put.log 2>&1
	mv log/* $backup_dir/
	rm $gzip_file
else
	rm $tmp_file
fi

