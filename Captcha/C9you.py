'''
Created on Jul 15, 2016

@author: myths
'''
from Captcha import Captcha
import Util
class C9you(Captcha):
    
    def __init__(self):
        super(C9you,self).__init__("9you","../data/9you/")
        self.setUrl('https://login.passport.9you.com/identifyingCode.jsp')
        self.setSuffix(".jpg")
        self.width=110
        self.height=100
        
    def splitImage(self, img):
        img = Util.resize(img, 500, 100)
        img = Util.otsu(img)
        img = Util.closing(img, 4)
        imgT=img[0:1,0:1]
        img1 = img[0:100, 35:145]
        img2 = img[0:100, 135:245]
        img3 = img[0:100, 235:345]
        img4 = img[0:100, 335:445]
        return [img1,img2, img3, img4]
        
if  "__main__" == __name__:
    c9you = C9you()
    c9you.preprocess()
    cnn = Cnn(c9you)
    #cnn.genLmdb()
    #cnn.train(200)
    #cnn.predictDir("/home/myths/Desktop/CaptchaRecognition/data/7k7k/unrecognized")

