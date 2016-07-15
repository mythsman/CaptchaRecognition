'''
Created on Jul 15, 2016

@author: myths
'''
from abc import ABCMeta, abstractmethod
import os, time, shutil, urllib2

class Captcha(object):
    
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.name = ''
        self.path = ''
        self.url = ''
        self.suffix = ''
    
    '''
    Downloads captcha pictures from server. 
    '''
    def download(self, num):
        time1 = time.time()
        
        downloadPath = os.path.join(self.path, 'unrecognized')
        if os.path.exists(downloadPath):
            shutil.rmtree(downloadPath)
        os.mkdir(downloadPath)
        
        for i in xrange(num):
            idx = i + 1
            data = urllib2.urlopen(self.url).read()
            with open(os.path.join(downloadPath, str(idx) + self.suffix), 'wb') as f:
                f.write(data)       
            
        time2 = time.time();
        costTime = int((time2 - time1) * 1000)
        print "Download", num, "pictures in", costTime, "ms."
    
    '''
    Split all recognized pictures into different directories by label. 
    '''
    def preprocess(self):
        print "This is 'preprocess' method"
            
    @abstractmethod
    def _splitImage(self, img):
        print "This is '_splitImage' method"
