create table if not exists suspiciousdnsfailures 
(
    fqdn string, 
    srcip string, 
    clusterid int, 
    clustersize bigint, 
    degree double, 
    confidence string, 
    table string
) 
partitioned by(dt string) 
row format delimited fields terminated by '\t';
