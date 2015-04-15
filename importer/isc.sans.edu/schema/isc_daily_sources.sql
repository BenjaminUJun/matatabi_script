create table if not exists isc_daily_sources 
(
    source_ip string, target_port int,
    protocol int,
    reports bigint,
    targets bigint,
    first_seen string,
    last_seen string,
    hostname string
) 
partitioned by(dt string)
row format delimited fields terminated by '\t';
