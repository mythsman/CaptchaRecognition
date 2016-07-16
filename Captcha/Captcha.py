'''
Created on Jul 15, 2016

@author: myths
'''
from abc import ABCMeta, abstractmethod
import os, time, shutil, urllib2, cv2


class Captcha(object):
    __metaclass__ = ABCMeta
    
    path = ''
    name = ''
    url = ''
    unrecognizedPath = ''
    recognizedPath = ''
    caffePath = ''
    splitedPath = ''
    suffix = ''
    outputSuffix = '.png'
    
    def __init__(self):
        pass
    
    def setName(self, name):
        self.name = name
        
    def setPath(self, path):
        self.path = path
        self.unrecognizedPath = os.path.join(self.path, 'unrecognized')
        self.recognizedPath = os.path.join(self.path, 'recognized')
        self.splitedPath = os.path.join(self.path, "splited");
        self.caffePath = os.path.join(self.path, "caffe");
    
    def setUrl(self, url):    
        self.url = url
    
    def setSuffix(self, suffix):
        self.suffix = suffix
        
    '''
    Downloads captcha pictures from server. 
    '''
    def download(self, num):
        time1 = time.time()
        
        if os.path.exists(self.unrecognizedPath):
            shutil.rmtree(self.unrecognizedPath)
        os.mkdir(self.unrecognizedPath)
        
        if not os.path.exists(self.recognizedPath):
            os.mkdir(self.recognizedPath)
        
        for i in xrange(num):
            idx = i + 1
            data = urllib2.urlopen(self.url).read()
            with open(os.path.join(self.unrecognizedPath, str(idx) + self.suffix), 'wb') as f:
                f.write(data)       
            
        time2 = time.time();
        costTime = int((time2 - time1) * 1000)
        print "Download", num, "pictures in", costTime, "ms."
    
    '''
    Split all recognized pictures into different directories by label. 
    '''
    def preprocess(self):
        time1 = time.time()
        
        if os.path.exists(self.splitedPath):
            shutil.rmtree(self.splitedPath)
        os.mkdir(self.splitedPath)
        fileList = os.listdir(self.recognizedPath)
        count = {}
        for f in fileList:
            imgPath = os.path.join(self.recognizedPath, f)
            img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
            imgs = self.splitImage(img)
            name = f.split('.')[0]          
            for i in xrange(len(name)):
                if count.has_key(name[i]):
                    count[name[i]] += 1
                else:
                    count[name[i]] = 1
                outputName = name[i] + "-" + str(count[name[i]]) + "-" + name + self.outputSuffix
                cv2.imwrite(os.path.join(self.splitedPath, outputName), imgs[i])
        
        time2 = time.time();
        costTime = int((time2 - time1) * 1000)
        print "Process", len(fileList), "pictures in", costTime, "ms."
    
        

    @abstractmethod
    def splitImage(self, img):
        pass
