#!/bin/bash

NECOMAtter_tweet="../../NECOMATter/tools/tweet_with_api_key.py"
backup_dir="DATA_BACKUP_DIR"

cd `dirname $0`
source $HOME/.bashrc
source ./VIRTUALENV_NAME/bin/activate

thismonth=`date +%Y%m`
today=`date +%Y%m%d`
nowTime=`date +%Y%m%d%H%M%S`

function dump_tweet_day() {
	today="$1"
	for file in logs/*$today*.json.gz
	do
		gzip -dc $file | jq .text | sed -e 's/^"//' -e 's/"$//'
	done
}

# get best 10 URL
best_10=`dump_tweet_day | ./UriCount.py | head -10`

# mew to NECOMAtter
#MEW (echo "top 10 URL in twitter search result:  "; echo '  '; echo "$best_10") | $NECOMAtter_tweet NECOMATTER_URI 'NECOMATTER_USER_NAME' NECOMATTER_API_KEY > /dev/null

# tweet to Twitter
(echo "top 3 URL today:"; echo ''; echo "$best_10" | head -3 | sed -e 's/ *$//') | ./Tweet.py

# add twitter follow
./tweet_log_jq.sh .user.screen_name | grep -v ^logs/ > screen_name_list.txt
python AddFollower.py > /dev/null

backup_dir_month="$backup_dir$thismonth"
mkdir -p $backup_dir_month
mv logs/*$today* $backup_dir_month
