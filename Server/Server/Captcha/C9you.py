#coding=utf-8
from Captcha import Captcha
import Util
from Cnn import Cnn
class C9you(Captcha):
    
    def __init__(self):
        super(C9you,self).__init__("9you")
        self.comment='久游网'
        self.url='https://login.passport.9you.com/identifyingCode.jsp'
        self.suffix=".jpg"
        self.width=26
        self.height=20
        
    def splitImage(self, img):
        img = Util.resize(img, 100, 20)
        img = Util.otsu(img)
        imgT=img[0:1,0:1]
        img1 = img[0:20, 7:33]
        img2 = img[0:20, 27:53]
        img3 = img[0:20, 47:73]
        img4 = img[0:20, 67:93]
        return [img1,img2, img3, img4]
        
if  "__main__" == __name__:
    c9you = C9you()
    c9you.preprocess()
    #cnn = Cnn()
    #cnn.load(c9you)
    #cnn.genLmdb()
    #cnn.train(4000)
    #cnn.predictDir()

