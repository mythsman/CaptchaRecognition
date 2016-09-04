#coding=utf-8
from Captcha import Captcha
from Cnn import Cnn
import Util
class Csdn(Captcha):
    
    def __init__(self):
        super(Csdn,self).__init__("csdn")
        self.comment='CSDN论坛'
        self.url='https://passport.csdn.net/ajax/verifyhandler.ashx'
        self.suffix=".jpg"
        self.width=100
        self.height=100
        
    def splitImage(self, img):
        img = Util.resize(img, 500, 100)
        img = Util.otsu(img)
        img = Util.closing(img,3)
        imgT = img[0:1 ,0:1]
        img1 = img[0:100, 30:130]
        img2 = img[0:100, 130:230]
        img3 = img[0:100, 215:315]
        img4 = img[0:100, 300:400]
        img5 = img[0:100, 400:500]
        return [img1, img2, img3, img4,img5]
        
if  "__main__" == __name__:
    csdn = Csdn()
    #csdn.preprocess()
    cnn = Cnn(csdn)
    #cnn.genLmdb()
    #cnn.train(500)
    #cnn.predictDir("/home/myths/Desktop/CaptchaRecognition/data/7k7k/unrecognized")
    print cnn.predict("/home/myths/Desktop/CaptchaRecognition/Server/Server/static/data/csdn/recognized/maoqu.jpg")
