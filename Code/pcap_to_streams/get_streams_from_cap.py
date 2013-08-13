'''
Created on Apr 21, 2013

@author: yfried
'''

import sys
import split_to_streams, parse_stream_packets
import os
import shutil
from impacket import ImpactDecoder
from impacket.ImpactPacket import ImpactPacketException
from parse_stream_packets import dPacket


    
class dStream:
    def __init__(self, packets):
        first_pkt = packets[0]
        self.dst_ip = first_pkt.dst_ip
        self.dport = first_pkt.dport
        self.sport = first_pkt.sport
        
        #list containing packet data of the session
        self.packets = packets
        
    def __str__(self):
        out=""
        out += ('src_port: ' + str(self.sport) +
                ', dst_port: ' + str(self.dport) +
                ', dst_ip: ' + str(self.dst_ip) +
                '\n containing ' + str(len(self.packets)) +
                ' packets')
        
        return out
    
def main(pcap_filename):
    streams = []
    
    print 'creating session dir...'
    split_dir = split_to_streams.main(pcap_filename)
    for p_filename in os.listdir(split_dir):
        fpath = os.path.abspath(os.path.join(split_dir,p_filename))
        stream_packets = parse_stream_packets.main(fpath)
        streams.append(dStream(stream_packets))
    
    print 'deleting session dir...'
    shutil.rmtree(split_dir)
    
    csv_filename = os.path.abspath(split_dir) + '.csv'
    csv_out = open(csv_filename,'w')
    
    first_line = 'stream_num,' + ','.join(dPacket.attr_names_as_list()) +"\n"
    csv_out.write(first_line)
    
    count_streams = 0
    for stream in streams:
        for packet in stream.packets:
            line = str(count_streams) + ',' +packet.csv_line() + "\n"
            csv_out.write(line)
        count_streams += 1
    
    csv_out.close()
    
    return streams
if __name__ == '__main__':
    args = sys.argv[1:]
    pcap_filename = args[0]
    main(pcap_filename)