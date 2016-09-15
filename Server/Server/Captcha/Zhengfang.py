#coding=utf-8
from Captcha import Captcha
from Cnn import Cnn
import Util,sys
class Zhengfang(Captcha):
    def __init__(self):
        super(Zhengfang,self).__init__('zhengfang')
        self.comment='正方教务系统'
        self.url='http://xk.suda.edu.cn/CheckCode.aspx'
        self.suffix=".gif"
        self.width=32
        self.height=32
        
    def splitImage(self, img):
        img = Util.resize(img, 100, 20)
        img = Util.otsu(img)
        #img = Util.closing(img, 5)
        img1 = img[0:20, 7:25]
        img2 = img[0:20, 23:41]
        img3 = img[0:20, 39:57]
        img4 = img[0:20, 55:73]
        img1=Util.resize(img1,32,32)
        img2=Util.resize(img2,32,32)
        img3=Util.resize(img3,32,32)
        img4=Util.resize(img4,32,32)
        return [img1, img2, img3, img4]
    
   
if  "__main__" == __name__:
    zhengfang = Zhengfang()
    zhengfang.preprocess()
    cnn = Cnn()
    cnn.load(zhengfang)
    cnn.genLmdb()
    cnn.train(2000)
    #cnn.predictDir()

