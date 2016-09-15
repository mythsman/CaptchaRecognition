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
        self.width=32
        self.height=32
        
    def splitImage(self, img):
        img = Util.resize(img, 100, 20)
        img = Util.bersen(img,7)
        imgT = img[0:1 ,0:1]
        img1 = img[0:20, 0:30]
        img2 = img[0:20, 22:52]
        img3 = img[0:20, 48:78]
        img4 = img[0:20, 70:100]
        img1=Util.resize(img1,32,32)
        img2=Util.resize(img2,32,32)
        img3=Util.resize(img3,32,32)
        img4=Util.resize(img4,32,32)
        return [img1, img2, img3, img4]
        
if  "__main__" == __name__:
    youxia = Youxia()
    youxia.preprocess()
    cnn = Cnn()
    cnn.load(youxia)
    cnn.genLmdb()
    cnn.train(4000)
    #cnn.predictDir()
