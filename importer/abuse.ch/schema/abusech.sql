create table if not exists abusech_palevo_tracker
(
  cc_ip string,
  hostname string
)
partitioned by(dt string)
row format delimited fields terminated by '\t';

create table if not exists abusech_zeus_tracker
(
  cc_ip string,
  hostname string
)
partitioned by(dt string)
row format delimited fields terminated by '\t';

create table if not exists abusech_spyeye_tracker
(
  cc_ip string,
  hostname string
)
partitioned by(dt string)
row format delimited fields terminated by '\t';

create table if not exists abusech_feodo_tracker
(
  cc_ip string,
  hostname string
)
partitioned by(dt string)
row format delimited fields terminated by '\t'; 
