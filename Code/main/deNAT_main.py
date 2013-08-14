'''
Created on Aug 13, 2013

@author: yfried
'''
import sys
from ..parse_to_streams import get_streams_from_cap
from ..TCPts import TCPts_regression
from pylab import plot, show
from optparse import OptionParser
from Code import parse_to_streams
# from Code import parse_to_streams, TCPts
# from ..parse_to_streams import get_streams_from_cap
# import TCPts.TCPts_regression
 
flag_verbose = False



def parse_cmd_arguments():
    """
    set up script arguments and check for errors
    @return: (options, args) defined in optparse
    
    """
#     choice_colores = ('red', 'blue','green','black','yellow', 'black')
    usage = 'usage: %prog [options] pcap_filename' #1 filename2 ...'
    parser = OptionParser(usage=usage)
    
#     parser.add_option('-u',
#                       action='store_true',dest="underscore", default=False,
#                       help="underscore matching text")
#     parser.add_option('-c',
#                       choices=choice_colores, dest="color",
#                       help="color the ouput. options are: "+",".join(choice_colores))
#     parser.add_option('-w', dest="HTMLFile",
#                       help="print to HTMLFile")
    parser.add_option('-v',
                     action='store_true',dest="verbose", default=False,
                     help="set output to VERBOSE mode.")
    parser.add_option('-c',
                      action='store_true',dest='packet_csv', default=False,
                      help="create csv file with packet details")
    (options, args) = parser.parse_args()
    
    
    # check options conflicts
#     if options.count_match and (options.HTMLFile is not None or options.color is not None or 
#             options.underscore):
#             parser.error("options -d and -wcu are mutally exclusive")
#     
#     if options.xclude and (options.color is not None or options.underscore):
#             parser.error("options -x and -cu are mutally exclusive")
    
    # check arg num
    if len(args) < 1:
        parser.error("incorrect number of arguments")
    
    return options, args




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
    
    (options, args) = parse_cmd_arguments()
    
#     args = sys.argv[1:]
    pcap_filename = args[0]
    
    parse_to_streams.get_streams_from_cap.flag_csv = options.packet_csv
    parse_to_streams.split_to_streams.flag_verbose = options.verbose
    main(pcap_filename) #, verbose=options.verbose)
#     print 'hello'