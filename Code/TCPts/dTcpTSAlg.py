'''
Created on Aug 23, 2013

@author: yfried
'''
from Code.Algorithms.dAlgorithm import dAlgorithm, dLogger
from Code.TCPts import dHost, TCPts_regression
import sys
from pylab import plot, show
import matplotlib.pyplot as plt
import numpy as np
from Code import Algorithms

# bellow that tcp_reg is considered untrustworthy and immediately discarded
r_val_bar = 0.99

# precentage that stream's slope and intercept can be different from
# host's and still consider match
reg_var = 12
r_val_match = 0.99
std_var = 1
p_val_prob_bar = 0.05

flag_filters = True
flag_graph = True
flag_print_res = True


class dTcpTSAlgClass(dAlgorithm):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.discarded_streams = []
        self.hosts = []
        self.reslog = dLogger('TCPts_results.txt')
        
    def search(self, stream_obj):
        return super(dTcpTSAlgClass, self).search(stream_obj)
    
    def init_host(self, stream_obj):
        new_host = dHost.dHost(stream_obj)
        self.hosts.append(new_host)
        return new_host
        
    def filter_streams(self, stream_obj):
#         if stream_obj.TCPts is None:
#             return False
        if stream_obj.tcp_reg is None or not stream_obj.tcp_reg.flag:
            return False
#         import pdb; pdb.set_trace()
        if stream_obj.tcp_reg.r_val < r_val_bar:
            return False
        
        return True
    
    def filter_hosts(self, host_obj):
        if host_obj.host_ts is None:
            return False
        else:
            return True
    
#     def calc_variance(self, tcp_regA, tcp_regB):
#         def within_range(a,b):
#             '''
#             calculate the deviation of deviation of b from a
#             return true if it's within defined "reg_var"
#             '''
# #             print reg_var
# #             sys.exit()
#             prcnt =  100 * float (abs(a - b))/float (a)
#             return (prcnt < reg_var)
#         
#         if (within_range(tcp_regA.slope, tcp_regB.slope) and 
#             within_range(tcp_regA.intercept, tcp_regB.intercept)):
#             return True
#         else:
#             return False
#         
    
    
    def calc_match(self, host_obj, stream_obj):
#         return self.calc_variance(host_obj.host_ts, stream_obj.tcp_reg)
#         import pdb; pdb.set_trace()
        new_host_tcpreg = host_obj.host_ts + stream_obj.tcp_reg
#         return (new_host_tcpreg.r_val >= r_val_match)
        return (new_host_tcpreg.std_err < std_var)
        
        
        
        
    def add_to_host(self, host, stream_obj):
        """
        add match_obj to the host.
        
        host.streams.append(match_obj)
        stream.host = host        
        """
        host.add_obj(stream_obj)
        # add ts_reg
        host.add_ts(stream_obj.tcp_reg)
        
    def result(self):
        if flag_filters:
            self.write_filters_to_file()
        if flag_graph:
            self.draw_hosts()
        self.grade_hosts()
        self.log_results()
        return self.hosts, self.discarded_streams


    def write_filters_to_file(self):
        f = open('filter_hosts_by_tcp_timestamps', 'w')
        for i, host in enumerate(self.hosts):
            msg = 'host #{n}\n'.format(n=i)
            f.write(msg)
            msg = host.get_filter()
            f.write(msg + '\n')
        f.close()
        return f
    
    def draw_hosts(self):
            # Have a look at the colormaps here and decide which one you'd like:
        # http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html
    #     num_plots = len(hosts)
    #     colormap = plt.cm.gist_ncar(np.random.random())
    #     colors = iter(cm.rainbow(np.linspace(0, 1)))
        ttl='hosts found using TCP timestamps'
        fig = plt.figure(ttl)
        ax1 = fig.add_subplot(111)
    #     ax1.gca().set_color_cycle(['red', 'green', 'blue', 'yellow'])
    #     ax1.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, num_plots)])
    
        labels = []
        for i, host in enumerate(self.hosts):
            x,y = host.host_ts.plot_scatter(False)
            ax1.scatter(x,y,color=plt.cm.gist_ncar(np.random.random()))
            labels.append('host {num}'.format(num=i+1))
#         import pdb; pdb.set_trace()
        ax1.set_title(ttl)
        
        ax1.legend(labels, ncol=4, loc=(0.5,-0.1), 
#                 bbox_to_anchor=[1.1, 0.5], 
               columnspacing=1.0, labelspacing=0.0,
               handletextpad=0.0, handlelength=1.5,
               fancybox=True, shadow=True)
        plt.draw()
        fig.savefig('hosts_TCPts.jpg',bbox_inches=0)
#         plt.show(block=False)
    
    def grade_hosts(self):
        sure_hosts = list()
        no_hosts = list()
        prob_hosts = list()
        for h in self.hosts:
            if len(h.streams) <= 2: #ignore hosts with less thanb 2 streams
                no_hosts.append(h)
            elif h.host_ts.p_val == 0.0 and h.host_ts.std_err < std_var:
                sure_hosts.append(h)
            elif h.host_ts.p_val < p_val_prob_bar:
                prob_hosts.append(h)
            else:
                no_hosts.append(h)
        self.hosts = dict(sure_hosts=sure_hosts,
                          prob_hosts=prob_hosts,
                          no_hosts=no_hosts)
    
    def log_results(self):
        lines = list()
        lines.append('discard criteria:\n\tno tcp_ts\n\tcp_reg.r_val < {rval}'.format(rval=r_val_bar))
        lines.append('match criteria (append stream to host if):\n\tnew_tcp_reg.std_err < {std}'.format(std=std_var))
        lines.append('hosts found:\n {sure}\nlow probability: {prob}\nbad id: {noh}'.format(sure=len(self.hosts['sure_hosts']),
                                                                                            prob=len(self.hosts['prob_hosts']),
                                                                                            noh=len(self.hosts['no_hosts'])
                                                                                            ))
        lines.append('discarded streams (not fitting for tcp_ts criteria): {dis}'.format(dis=len(self.discarded_streams)))
        for key in self.hosts.keys():
            lines.append('hosts type {type}'.format(type=key))
            for i, host in enumerate(self.hosts[key]):
                lines.append('host #{n}:'.format(n=i+1))
                lines.append('matched {n} TCP streams'.format(n=len(host.streams)))
                lines.append('tcp regression: ' + str(host.host_ts))
#             lines.append('') #empty line
        
        lines = '\n'.join(lines)
        self.reslog.write(lines)
        self.reslog.close()
        if flag_print_res:
            self.reslog.print_to_terminal()