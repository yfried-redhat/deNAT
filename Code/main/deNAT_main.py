'''
Created on Aug 13, 2013

@author: yfried
'''
# from ..parse_to_streams import get_streams_from_cap
from ..TCPts import TCPts_regression
from optparse import OptionParser
from Code import parse_to_streams
from Code.parse_to_streams import split_to_streams
from Code.TCPts.dTcpTSAlg import dTcpTSAlgClass
from Code.TCPts import dTcpTSAlg
import numpy as np
# from matplotlib import cm
import itertools
from matplotlib.pyplot import show
import os

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
    parser.add_option('-d', dest="outputdir", default=None,
                      help="save output to this directory")
    parser.add_option('-s','--std', type='float', dest='tcp_std_err', default=None,
                      help='maximun valid std_err for tcp_reg')
    parser.add_option('-r','--rval', type='float', dest='tcp_r_val', default=None,
                      help='minimum valid r_val for tcp_reg')
    parser.add_option('-b','--buffer', type='int', dest='tcp_var', default=None,
                      help='% of variance allowed for tcp_ts')
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
    stream_list, packet_list = split_to_streams.main(pcap_filename)
    
    sort_by_ts = dTcpTSAlgClass()
    
    for stream_obj in stream_list:
        stream_obj.tcp_reg = TCPts_regression.TCPts_regression(stream_obj)
        if sort_by_ts.filter_streams(stream_obj):
            sort_by_ts.step(stream_obj)
        else:
            sort_by_ts.discarded_streams.append(stream_obj)
            
    hosts, discarded = sort_by_ts.result()
        
    show()



if __name__ == '__main__':
    
    (options, args) = parse_cmd_arguments()
    
#     args = sys.argv[1:]
    pcap_filename = args[0]
    
    parse_to_streams.split_to_streams.flag_csv = options.packet_csv
    parse_to_streams.split_to_streams.flag_verbose = options.verbose
    
    if options.outputdir is not None:
        if not os.path.exists(options.outputdir):
            os.makedirs(options.outputdir)
        os.chdir(options.outputdir)
        print 'writing results to {path}'.format(path=options.outputdir)
    if options.tcp_var is not None:
        dTcpTSAlg.reg_var = options.tcp_var
    if options.tcp_r_val is not None:
        dTcpTSAlg.r_val_bar = options.tcp_r_val
    if options.tcp_std_err is not None:
        dTcpTSAlg.std_var = options.tcp_std_err
#         print dTcpTSAlg.reg_var
#         sys.exit()
    main(pcap_filename) #, verbose=options.verbose)
#     print 'hello'