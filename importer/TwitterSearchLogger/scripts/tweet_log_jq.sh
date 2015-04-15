#!/bin/bash

for file in logs/*.json.gz
do
	echo "$file "
	gzip -dc $file | /usr/local/bin/jq $*
done
