#!/bin/bash

hdfs_save_dir_base="HIVE_TABLE_PATH"
log_file="stream_log.json"
pid_file="stream_bot.pid"
old_log_dir="logs"
backup_dir="DATA_BACKUP_DIR"

cd `dirname $0`
source $HOME/.bashrc
source VIRTUALENV_NAME/bin/activate

thismonth=`date +%Y%m`
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

function reload_log() {
	new_log_file="$1"
	mv $log_file $new_log_file
	kill -HUP `cat $pid_file`
}

function check_and_restart_stream_daemon() {
	if test ! -d /proc/`cat $pid_file`; then
		echo twitter stream read daemon dead. restart.
		source ./virtualenv/bin/activate
		python ./TwitterStreamingWatcher.py $log_file
		sleep 1
		if test ! -d /proc/`cat $pid_file`; then
			echo twitter stream read daemon restart failed.
			exit 1
		fi
	fi
}

check_and_restart_stream_daemon

new_log_file="$old_log_dir/$nowTime-$log_file"
reload_log $new_log_file

gzip -9 $new_log_file

hdfs_save_dir="$hdfs_save_dir_base/dt=$today"
hdfs_file_name="$nowTime.oneline.json"
copy_to_hdfs $new_log_file".gz" $hdfs_save_dir $hdfs_file_name".gz"
hive -e "ALTER TABLE TWITTER_STREAMING_TABLE_NAME ADD IF NOT EXISTS PARTITION(dt='${today}')" > /dev/null

backup_dir_month="$backup_dir$thismonth"
mkdir -p $backup_dir_month
mv $new_log_file".gz" $backup_dir_month
