'''
Created on Aug 15, 2013

@author: yfried
'''


IPid = 'IPid'
TCPts = 'TCPts'

class Host(object):
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


    def __init__(self,match_method=[]):
        '''
        Constructor
        '''
        self.matching_methods = match_method
        self.streams = []
        self.packets = []
        
        
    def match_obj(self, match_obj, matchMethod):
        "matchin the match_obj (stream or packet) to host"
        