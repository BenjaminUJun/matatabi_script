#!/usr/bin/ruby

prestoExecutionCommand = "/usr/local/presto-0.54-SNAPSHOT/bin/presto-cli-0.54-SNAPSHOT-executable.jar --server localhost:8080 --catalog hive --schema default --execute"

netflowTable = ARGV[0]
date = ARGV[1]

tmp1 =  `#{prestoExecutionCommand} "select sa,count(distinct da) as num from #{netflowTable} where dt='#{date}' and flg='....S.' and pr='TCP' and dp=443 group by sa order by num,sa desc;"`

tmp1.delete("\"").split(/\n/).each{|line|
	tmp2 = line.split(/\,/)
	puts "#{tmp2[0]} #{tmp2[1]}"
}

