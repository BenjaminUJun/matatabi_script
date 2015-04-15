#!/bin/bash

source /home/hadoop/.profile

/usr/bin/ruby1.9.1 udp-fragment-daily.rb <SFLOW TABLE NAME> `date --date '1 days ago' "+\%Y\%m\%d"` 
