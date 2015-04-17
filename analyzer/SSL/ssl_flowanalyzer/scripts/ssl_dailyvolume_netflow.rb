#!/usr/bin/ruby

prestoExecutionCommand = "/usr/local/presto-0.54-SNAPSHOT/bin/presto-cli-0.54-SNAPSHOT-executable.jar --server localhost:8080 --catalog hive --schema default --execute"

netflowTable = ARGV[0]
date_offset = ARGV[1].to_i

puts "====#{netflowTable}===="
while date_offset > 1 do 
	date =  `date -d "#{date_offset} days ago" '+%Y%m%d'`.to_s.chop

    tmp1 =  `#{prestoExecutionCommand} "select count(*) from netflow_wide where dt='#{date}' and flg='....S.' and pr='TCP' and dp=443;"`
    number_of_tcp_443_syn = tmp1.split(/\"/)[1].to_i

    puts "#{date} #{number_of_tcp_443_syn}"

	date_offset -= 1
end
puts "====================="
