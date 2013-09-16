'''
Created on Aug 18, 2013

@author: yfried
'''

from Code.Algorithms import dHost

class dNat(object):
    '''
    classdocs
    '''


    def __init__(self,streams, packets):
        '''
        Constructor
        '''
        self.streamss = streams
        self.packets = packets
        self.hosts = []
        
        
    def match_obj(self, match_obj, matchMethod):
        
        for host in hosts:
            if matchMethod in host.matching_methods:
                #try to match match_obj to host
                