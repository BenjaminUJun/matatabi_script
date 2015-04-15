#!/bin/bash

cd `dirname $0`
source $HOME/.bashrc
source ./VIRTUALENV_NAME/bin/activate

./tweet_log_jq.sh .[].user.screen_name | grep -v ^logs/ > screen_name_list.txt
python AddFollower.py screen_name_list.txt
