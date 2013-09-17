'''
Created on Aug 13, 2013

@author: yfried
'''
# from ..parse_to_streams import get_streams_from_cap
from ..TCPts import TCPts_regression
from pylab import plot, show
import matplotlib.pyplot as plt
from optparse import OptionParser
from Code import parse_to_streams
from Code.parse_to_streams import split_to_streams
from Code.TCPts.dTcpTSAlg import dTcpTSAlgClass
from Code.TCPts import dTcpTSAlg
import numpy as np
# from matplotlib import cm
import itertools

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
#     import pdb; pdb.set_trace()
    print 'hosts', len(hosts)

    # Have a look at the colormaps here and decide which one you'd like:
    # http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html
#     num_plots = len(hosts)
#     colormap = plt.cm.gist_ncar(np.random.random())
#     colors = iter(cm.rainbow(np.linspace(0, 1)))
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
#     ax1.gca().set_color_cycle(['red', 'green', 'blue', 'yellow'])
#     ax1.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, num_plots)])

    labels = []
    for i, host in enumerate(hosts):
        x,y = host.host_ts.plot_scatter(False)
        ax1.scatter(x,y,color=plt.cm.gist_ncar(np.random.random()))
        labels.append('host {num}'.format(num=i))
    
    ax1.legend(labels, ncol=4, loc='upper center', 
           bbox_to_anchor=[0.5, 1.1], 
           columnspacing=1.0, labelspacing=0.0,
           handletextpad=0.0, handlelength=1.5,
           fancybox=True, shadow=True)
    show()
        
#         print len(host.streams)
    print 'discarded', len(discarded)
#         print tcp_reg
#         if tcp_reg.flag:
#             plot(tcp_reg.x_grid, tcp_reg.line)
#         print tcp_reg.x_grid
#         print tcp_reg.line
#         sys.exit()
        
#     show()

if __name__ == '__main__':
    
    (options, args) = parse_cmd_arguments()
    
#     args = sys.argv[1:]
    pcap_filename = args[0]
    
    parse_to_streams.split_to_streams.flag_csv = options.packet_csv
    parse_to_streams.split_to_streams.flag_verbose = options.verbose
    
    if options.tcp_var is not None:
        dTcpTSAlg.reg_var = options.tcp_var
#         print dTcpTSAlg.reg_var
#         sys.exit()
    main(pcap_filename) #, verbose=options.verbose)
#     print 'hello'