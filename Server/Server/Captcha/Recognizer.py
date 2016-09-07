#coding=utf-8
from C7k7k import C7k7k
from Zhengfang import Zhengfang
from Csdn import Csdn
from C9you import C9you
from Cnn import Cnn

class Recognizer():
    names=[]
    def __init__(self):
        self.names.append('7k7k')
        self.names.append('zhengfang')
        self.names.append('csdn')
        self.names.append('9you')

    def get(self,name):
        if name=='7k7k':
            return C7k7k()
        elif name=='zhengfang':
            return Zhengfang()
        elif name=='csdn':
            return Csdn()
        elif name=='9you':
            return C9you()
        
    def recognize(self,name,url):
        cnn = Cnn()
        cnn.load(self.get(name))
        res=cnn.predict(url)
        return res

if __name__=='__main__':
    cnn=Cnn()
    cnn.load(Zhengfang())
    print cnn.predict('/home/myths/Desktop/CaptchaRecognition/Server/Server/static/data/zhengfang/recognized/bcqu.png')
    cnn.load(C7k7k()) 
    print cnn.predict('/home/myths/Desktop/CaptchaRecognition/Server/Server/static/data/7k7k/unrecognized/c8d6.png')
