#!/usr/bin/ruby
#
prestoExecutionCommand = "/usr/local/presto-0.54-SNAPSHOT/bin/presto-cli-0.54-SNAPSHOT-executable.jar --server localhost:8080 --catalog hive --schema default --execute"

sflowTable = ARGV[0]
date = ARGV[1]

outputData = `#{prestoExecutionCommand} "select srcip,count(*) as \\"number\\" from #{sflowTable} where dt='#{date}' and udpdstport=123 group by srcip order by \\"number\\" desc limit 10;"`

puts "====#{sflowTable}===="
puts "#{outputData}"
puts "====================="

