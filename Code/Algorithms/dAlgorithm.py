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

    @abc.abstractmethod
    def __init__(self):
        '''
        init algorithm
        '''
#         self.hosts = []
        return
    
#     @abc.abstractmethod
#     def __init__(self)
#     """
#     """
#     return

        
    def step(self, match_obj):
        """
        perform the algorithm for a single match_obj
        return a host (old or new) to which match_obj was added
        """
        host = self.search(match_obj)
        if host is not None:
            #add match_obj to existing host
            self.add_to_host(host, match_obj)
        else:
            #init new host with match_obj
            host = self.init_host(match_obj)
            
        return host
    
        
        
        return
    
    def search(self, match_obj):
        """
        try match match_obj to existing host.
        return host.
        if fail - return None
        """
        for host in self.hosts:
            if self.calc_match(host, match_obj):
                return host
        else:
            return None
    
    @abc.abstractmethod
    def init_host(self, match_obj):
        """
        create a new host for match_obj
        """
        return
    
    
    @abc.abstractmethod
    def filter_streams(self, match_obj):
        """
        check if match_obj is valid for classification
        i.e. for TCPts - check that stream_obj.TCPts != None
        """
        return
    
#     def filter_hosts(self,host):
#         """
#         check if host is valid for classification 
#         """
#         return
#         
    
    @abc.abstractmethod
    def calc_match(self,host, match_obj):
        """check stream against host's previous streams.
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

    @abc.abstractmethod
    def log_results(self):
        return
    
class dLogger(object):
    
    def __init__(self, filename='resfile.txt'):
        self.rfile = open(filename,'w')
        
    def write(self, message):
        self.rfile.write(message)
    
    def writelines(self, lines):
        self.rfile.writelines(lines)
        
    def close(self):
        self.rfile.close()
    
    def print_to_terminal(self):
        with open(self.rfile.name, 'r') as fin:
            print fin.read()
                   
    