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
        self.width=90
        self.height=80
        
    def splitImage(self, img):
        img = Util.resize(img, 500, 100)
        img = Util.otsu(img)
        img = Util.closing(img, 5)
        img1 = img[0:80, 35:125]
        img2 = img[0:80, 115:205]
        img3 = img[0:80, 195:285]
        img4 = img[0:80, 275:365]
        return [img1, img2, img3, img4]
    
   
if  "__main__" == __name__:
    zhengfang = Zhengfang()
    #zhengfang.preprocess()
    cnn = Cnn(zhengfang)
    #cnn.genLmdb()
    #cnn.train(1000)
    print cnn.predict("../static/data/zhengfang/recognized/aqh1.png")

