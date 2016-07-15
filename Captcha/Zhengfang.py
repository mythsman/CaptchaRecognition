'''
Created on Jul 15, 2016

@author: myths
'''
from Captcha import Captcha
class Zhengfang(Captcha):
    
    def __init__(self):
        self.name = "Zhengfang"
        self.path = "../data/zhengfang/"
        self.url = 'http://xk.suda.edu.cn/CheckCode.aspx'
        self.suffix = ".gif"
        
    def _splitImage(self, img):
        pass
    
    

zhengfang = Zhengfang()
zhengfang.download(100)
