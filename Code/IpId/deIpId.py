'assuming that packet has ipId and arrival time'
from ..parse_to_streams.streams_and_packets import dStream, dPacket
from Code.TCPts import dHost
from Code.Algorithms.dAlgorithm import dAlgorithm, dLogger

#         captured time
#       self.sn = sn
#        self.time = wtime
#         packet Serial Number within session
        
#        self.IPid = IPid
class matchTypes:
    NOT_MATCH           = 0
    PERFECT_MATCH       = 1
    OUT_OF_ORDER_MATCH  = 2
    DUP                 = 3
class deIpId:    
    def __str__(self):
        return "deIpId class"
    def __init__(self, timeLim=300, gapLim=64, timeFac=5, gapFac=70, fSize=50):
        self.timeLim = timeLim
        self.gapLim  = gapLim
        self.timeFac = timeFac
        self.gapFac  = gapFac
        self.fSize   = fSize
        self.newPacket = dPacket
        self.lastRecievedPacket = None
        self.hosts = []
    
    def init_host(self, stream_obj):
        new_host = dHost.dHost(stream_obj)
        self.hosts.append(new_host)
        return new_host
        
    def checkOnHost(self, newPacket, host):
        self.newPacket = newPacket
        self.lastRecievedPacket = host.packets[-1]
        #we have already recieved at least one packet
        newLastTimeDelta = abs(newPacket.time - self.lastRecievedPacket.time)
        newLastTimeDelta = newLastTimeDelta % (2^16)
        pIdDelta = self.IPid-self.lastRecievedPacket % (2^16)
        if  newLastTimeDelta > self.timeLim or newPacket.Ipid == 0:
            return matchTypes.NOT_MATCH
            #do nothing this packet doesn't match
        elif (pIdDelta == 1):
            return matchTypes.PERFECT_MATCH
        elif  (abs(newPacket.Ipid - self.lastRecievedPacket.Ipid) < self.gapLim):
            if (self.checkPacketExists(self,host, newPacket)):
                return matchTypes.DUP
            else:
                return matchTypes.OUT_OF_ORDER_MATCH

    #check if the packet exists on specific host
    def checkPacketExists(self,host, packet):
        for pckt in host:
            if (packet == pckt):
                return True;        
        return False;

    #go over all hosts and trying add the packet to specific host
    #if not added to host create a new host
    def goOverAllHosts(self,packet): 
        for h in self.hosts:                        
            if (self.checkOnHost(self, packet, h) == matchTypes.PERFECT_MATCH):
                h.append(packet);
                return;  
            elif (self.checkOnHost(self, packet, h) == matchTypes.NOT_MATCH):
                return;
            elif (self.checkOnHost(self, packet, h) == matchTypes.OUT_OF_ORDER_MATCH):
                h.append(packet);
                return;  
            elif (self.checkOnHost(self, packet, h) == matchTypes.DUP):
                return;
             
    def runAlgorithm (self):            
        #TBD       
        return 1;
                