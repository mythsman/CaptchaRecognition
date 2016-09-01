'''
Created on Jul 15, 2016

@author: myths
'''
from abc import ABCMeta, abstractmethod
import os, time, shutil, urllib2, cv2, Image, numpy as np


class Captcha(object):
    __metaclass__ = ABCMeta
    width = 0               #The width of the raw picture
    height = 0              #The height of the raw picture
    path = ''               #The path owned by data
    name = ''               #The captcha name
    comment=''              #The comment 
    url = ''                #The url of the captcha
    unrecognizedPath = ''   #The path of unrecognized pictures
    recognizedPath = ''     #The path of recognized pictures
    caffePath = ''          #The path of files used by caffe
    splitedPath = ''        #The path of splited pictures
    suffix = ''             #The raw suffix of the pictures
    outputSuffix = '.png'   #The output suffix of the pictures
    
    def __init__(self,name):
        self.name=name
        self.path=os.path.join('static/data',self.name)
        if os.path.exists(os.path.join('..',self.path)):
            self.path=os.path.join('..',self.path)
        else:
            self.path=os.path.join('Server',self.path)
        self.unrecognizedPath = os.path.join(self.path, 'unrecognized')
        self.recognizedPath = os.path.join(self.path, 'recognized')
        self.splitedPath = os.path.join(self.path, "splited");
        self.caffePath = os.path.join(self.path, "caffe");
    
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
            img = np.array(Image.open(imgPath).convert('L'))
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
