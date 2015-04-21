#!/bin/bash

for file in logs/*.json.gz
do
	echo "$file "
	gzip -dc $file | jq $*
done
