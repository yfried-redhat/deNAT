'''
Created on Aug 13, 2013

@author: yfried
'''
import sys
from ..parse_to_streams import get_streams_from_cap
from ..TCPts import TCPts_regression
from pylab import plot, show
# from Code import parse_to_streams, TCPts
# from ..parse_to_streams import get_streams_from_cap
# import TCPts.TCPts_regression
 
def main(pcap_filename):
    stream_list = get_streams_from_cap.main(pcap_filename)
    for stream_obj in stream_list:
        tcp_reg = TCPts_regression.TCPts_regression(stream_obj)
#         print tcp_reg
        if tcp_reg.flag:
            plot(tcp_reg.x_grid, tcp_reg.line)
#         print tcp_reg.x_grid
#         print tcp_reg.line
#         sys.exit()
        
    show()

if __name__ == '__main__':
    args = sys.argv[1:]
    pcap_filename = args[0]
    main(pcap_filename)
#     print 'hello'