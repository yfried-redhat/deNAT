'''
Created on Aug 15, 2013

@author: yfried
'''
import abc
from Code.parse_to_streams.streams_and_packets import dStream


class matchingMethod(object):
    '''
    classdocs
    '''
    __metaclass__ = abc.ABCMeta

#     def __init__(selfparams):
#         '''
#         Constructor
#         '''
    
    @abc.abstractmethod
    def checkStream(self,stream_list ,stream_obj):
        """check stream against previous streams.
        return:
        @todo: choose between:
        1. boolean - belongs to list or not
        or
        2. probability of match
        """
        return