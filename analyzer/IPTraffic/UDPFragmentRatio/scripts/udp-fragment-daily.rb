#!/usr/bin/ruby
prestoExecutionCommand = "/usr/local/presto-0.54-SNAPSHOT/bin/presto-cli-0.54-SNAPSHOT-executable.jar --server localhost:8080 --catalog hive --schema default --execute"

sflowTable = ARGV[0]
date = ARGV[1]

# get the number of flow in the given date and sflow source
row1 =  `#{prestoExecutionCommand} "select count(*) from #{sflowTable} where #{sflowTable}.dt='#{date}';"`
total_flow = row1.split(/\"/)[1].to_i

# get the number of UDP flow in the given date and sflow source
row2 =  `#{prestoExecutionCommand} "select count(*) from #{sflowTable} where #{sflowTable}.dt='#{date}' and #{sflowTable}.ipprotocol=17;"`
number_of_udp_flow = row2.split(/\"/)[1].to_i

# get the number of fragmented UDP flow in the given date and sflow source
row3 =  `#{prestoExecutionCommand} "select count(*) from #{sflowTable} where #{sflowTable}.dt='#{date}' and #{sflowTable}.ipprotocol=17 and ipfragmentoffset is NOT NULL;"`
number_of_fragmented_udp_flow = row3.split(/\"/)[1].to_i

# calculate fragment ratio 
flagmentRatio = (number_of_fragmented_udp_flow.to_f/number_of_udp_flow.to_f)*100

puts "<date>,<total flow>,<udp flow>,<fragmented udp flow>,<fragment ratio (fragmented udp flow/udp flow * 100 [%])>"
puts "#{date},#{total_flow.to_i},#{number_of_udp_flow},#{number_of_fragmented_udp_flow},#{flagmentRatio.round(3)}"
