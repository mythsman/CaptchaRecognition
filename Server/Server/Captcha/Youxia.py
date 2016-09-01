#coding=utf-8
from Captcha import Captcha
from Cnn import Cnn
import Util
class Youxia(Captcha):
    
    def __init__(self):
        super(Youxia,self).__init__("youxia")
        self.comment='游侠网'
        self.url='http://passport.ali213.net/seccode.php'
        self.suffix=".png"
        self.width=150
        self.height=90
        
    def splitImage(self, img):
        img = Util.resize(img, 500, 100)
        img = Util.bersen(img,33)
        img = Util.closing(img, 7)
        imgT = img[0:1 ,0:1]
        img1 = img[0:100, 0:150]
        img2 = img[0:100, 110:260]
        img3 = img[0:100, 240:390]
        img4 = img[0:100, 350:500]
        return [img1, img2, img3, img4]
        
if  "__main__" == __name__:
    youxia = Youxia()
    #youxia.preprocess()
    cnn = Cnn(youxia)
    cnn.genLmdb()
    cnn.train(100)
    #cnn.predictDir("/home/myths/Desktop/CaptchaRecognition/data/7k7k/unrecognized")
