CREATE TABLE querylog (date STRING,
                            time STRING,
                            type STRING,
                            node STRING,
                            ipaddr STRING,
                            qtype STRING,
                            qname STRING,
                            cname STRING,
                            typename STRING,
                            recrflag STRING)
PARTITIONED BY(dt STRING, sv STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ' ' LINES TERMINATED BY '\n';
