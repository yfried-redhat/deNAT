'''
Created on Aug 13, 2013

@author: yfried
'''

from ..parse_to_streams.streams_and_packets import dStream, dPacket
# from ..parse_to_streams.parse_stream_packets import dPacket
from scipy import stats
import sys
from operator import itemgetter
from numpy.lib.polynomial import polyval

class TCPts_regression:
    '''
    classdocs
    '''
    
    def scatter_plot(self, dStream_obj):
        '''
         return list of scattered points (x,y)
         where
         x - packet wireshark timestamp
         y - packet tcp_timestamp
        '''
        flag = False
        def map_packet_to_scatter(dPacket_obj):
            x,y = float(dPacket_obj.time),dPacket_obj.TCPts 
#             print x,y
#             sys.exit()
            if y:
                return float(x),y
#             else:
#                 flag = True
# #                 print 'found no TS'
#                 sys.exit()
#         return map(map_packet_to_scatter, dStream_obj.packets)
        ret = [map_packet_to_scatter(pkt) for pkt in dStream_obj.packets]
#         if flag:
#             print ret
#             sys.exit()

        return ret

    def __init__(self, dStream_obj):
        '''
        Constructor
        '''
#         print len(dStream_obj.packets)
#         sys.exit()
        
        scatter_list = self.scatter_plot(dStream_obj)
#         print scatter_list 
#         sys.exit()
#         print scatter_list

        
        scatter_list = [point for point in scatter_list if point]
#         print scatter_list

        if scatter_list:
            self.flag = True
            slope, intercept, r_value, p_value, std_err = stats.linregress(scatter_list)
    #         sys.exit()
            self.slope = slope
            self.intercept = intercept
            self.r_val = r_value
            self.p_val = p_value
            self.std_err = std_err
            
            self.max = max(scatter_list,key=itemgetter(1))
            self.min = min(scatter_list,key=itemgetter(1))
            
            self.x_grid = [x for x,y in scatter_list]
            
            self.line = polyval([self.slope, self.intercept], self.x_grid)
        else:
            self.flag = False
#         print scatter_list, self.max
#         sys.exit()     
     
    def __str__(self):
        out=''
        out += ('slope: ' + str(self.slope) +
                 ' intercept: ' + str(self.intercept) +
                 'R: ' + str(self.r_val) +
                 'P: ' + str(self.p_val) +
                 'std_err: ' + str(self.std_err)
                 )
        return out
     
     
    
         
