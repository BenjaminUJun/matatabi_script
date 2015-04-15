#!/bin/sh

ruby put-sflow.rb <SFLOW FILE NAME(.tar.gz)> `date --date '1 days ago' "+%Y%m%d"` <SFLOW TABLE NAME> $*
