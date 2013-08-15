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
    
    tagging method - list containing 0-2 values from [IPid, TCPts]

    '''


    def __init__(self,tagging=[]):
        '''
        Constructor
        '''
        self.tagging = tagging
        self.streams = []