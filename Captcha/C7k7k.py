'''
Created on Jul 15, 2016

@author: myths
'''
from Captcha import Captcha
import Util
class C7k7k(Captcha):
    
    def __init__(self):
        self.setName("7k7k")
        self.setPath("../data/7k7k/")
        self.setUrl('http://zc.7k7k.com/authcode')
        self.setSuffix(".png")
        self.width=150
        self.height=90
        
    def splitImage(self, img):
        img = Util.resize(img, 500, 100)
        img = Util.otsu(img)
        img = Util.closing(img, 3)
        img1 = img[0:90, 25:175]
        img2 = img[0:90, 125:275]
        img3 = img[0:90, 225:375]
        img4 = img[0:90, 325:475]
        return [img1, img2, img3, img4]
        
if  "__main__" == __name__:
    c7k7k = C7k7k()
    #c7k7k.preprocess()
    c7k7k.download(1000)
