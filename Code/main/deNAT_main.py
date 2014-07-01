'''
Created on Aug 13, 2013

@author: yfried
'''
from Code.Algorithms.dHost import dHost
from Code.IpId.deIpId import deIpId
from Code.TCPts import TCPts_regression
from optparse import OptionParser
from Code import parse_to_streams
from Code.parse_to_streams import split_to_streams
from Code.TCPts.dTcpTSAlg import dTcpTSAlgClass
from Code.TCPts import dTcpTSAlg
from matplotlib.pyplot import show
import os
import cPickle as pickle

flag_verbose = False

pickle_mode = False


def parse_cmd_arguments():
    """
    Set up script arguments and check for errors

    @return: (options, args) defined in optparse
    """

    usage = 'usage: %prog [options] pcap_filename'
    parser = OptionParser(usage=usage)

    parser.add_option('-d', dest="outputdir", default=None,
                      help="save output to this directory")
    parser.add_option('-s', '--std', type='float', dest='tcp_std_err',
                      default=None,
                      help='maximun valid std_err for tcp_reg')
    parser.add_option('-r', '--rval', type='float', dest='tcp_r_val',
                      default=None,
                      help='minimum valid r_val for tcp_reg')
    parser.add_option('-b', '--buffer', type='int', dest='tcp_var',
                      default=None,
                      help='% of variance allowed for tcp_ts')
    parser.add_option('-v',
                      action='store_true', dest="verbose", default=False,
                     help="set output to VERBOSE mode.")
    parser.add_option('-c',
                      action='store_true', dest='packet_csv', default=False,
                      help="create csv file with packet details")

    (options, args) = parser.parse_args()

    # check options conflicts

    # check arg num
    if len(args) < 1:
        parser.error("incorrect number of arguments")

    return options, args


def main(pcap_filename):
    pkl_filename = "{p}_pickle".format(p=pcap_filename)
    pkt_filename = "{p}_packets".format(p=pkl_filename)
    strm_filename = "{p}_streams".format(p=pkl_filename)
    if pickle_mode:
        print "pickle mode"
        p_pkt_lst = open(pkt_filename, 'rb')
        p_strm_lst = open(strm_filename, 'rb')
        stream_list = pickle.load(p_strm_lst)
        packet_list = pickle.load(p_pkt_lst)
        p_pkt_lst.close()
        p_strm_lst.close()

    else:
        stream_list, packet_list = split_to_streams.main(pcap_filename)

        # p_pkt_lst = open(pkt_filename, 'wb')
        # p_strm_lst = open(strm_filename, 'wb')
        # pickle.dump(stream_list, p_strm_lst)
        # pickle.dump(packet_list, p_pkt_lst)

    # p_pkt_lst.close()
    # p_strm_lst.close()

    sort_by_ts = dTcpTSAlgClass()
    sort_by_ipid = deIpId()

    dumy_host = dHost(packet_list[0])
    dumy_host.packets = packet_list
    sort_by_ipid.draw_hosts([dumy_host], "IPid Unsorted")

    for stream_obj in stream_list:
        stream_obj.tcp_reg = TCPts_regression.TCPts_regression(stream_obj)
        if sort_by_ts.filter_streams(stream_obj):
            sort_by_ts.step(stream_obj)
        else:
            sort_by_ts.discarded_streams.append(stream_obj)

    for packet_obj in packet_list:
        sort_by_ipid.runAlgorithm(packet_obj)

    ipid_hosts, ipid_discarded = sort_by_ipid.result()

    hosts, discarded = sort_by_ts.result()

    show()


if __name__ == '__main__':
    (options, args) = parse_cmd_arguments()

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
    main(pcap_filename)
