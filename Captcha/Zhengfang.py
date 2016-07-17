'''
Created on Jul 15, 2016

@author: myths
'''
from Captcha import Captcha
import Util
class Zhengfang(Captcha):
    width = 90
    height = 80
    def __init__(self):
        self.setName("Zhengfang")
        self.setPath("../data/zhengfang/")
        self.setUrl('http://xk.suda.edu.cn/CheckCode.aspx')
        self.setSuffix(".gif")
        
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
    zhengfang.preprocess()
