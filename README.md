deNAT
=====

count hosts behind a NAT

========================================================
usage (from within the deNAT dir):
python -m Code.main.deNAT_main <pcap-filename>

pcap-filename - a capture file containing a single-side sniffing capture where all packets has the same source IP (NAT)

========================================================

terms
=====
stream - tcp session. identified by 5-tuple (IP,port,protocol)



packages
========
main - project executed from here
pcap_to_stream - parse packets and group them by stream 
TCPts - tag tcp-stream with 
