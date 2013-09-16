#!/usr/bin/python
'''
Created on Apr 21, 2013

@author: yfried

this module contains classes for packet parsing:
dPacket - parsed packets
dStream - collecting dPackets belonging to the same tcp stream


'''
from pcapy import open_offline, PcapError
import sys
from impacket import ImpactDecoder
from impacket.ImpactPacket import ImpactPacketException
from decimal import Decimal





def calc_wtime(wts):
    int_num, frac_num = wts
    frac_num = Decimal(frac_num)
    while frac_num>=1:
        frac_num = Decimal(frac_num/10)
    return Decimal(int_num + frac_num)


class dPacket:
    def __init__(self, wtime, dstip,src_port,dst_port, IPid, TCPts, sn=None):
#         captured time
        self.sn = sn
        self.time = wtime
#         packet Serial Number within session
        
        self.dst_ip = dstip
        self.sport = src_port
        self.dport = dst_port
        
        self.IPid = IPid
        self.TCPts = TCPts
        self.stream = None
    
    def __str__(self):
        out = ('SN: '+ str(self.sn) +
               ' time: ' + str(self.time) +
            ", dstIP: " + str(self.dst_ip) +
            ", src port: " + str(self.sport) +
            ", dst port: " + str(self.dport) + 
            "\nIPid: " + str(self.IPid))
            
        if self.TCPts:
            out += ", TCPts: " + str(self.TCPts)
        return out
    
    def attr_val_as_list(self):
        return [self.time, self.dst_ip,self.sport,self.dport,self.IPid,self.TCPts]
        
    @staticmethod
    def attr_names_as_list():
        return ["SN","time", "dst_ip","sport","dport","IPid","TCPts"]
        
    def csv_line(self):
        str_list = [str(val) for val in self.attr_val_as_list()]
        out = ",".join(str_list)
        return out
        
    
def parse_packet(header, data):
#     eth = dpkt.ethernet.Ethernet(buf)
#     ip = eth.data
#     if ip.get_proto
    
    wtime = calc_wtime(wts=header.getts())
    eth = ImpactDecoder.EthDecoder().decode(data)
    ip = eth.child()
    tcp = ip.child()
    
    TCPts = None
    for opt in tcp.get_options():
        try:
            TCPts = opt.get_ts()
            break
        except ImpactPacketException:
            pass
            
    
    return dPacket(wtime, ip.get_ip_dst(), tcp.get_th_sport(),
                   tcp.get_th_dport(), ip.get_ip_id(), TCPts)


  
class dStream:
    def __init__(self, packets):
        first_pkt = packets[0]
        self.dst_ip = first_pkt.dst_ip
        self.dport = first_pkt.dport
        self.sport = first_pkt.sport
        
        self.host = None
        
        #list containing packet data of the session
        self.packets = packets
        for pkt in self.packets:
            pkt.host = self
        
    def __str__(self):
        out=""
        out += ('src_port: ' + str(self.sport) +
                ', dst_port: ' + str(self.dport) +
                ', dst_ip: ' + str(self.dst_ip) +
                '\n containing ' + str(len(self.packets)) +
                ' packets')
        
        return out

    def get_filter(self):
        cap_filter = '((tcp.srcport == {sport}) && (tcp.dstport == {dport}) && (ip.dst == {ip}))'.format(
              sport=self.sport,
              dport=self.dport,
              ip=self.dst_ip 
        )
        return cap_filter

def parse_stream_packtes(pcap_session):
    (header,data) = pcap_session.next()
    
    stream_pkts = []
    
    while header:
        packet = parse_packet(header, data)
        stream_pkts.append(packet)

        try:
            (header,data) = pcap_session.next()
        except PcapError:
            header = None
    return stream_pkts
    
def main(pcap_session_filename):
#     args = sys.argv[1:]
#     pcap_session_filename = args[0]
    
    pcap_session = open_offline(pcap_session_filename)
    
    stream_packets = parse_stream_packtes(pcap_session)
    
    return stream_packets
    
    
#     print stream_pkts[-1].time
#     print type(stream_pkts[-1].time)
#     print stream_pkts[-1].time - stream_pkts[-2].time

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "Usage: %s <filename>" % sys.argv[0]
        sys.exit(1)
        
    main(sys.argv[1])