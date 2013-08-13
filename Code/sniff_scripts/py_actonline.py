'''
Created on May 7, 2013

@author: yfried

usage <module> interval amount
will access a list of sites every INTERVAL seconds for AMOUNT times 
'''
import subprocess
import threading
import sys
import time
import urllib2

class RepeatEvery(threading.Thread):
    def __init__(self, interval, func, *args, **kwargs):
        threading.Thread.__init__(self)
        self.interval = interval  # seconds between calls
        self.func = func          # function to call
        self.args = args          # optional positional argument(s) for call
        self.kwargs = kwargs      # optional keyword argument(s) for call
        self.runable = True
    def run(self):
        while self.runable:
            self.func(*self.args, **self.kwargs)
            time.sleep(self.interval)
    def stop(self):
        self.runable = False



def get_all_sites(url="http://www.ynet.co.il"):
    # url_dict = {
                # "ynet": "http://www.ynet.co.il",
                # "nrg": "http://www.nrg.co.il",
                # "kipa":"http://www.kipa.co.il"
                # }
    #for site,url in url_dict.items():
#         threading.Timer(5.0, subprocess.call,args=[["wget", url]]).start()
    #subprocess.call(["wget", url])
    print url
    response = urllib2.urlopen(url)
    html = response.read()
    print html

def main(interval, limit, url):
#     sys.exit()
    print 'starting!'
    thread = RepeatEvery(interval, get_all_sites, url)
    thread.start()
    thread.join(limit)
    thread.stop()
    print 'done!'
	
    

if __name__ == '__main__':
    interval = float(sys.argv[1])
    limit = int(sys.argv[2])
    url = sys.argv[3]
    
    main(interval, limit, url)