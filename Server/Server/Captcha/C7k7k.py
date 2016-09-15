#coding=utf-8
from Captcha import Captcha
from Cnn import Cnn
import Util
class C7k7k(Captcha):
    
    def __init__(self):
        super(C7k7k,self).__init__('7k7k')
        self.comment='7k7k'
        self.url='http://zc.7k7k.com/authcode'
        self.suffix=".png"
        self.width=32
        self.height=32
        
    def splitImage(self, img):
        img = Util.resize(img, 100, 20)
        img = Util.bersen(img,7)
        img = Util.closing(img, 1)
        img1 = img[0:20, 5:35]
        img2 = img[0:20, 25:55]
        img3 = img[0:20, 45:75]
        img4 = img[0:20, 65:95]
        img1=Util.resize(img1,32,32)
        img2=Util.resize(img2,32,32)
        img3=Util.resize(img3,32,32)
        img4=Util.resize(img4,32,32)
    
        return [img1, img2, img3, img4]
        
if  "__main__" == __name__:
    c7k7k = C7k7k()
    c7k7k.preprocess()
    cnn = Cnn()
    cnn.load(c7k7k)
    cnn.genLmdb()
    cnn.train(4000)
    #cnn.predictDir()
