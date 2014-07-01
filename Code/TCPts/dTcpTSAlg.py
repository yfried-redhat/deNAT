'''
Created on Aug 23, 2013

@author: yfried
'''
import matplotlib.pyplot as plt
import numpy as np

from Code.Algorithms import dHost
from Code.Algorithms.dAlgorithm import dAlgorithm, flag_print_res, flag_graph
from Code.Algorithms.dAlgorithm import dLogger

# bellow that tcp_reg is considered untrustworthy and immediately discarded
r_val_bar = 0.99

# precentage that stream's slope and intercept can be different from
# host's and still consider match
reg_var = 12
r_val_match = 0.99
std_var = 1
p_val_prob_bar = 0.05

flag_filters = True


class dTcpTSAlgClass(dAlgorithm):

    def __init__(self):
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

    def calc_match(self, host_obj, stream_obj):
        new_host_tcpreg = host_obj.host_ts + stream_obj.tcp_reg
        return new_host_tcpreg.std_err < std_var

    def add_to_host(self, host, stream_obj):
        """add match_obj to the host.

        host.streams.append(match_obj)
        stream.host = host
        """
        host.add_obj(stream_obj)
        # add ts_reg
        host.add_ts(stream_obj.tcp_reg)

    def result(self):
        self.grade_hosts()
        if flag_filters:
            self.write_filters_to_file()
        if flag_graph:
            self.draw_hosts()
        self.log_results()
        return self.hosts, self.discarded_streams

    def write_filters_to_file(self):
        f = open('filter_hosts_by_tcp_timestamps', 'w')
        for j, key in enumerate(self.hosts.keys()):
            for i, host in enumerate(self.hosts[key]):
                msg = 'host #{k}.{n}\n'.format(k=j+1, n=i+1)
                f.write(msg)
                msg = host.get_filter()
                f.write(msg + '\n')
        f.close()
        return f

    def draw_hosts(self):
    # Have a look at the colormaps here and decide which one you'd like:
    # http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html
        ttl = 'hosts found using TCP timestamps'
        fig = plt.figure(ttl)
        ax1 = fig.add_subplot(111)

        labels = []
        for j, key in enumerate(self.hosts.keys()):
            for i, host in enumerate(self.hosts[key]):
                x, y = host.host_ts.plot_scatter(False)
                ax1.scatter(x, y, color=plt.cm.gist_ncar(np.random.random()))
                labels.append('host {k}.{num}'.format(k=j+1, num=i+1))
#         import pdb; pdb.set_trace()
        ax1.set_title(ttl)

        ax1.legend(labels, ncol=4, loc=(0.5, -0.1),
                   columnspacing=1.0, labelspacing=0.0,
                   handletextpad=0.0, handlelength=1.5,
                   fancybox=True, shadow=True)
        plt.draw()
        fig.savefig('hosts_TCPts.jpg', bbox_inches=0)

    def grade_hosts(self):
        sure_hosts = list()
        no_hosts = list()
        prob_hosts = list()
        for h in self.hosts:
            if len(h.streams) <= 2:  # ignore hosts with less than 2 streams
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
        lines.append("TCP timestamps results:")
        lines.append('discard criteria:\n\t'
                     'no tcp_ts\n\t'
                     'cp_reg.r_val < {rval}'.format(rval=r_val_bar))
        lines.append('match criteria (append stream to host if):\n\t'
                     'new_tcp_reg.std_err < {std}'.format(std=std_var))
        lines.append('hosts found:\n'
                     '{sure}\n'
                     'low probability: {prob}\n'
                     'bad id: {noh}'.format(sure=len(self.hosts['sure_hosts']),
                                            prob=len(self.hosts['prob_hosts']),
                                            noh=len(self.hosts['no_hosts'])))
        lines.append('discarded streams '
                     '(not fitting for tcp_ts criteria): '
                     '{dis}'.format(dis=len(self.discarded_streams)))
        for j, key in enumerate(self.hosts.keys()):
            lines.append('{n}. hosts type {type}'.format(n=j+1, type=key))
            for i, host in enumerate(self.hosts[key]):
                lines.append('\thost #{t}.{n}:'.format(t=j+1, n=i+1))
                lines.append('\tmatched {n} TCP streams'.format(
                    n=len(host.streams)))
                lines.append('\ttcp regression: ' + str(host.host_ts))

        lines = '\n'.join(lines)
        self.reslog.write(lines)
        self.reslog.close()
        if flag_print_res:
            self.reslog.print_to_terminal()
