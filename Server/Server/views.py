#coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from Captcha.C7k7k import C7k7k
from Captcha.Recognizer import Recognizer
import json,time,hashlib,os

def index(request):
    if request.method=='POST':
        dicts={}
        mode=request.POST['mode']
        dicts['mode']=mode
        if mode=='0':
            pic=request.FILES['file']
            token=request.POST['csrfmiddlewaretoken']
            m=hashlib.md5()
            m.update(token+str(time.time()))
            fileName=m.hexdigest()
            f = open('Server/static/upload/'+fileName,'w')
            f.write(pic.read())
            f.close()
            dicts['src']='static/upload/'+fileName
        elif mode=='1':
            recognizer=Recognizer()
            pic=request.FILES['file']
            token=request.POST['csrfmiddlewaretoken']
            m=hashlib.md5()
            m.update(token+str(time.time()))
            fileName=m.hexdigest()
            f = open('Server/static/upload/'+fileName,'w')
            f.write(pic.read())
            f.close()
            picType=request.POST['type']
            res=recognizer.recognize(picType,'Server/static/upload/'+fileName)
            dicts['res']=res[0]
            dicts['time']=str(res[1]).split('.')[0]
        elif mode=='2':
            name=request.POST['name']
            path='static/data/'+name+'/recognized/'
            fileList=os.listdir('Server/'+path)
            dicts['src1']=os.path.join(path,fileList[0])
            dicts['src2']=os.path.join(path,fileList[1])
            dicts['url']=Recognizer().get(name).url
            
        return HttpResponse(json.dumps(dicts),content_type='application/json')
    else:
        lists={}
        recognizer=Recognizer()
        for name in recognizer.names:
            lists[name]=recognizer.get(name).comment
        return render(request, 'index.html',{'lists':lists})
