#!/usr/bin/python
# Copyright (c) 2003 CORE Security Technologies
#
# This software is provided under under a slightly modified version
# of the Apache Software License. See the accompanying LICENSE file
# for more information.
#
# $Id: split.py 17 2003-10-27 17:36:57Z jkohen $
#
# Pcap dump splitter.
#
# This tools splits pcap capture files into smaller ones, one for each
# different TCP/IP connection found in the original.
#
# Authors:
#  Alejandro D. Weil <aweil@coresecurity.com>
#  Javier Kohen <jkohen@coresecurity.com>
#
# Reference for:
#  pcapy: open_offline, pcapdumper.
#  ImpactDecoder.


# Note: This module was edited by Yair Fried.
# it no longer saves cap files.
# it now returns:
# list_of_streams, list_of_packet
# list_of_streams: each stream is a list of the packets belonging to the
# same stream
# list_of_packets: raw list of all pakcets in cap in the order processed


from exceptions import Exception
import sys
import pcapy
from pcapy import open_offline
from impacket.ImpactDecoder import EthDecoder
from impacket.ImpactDecoder import LinuxSLLDecoder
import os
from impacket.ImpactPacket import ImpactPacketException
from Code.parse_to_streams.streams_and_packets import dPacket
from Code.parse_to_streams.streams_and_packets import dStream
from Code.parse_to_streams.streams_and_packets import calc_wtime
from Code.main import conf


flag_csv = False


class Connection(object):
    """This class can be used as a key in a dictionary to select a connection
    given a pair of peers. Two connections are considered the same if both
    peers are equal, despite the order in which they were passed to the
    class constructor.
    """

    def __init__(self, p1, p2):
        """This constructor takes two tuples, one for each peer. The first
        element in each tuple is the IP address as a string, and the
        second is the port as an integer.
        """

        self.p1 = p1
        self.p2 = p2

    def getFilename(self):
        """Utility function that returns a filename composed by the IP
        addresses and ports of both peers.
        """
        return '%s.%d-%s.%d.pcap' % (self.p1[0], self.p1[1], self.p2[0],
                                     self.p2[1])

    def __cmp__(self, other):
        if ((self.p1 == other.p1 and self.p2 == other.p2) or
                (self.p1 == other.p2 and self.p2 == other.p1)):
            return 0
        else:
            return -1

    def __hash__(self):
        return (hash(self.p1[0]) ^ hash(self.p1[1])
                ^ hash(self.p2[0]) ^ hash(self.p2[1]))


class Decoder(object):
    def __init__(self, pcapObj, filename=None):
        # Query the type of the link and instantiate a decoder accordingly.
        datalink = pcapObj.datalink()
        if pcapy.DLT_EN10MB == datalink:
            self.decoder = EthDecoder()
        elif pcapy.DLT_LINUX_SLL == datalink:
            self.decoder = LinuxSLLDecoder()
        else:
            raise Exception("Datalink type not supported: " % datalink)

        self.pcap = pcapObj
        self.connections = {}
        # added by yair
        self.packet_count = 0
        self.packet_list = []
        self.filename = filename
        self.dir = None

#         a dictionary containing all TCP streams
        self.streams = {}

    def start(self):
        # Sniff ad infinitum.
        # PacketHandler shall be invoked by pcap for every packet.
        self.pcap.loop(0, self.packetHandler)

    def packetHandler(self, hdr, data):
        """Handles an incoming pcap packet. This method only knows how
        to recognize TCP/IP connections.
        Be sure that only TCP packets are passed onto this handler (or
        fix the code to ignore the others).

        Setting r"ip proto \tcp" as part of the pcap filter expression
        suffices, and there shouldn't be any problem combining that with
        other expressions.
        """

        global flag_verbose

        # Use the ImpactDecoder to turn the rawpacket into a hierarchy
        # of ImpactPacket instances.
        p = self.decoder.decode(data)
        ip = p.child()
        tcp = ip.child()

        # Build a distinctive key for this pair of peers.
        src = (ip.get_ip_src(), tcp.get_th_sport())
        dst = (ip.get_ip_dst(), tcp.get_th_dport())
        con = Connection(src, dst)

        wtime = calc_wtime(wts=hdr.getts())
        TCPts = None
        for opt in tcp.get_options():
            try:
                TCPts = opt.get_ts()
                break
            except ImpactPacketException:
                pass

        self.packet_count += 1
        packet = dPacket(wtime, ip.get_ip_dst(), tcp.get_th_sport(),
                         tcp.get_th_dport(), ip.get_ip_id(), TCPts,
                         self.packet_count)

        self.packet_list.append(packet)

        #add by yair - create dir for split files
        if flag_csv:
            split_dir_name = self.filename + '_TCPsessions'
            newpath = os.path.join(os.getcwd(), split_dir_name)
            self.dir = newpath

        # If there isn't an entry associated yet with this connection,
        # open a new pcapdumper and create an association.
        self.connections.setdefault(con, [])
        self.connections[con].append(packet)


def main(filename):
    # Open file
    p = open_offline(filename)

    # At the moment the callback only accepts TCP/IP packets.
    p.setfilter(r'ip proto \tcp')

    print "Reading from %s: linktype=%d" % (filename, p.datalink())

    # Start decoding process.
    m_decoder = Decoder(p, filename)
    m_decoder.start()

    streams = []
    for stream in m_decoder.connections.values():
        streams.append(dStream(stream))

    if flag_csv:
        csv_filename = os.path.abspath(m_decoder.dir) + '.csv'
        csv_out = open(csv_filename, 'w')
        first_line = ('stream_num,' +
                      ','.join(dPacket.attr_names_as_list()) + "\n")
        csv_out.write(first_line)

        count_streams = 0
        for stream in streams:
            for packet in stream.packets:
                line = str(count_streams) + ',' + packet.csv_line() + "\n"
                csv_out.write(line)
            count_streams += 1

        csv_out.close()

    return streams, m_decoder.packet_list,


# Process command-line arguments.
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "Usage: {f} <filename>".format(f=sys.argv[0])
        sys.exit(1)

    main(sys.argv[1])
