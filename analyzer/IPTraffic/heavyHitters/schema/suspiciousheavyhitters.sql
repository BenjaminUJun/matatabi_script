create table if not exists suspiciousheavyhitters 
(
    srcip string,
    dstip string,
    pkt bigint,
    byte bigint,
    confidence string
)
partitioned by(dt string, dataSrc string) 
row format delimited fields terminated by '\t';
