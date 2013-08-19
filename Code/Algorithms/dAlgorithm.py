'''
Created on Aug 15, 2013

@author: yfried
'''
import abc


class dAlgorithm(object):
    '''
    classdocs
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        '''
        init algorithm
        '''
        return
    
#     @abc.abstractmethod
#     def __init__(self)
#     """
#     """
#     return

        
    @abc.abstractmethod
    def step(self, match_obj):
        """
        perform the algorithm for a single match_obj
        """
        host = self.search(match_obj)
        if host is not None:
            self.add_to_host(host, match_obj)
        else:
            host = self.init_host(match_obj)
            
        return host

    
        
    @abc.abstractmethod
    def filter_streams(self, match_obj):
        """
        check if match_obj is valid for classification
        i.e. for TCPts - check that stream_obj.TCPts != None
        """
        return
    
    def filter_hosts(self,host):
        """
        check if host is valid for classification 
        """
        return
        
        
    
    def search(self, match_obj):
        """
        try match match_obj to existing host.
        return host.
        if fail - return None
        """
        return
    
    def init_host(self, match_obj):
        """
        create a new host for match_obj
        """
        return
    
    @abc.abstractmethod
    def calc_match(self,host ,stream_obj):
        """check stream against previous streams.
        return:
        @todo: choose between:
        1. boolean - belongs to list or not
        or
        2. probability of match
        """
        return
    
    @abc.abstractmethod
    def add_to_host(self, host, match_obj):
        """
        add match_obj to the host.
        
        host.streams.append(match_obj)
        stream.host = host        
        """
        return
    
            
    