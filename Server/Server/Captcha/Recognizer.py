from C7k7k import C7k7k
from Zhengfang import Zhengfang
from Cnn import Cnn

class Recognizer():
    captcha={}
    def __init__(self):
        self.captcha['7k7k']=C7k7k()
        self.captcha['zhengfang']=Zhengfang()

    def get(self,name):
        return self.captcha[name]
    
    def recognize(self,name,url):
        return Cnn(self.captcha[name]).predict(url)

