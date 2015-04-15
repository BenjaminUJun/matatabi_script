#!/usr/bin/ruby
# example :
# >ruby put sflow.rb <SFLOW FILE NAME (.tar.gz)> <YYYYMMDD> <SFLOW TAABLE NAME>
require 'zlib'

# clear data hash 
def cleardata(data,dataType)
    dataType.each{|line|
        data[line] = nil
    }
end

def loadSflow(flowFileName, data, dataType, output)
    # header information
    datagramSourceIP = ""
    datagramSize = 0
    unixSecondsUTC = 0
    datagramVersion = 0
    agentSubId = 0
    agent = ""
    packetSequenceNo = 0
    sysUpTime = 0
    samplesInPacket = 0

    Zlib::GzipReader.open(flowFileName){|flowdata|
        cleardata(data,dataType)

        # purse each line and pick up values listed in the field list
        flowdata.each_line{|line|
            unless line =~ /startDatagram/ || line =~ /startSample/ 
                if line =~ /endSample/
                    data["datagramSourceIP"] = datagramSourceIP
                    data["datagramSize"] = datagramSize
                    data["unixSecondsUTC"] = unixSecondsUTC
                    data["datagramVersion"] = datagramVersion
                    data["agentSubId"] = agentSubId
                    data["agent"] = agent
                    data["packetSequenceNo"] = packetSequenceNo
                    data["sysUpTime"] = sysUpTime
                    data["samplesInPacket"] = samplesInPacket


                    dataType.each{|type|
                        output.print "#{data[type]},"
                    }
                    output.print "\n"

                    cleardata(data,dataType)
                end

                if line =~ /endDatagram/
                    data = Hash.new()
                    dataType.each{|type|
                        data[type] = nil
                    }
                end

                if line =~ /datagramSourceIP/
                    tmp = line.split(/\ /)
                    datagramSourceIP = tmp[1].to_s.chop
                    data["datagramSourceIP"] = datagramSourceIP
                elsif line =~ /datagramSize/
                    tmp = line.split(/\ /)
                    datagramSize = tmp[1].chop.to_i
                    data["datagramSize"] = datagramSize
                elsif line =~ /unixSecondsUTC/
                    tmp = line.split(/\ /)
                    unixSecondsUTC = tmp[1].chop.to_i
                    data["unixSecondsUTC"] = unixSecondsUTC
                elsif line =~ /datagramVersion/
                    tmp = line.split(/\ /)
                    datagramVersion = tmp[1].chop.to_i
                    data["datagramVersion"] = datagramVersion
                elsif line =~ /agentSubId/
                    tmp = line.split(/\ /)
                    agentSubId = tmp[1].chop.to_i
                    data["agentSubId"] = agentSubId
                elsif line =~ /agent/
                    tmp = line.split(/\ /)
                    agent = tmp[1].chop.to_s
                    data["agent"] = agent
                elsif line =~ /packetSequenceNo/
                    tmp = line.split(/\ /)
                    packetSequenceNo = tmp[1].chop.to_i
                    data["packetSequenceNo"] = packetSequenceNo
                elsif line =~ /sysUpTime/
                    tmp = line.split(/\ /)
                    sysUpTime = tmp[1].chop.to_i
                    data["sysUpTime"] = sysUpTime
                elsif line =~ /samplesInPacket/
                    tmp = line.split(/\ /)
                    samplesInPacket = tmp[1].chop.to_i
                    data["samplesInPacket"] = samplesInPacket
                else
                    tmp = line.split(/\ /)
                    if tmp[1].to_s.length != 0 then
                        data[tmp[0]] = tmp[1].to_s.chop
                    else
                        data[tmp[0]] = nil
                    end
                end
            end
        }
    }
end


flowFileName = ARGV[0]
date = ARGV[1]
importTableName = ARGV[2]

data = {}
dataType = []

# list of sflow field
fieldList = "datagramSourceIP,datagramSize,unixSecondsUTC,datagramVersion,agentSubId,agent,packetSequenceNo,sysUpTime,samplesInPacket,ICMPCode,ICMPType,IP6HeaderExtension:,IP6_label,IPFragmentOffset,IPProtocol,IPSize,IPTOS,IPTTL,IPV6_payloadLen,TCPDstPort,TCPFlags,TCPSrcPort,UDPBytes,UDPDstPort,UDPSrcPort,counterBlock_tag,dot3StatsAlignmentErrors,dot3StatsCarrierSenseErrors,dot3StatsDeferredTransmissions,dot3StatsExcessiveCollisions,dot3StatsFCSErrors,dot3StatsFrameTooLongs,dot3StatsInternalMacReceiveErrors,dot3StatsInternalMacTransmitErrors,dot3StatsLateCollisions,dot3StatsMultipleCollisionFrames,dot3StatsSQETestErrors,dot3StatsSingleCollisionFrames,dot3StatsSymbolErrors,dropEvents,dstIP,dstIP6,dstMAC,extendedType,flowBlock_tag,flowSampleType,headerBytes,headerLen,headerProtocol,ifDirection,ifInBroadcastPkts,ifInDiscards,ifInErrors,ifInMulticastPkts,ifInOctets,ifInUcastPkts,ifInUnknownProtos,ifIndex,ifOutBroadcastPkts,ifOutDiscards,ifOutErrors,ifOutMulticastPkts,ifOutOctets,ifOutUcastPkts,ifPromiscuousMode,ifSpeed,ifStatus,in_priority,in_vlan,inputPort,ip.tot_len,meanSkipCount,networkType,out_priority,out_vlan,outputPort,samplePool,sampleSequenceNo,sampleType,sampleType_tag,sampledPacketSize,sourceId,srcIP,srcIP6,srcMAC,strippedBytes"

# initialize data hash
fieldList.split(/\,/).each{|line|
    if data[line] == nil
        data[line] = nil
        dataType.push(line)
    end
}
p dataType

# output directory of a temporally file
tmpDirectory = "./tmp/"
outputFileName = tmpDirectory + flowFileName.split(/\./)[0] + ".csv"
output = open("#{outputFileName}","a")

# load sflow data
begin
    loadSflow(flowFileName, data, dataType, output)
rescue => e
    puts $@
    puts e
end

output.close

# compress csv data by lzo
`lzop -U #{outputFileName}`

# import the lzo file to hive 
`hive -S -e  "load data local inpath '#{outputFileName}.lzo' into table #{importTableName} partition(dt='#{date}');"`

# cleanup file
`/bin/rm -f '#{outputFileName}.lzo'`
`/bin/rm -f '#{outputFileName}'`

