'assuming that packet has ipId and arrival time'
import matplotlib.pyplot as plt
import numpy as np

from Code.Algorithms import dHost
from Code.Algorithms.dAlgorithm import dAlgorithm, flag_print_res, flag_graph, dLogger
from Code.parse_to_streams.streams_and_packets import dPacket

class matchTypes(object):
    NOT_MATCH = 0
    PERFECT_MATCH = 1
    OUT_OF_ORDER_MATCH = 2
    SKIP = 3
    DUP = 4


class deIpId(object):
    def __str__(self):
        return "deIpId class"

    def __init__(self, timeLim=300, gapLim=32, timeFac=5, gapFac=30,
                 fSize=500):
        self.timeLim = timeLim
        self.gapLim = gapLim
        self.timeFac = timeFac
        self.gapFac = gapFac
        self.fSize = fSize
        self.newPacket = dPacket
        self.lastRecievedPacket = None
        self.hosts = []

        self.reslog = dLogger('IPid_results.txt')

    def init_host(self, obj):
        new_host = dHost.dHost(obj)
        self.hosts.append(new_host)
        return new_host

    def checkOnHost(self, newPacket, host):
        self.newPacket = newPacket
        self.lastRecievedPacket = host.packets[-1]
        #we have already recieved at least one packet
        newLastTimeDelta = abs(newPacket.time - self.lastRecievedPacket.time)
        pIdDelta = (self.newPacket.IPid -
                    self.lastRecievedPacket.IPid) % 2 ** 16
        if newLastTimeDelta > self.timeLim or newPacket.IPid == 0:
            return matchTypes.NOT_MATCH
            #do nothing this packet doesn't match
        elif pIdDelta == 1:
            return matchTypes.PERFECT_MATCH
        elif abs(newPacket.IPid - self.lastRecievedPacket.IPid) < self.gapLim:
            if self.checkPacketExists(host, newPacket):
                return matchTypes.DUP
            else:
                if newPacket.time < self.lastRecievedPacket.time:
                    # print "OutOfOrderException\n packet {p}" \
                    #       "\nlastRecieved {l}".format(
                    #     p=newPacket,
                    #     l=self.lastRecievedPacket)
                    return matchTypes.OUT_OF_ORDER_MATCH
                else:
                    return matchTypes.SKIP

    # check if the packet exists on specific host
    def checkPacketExists(self, host, packet):
        return packet.IPid in [p.IPid for p in host.packets]

    # go over all hosts and trying add the packet to specific host
    # if not added to host create a new host
    def goOverAllHosts(self, packet):
        for h in self.hosts:
            match_val = self.checkOnHost(packet, h)
            if match_val == matchTypes.PERFECT_MATCH:
                h.add_obj(packet)
                break
            elif match_val == matchTypes.NOT_MATCH:
                break
            elif match_val == matchTypes.SKIP:
                h.add_obj(packet)
                break
            elif match_val == matchTypes.OUT_OF_ORDER_MATCH:
                break
            elif match_val == matchTypes.DUP:
                break
        else:
            self.init_host(packet)  # Create a new host

    def draw_hosts(self, host_list, title):
        ttl = title
        fig = plt.figure(ttl)
        ax1 = fig.add_subplot(111)
        labels = []

        for i, host in enumerate(host_list):
            x = list()
            y = list()
            for p in host.packets:
                try:
                    x.append(p.time)
                    y.append(p.IPid)
                except ValueError:
                    continue

            ax1.scatter(x, y, color=plt.cm.gist_ncar(np.random.random()))
            labels.append('host {k}'.format(k=i))
        ax1.set_title(ttl)

        ax1.legend(labels, ncol=4, loc=(0.5, -0.1),
                   columnspacing=1.0, labelspacing=0.0,
                   handletextpad=0.0, handlelength=1.5,
                   fancybox=True, shadow=True)
        plt.draw()
        fig.savefig('{t}.jpg'.format(t=title), bbox_inches=0)

    #for each packet runAlgorithm should be called
    def runAlgorithm(self, packet):
        self.goOverAllHosts(packet)

    #merging hosts which are close enough
    #TBD
    def mergeHosts(self):
        final = []
        # maybe sort self.hosts by first/last packet time?
        self.hosts = sorted(self.hosts, key=lambda host: host.packets[0].sn)
        while self.hosts:
            # until hosts_list is empty
            final_host = self.hosts.pop(0)
            skip_hosts = []
            # collect all hosts that match final_host:
            for h in self.hosts:
            # iterate over list without final_host
                if self.match_hosts(final_host, h):
                    # add h to final_host
                    final_host.packets = final_host.packets + h.packets
                    skip_hosts.append(h)
                # remove skip_hosts from hosts_list
            # (hosts_list = hosts_list - skip_hosts):
            self.hosts = [h for h in self.hosts if h not in skip_hosts]
            # add final_host to final
            final.append(final_host)

        # fiter out hosts with less than self.fSize packets
        self.hosts = [h for h in final if len(h.packets) >= self.fSize]
        self.nonHosts = [h for h in final if not h in self.hosts]

        return self.hosts, self.nonHosts

    def match_hosts(self, hostA, hostB):
        if ((abs(hostB.packets[0].IPid - hostA.packets[-1].IPid) <=
             self.gapFac * self.gapLim) and
                (abs(hostB.packets[0].time - hostA.packets[-1].time) <=
                 self.timeFac * self.timeLim)):
            return True
        else:
            return False

    def log_results(self):
        lines = list()
        lines.append("IPid results:")
        lines.append('discard criteria:\n\t'
                     'number of packets < {rval}'.format(rval=self.fSize))
        lines.append('match criteria (append packet to host if):\n\t'
                     'packet.IPid is within {std} form last '
                     'packet.IPid'.format(std=self.gapLim))
        lines.append('hosts found:\n'
                     '{sure}\n'.format(sure=len(self.hosts)))
        lines.append('discarded hosts '
                     '(not fitting for discard criteria): '
                     '{dis}'.format(dis=len(self.nonHosts)))

        lines = '\n'.join(lines)
        self.reslog.write(lines)
        self.reslog.close()
        if flag_print_res:
            self.reslog.print_to_terminal()

    def result(self):
        # self.draw_hosts(self.hosts, "IPid before merge")
        hosts, discarded = self.mergeHosts()
        self.log_results()
        if flag_graph:
            self.draw_hosts(hosts, "IPid after merge")
            self.draw_hosts(discarded, "IPid discarded hosts")
        return hosts, discarded

        # def imidiate_draw(self):
        #     self.draw_hosts(self.hosts, "%d packets" % sum([len(h.packets)
        # for h in self.hosts]))
        #     plt.show()
