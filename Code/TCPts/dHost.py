'''
Created on Aug 15, 2013

@author: yfried
'''
from Code.parse_to_streams.streams_and_packets import dStream, dPacket


IPid = 'IPid'
TCPts = 'TCPts'

class dHost(object):
    '''
    Host
    ====
    
    @todo: add host definitions -(OS/MAC/other...) 
    
    description:
    collects all streams/packets that were tagged as belonging to the same single host
    
    contains:
    
    streams - list of parsed packet streams
    pakcets - list of parsed packets by order processed
    
    tagging method - list containing 0-2 values from [IPid, TCPts]

    '''

    
    def tcpts_init(self, ts_reg_init):
        self.host_ts = ts_reg_init
    
    def add_ts(self, ts_reg_add):
        self.host_ts += ts_reg_add
    
    def __init__(self, dObj):
        '''
        Constructor
        '''
#         self.matching_methods = match_method
        if isinstance(dObj, dStream):
            self.streams = [dObj]
            self.packets = [dObj.packets]
        elif isinstance(dObj, dPacket):
            self.packets = [dObj]
            self.streams = [dObj.stream]
            
            
        stream = self.streams[0]
        self.tcpts_init(stream.tcp_reg)
        
    def get_filter(self):
#         import pdb; pdb.set_trace()
        filters = [s.get_filter() for s in self.streams]
#         pdb.set_trace()
        return ' || '.join(filters)
            
        
    def add_obj(self, dObj):
        "add obj (stream or packet) to host"
        if isinstance(dObj, dStream):
            self.streams.append(dObj)
            self.packets += dObj.packets
#             stream = dObj
        elif isinstance(dObj, dPacket):
            self.packets += dObj
            self.streams.append(dObj.stream)
#             stream = dObj.stream
        
