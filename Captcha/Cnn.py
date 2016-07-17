'''
Created on Jul 16, 2016

@author: myths
'''
import caffe, lmdb, os, shutil, cv2, time
import numpy as np
from caffe.proto import caffe_pb2 
from caffe import layers as L, params as P
import pylab
from Zhengfang import Zhengfang
class Cnn:
    
    labelMap = {}
    cypherMap = {}
    
    def __init__(self, captcha):
        self.captcha = captcha
        if not os.path.exists(self.captcha.caffePath):
            os.mkdir(self.captcha.caffePath)
        self.trainLmdbPath = os.path.join(self.captcha.caffePath, 'train_lmdb')
        if not os.path.exists(self.trainLmdbPath):
            os.mkdir(self.trainLmdbPath)
        self.testLmdbPath = os.path.join(self.captcha.caffePath, 'test_lmdb')
        if not os.path.exists(self.testLmdbPath):
            os.mkdir(self.testLmdbPath)
        self.setMap()
    
    def setMap(self):
        lists = os.listdir(self.captcha.splitedPath)
        for item in lists:
            label = item[0]
            if not self.labelMap.has_key(label):
                self.labelMap[label] = len(self.labelMap)
        for key, value in self.labelMap.items():
            self.cypherMap[value] = key
        
        
    def encode(self, label):
        return self.labelMap.get(label)
    
    def decode(self, cypher):
        return self.cypherMap.get(cypher)

    def genLmdb(self, batch_size=200):
        time1 = time.time()
        
        if os.path.exists(self.testLmdbPath):
            shutil.rmtree(self.testLmdbPath)
        if os.path.exists(self.trainLmdbPath):
            shutil.rmtree(self.trainLmdbPath)
            
        trainEnv = lmdb.open(self.trainLmdbPath, map_size=int(1e12))
        testEnv = lmdb.open(self.testLmdbPath, map_size=int(1e12))
        trainTxn = trainEnv.begin(write=True)              
        testTxn = testEnv.begin(write=True)
        datum = caffe_pb2.Datum()
        cnt = 0
        test_cnt = 0
        train_cnt = 0
        lists = os.listdir(self.captcha.splitedPath)
        for picName in lists:
            picPath = os.path.join(self.captcha.splitedPath, picName)
            pic = cv2.imread(picPath, cv2.IMREAD_GRAYSCALE)
            data = np.array([pic]).astype('int')
            label = self.encode(picName[0])
            datum = caffe.io.array_to_datum(data, label)   
            cnt += 1
            if cnt % 7 == 0:
                keystr = '{:0>8d}'.format(test_cnt)
                test_cnt += 1
                testTxn.put(keystr, datum.SerializeToString())
                if test_cnt % batch_size == 0: 
                    testTxn.commit()
                    testTxn = testEnv.begin(write=True)  
                    
            else:
                keystr = '{:0>8d}'.format(train_cnt)
                train_cnt += 1
                trainTxn.put(keystr, datum.SerializeToString())
                if train_cnt % batch_size == 0:
                    trainTxn.commit()
                    trainTxn = trainEnv.begin(write=True) 
                    
        time2 = time.time()
        costTime = int(time2 - time1)
        print 'Write {} test pictures and {} train pictures in {} s.'.format(test_cnt, train_cnt, costTime)
        testEnv.close()
        trainEnv.close()
    
    
    def lenet(self, lmdb, batch_size):

        n = caffe.NetSpec()
        
        n.data, n.label = L.Data(batch_size=batch_size, backend=P.Data.LMDB, source=lmdb,
                                 transform_param=dict(scale=1. / 255), ntop=2)
        
        n.conv1 = L.Convolution(n.data, kernel_size=3, num_output=20, weight_filler=dict(type='xavier'))
        n.pool1 = L.Pooling(n.conv1, kernel_size=2, stride=2, pool=P.Pooling.MAX)
        n.conv2 = L.Convolution(n.pool1, kernel_size=5, num_output=50, weight_filler=dict(type='xavier'))
        n.pool2 = L.Pooling(n.conv2, kernel_size=2, stride=2, pool=P.Pooling.MAX)
        n.fc1 = L.InnerProduct(n.pool2, num_output=500, weight_filler=dict(type='xavier'))
        n.relu1 = L.ReLU(n.fc1, in_place=True)
        n.score = L.InnerProduct(n.relu1, num_output=len(self.labelMap), weight_filler=dict(type='xavier'))
        n.loss = L.SoftmaxWithLoss(n.score, n.label)
        
        return n.to_proto()
    

    def genConfig(self):
        self.model = os.path.join(self.captcha.caffePath, 'result.caffemodel')
        self.trainBatch = 200
        self.testBatch = 40
        self.trainProtoPath = os.path.join(self.captcha.caffePath, 'train.prototxt')
        self.testProtoPath = os.path.join(self.captcha.caffePath, 'test.prototxt')
        self.solverProtoPath = os.path.join(self.captcha.caffePath, 'solver.prototxt')
        if os.path.exists(self.trainProtoPath):
            os.remove(self.trainProtoPath)
        if os.path.exists(self.testProtoPath):
            os.remove(self.testProtoPath)
        if os.path.exists(self.solverProtoPath):
            os.remove(self.solverProtoPath)
            
        with open(self.trainProtoPath, 'w') as f:
            f.write(str(self.lenet(self.trainLmdbPath, self.trainBatch)))
            
        with open(self.testProtoPath, 'w') as f:
            f.write(str(self.lenet(self.testLmdbPath, self.testBatch)))

        with open(self.solverProtoPath, 'w+') as f:
            f.write('train_net: "' + self.trainProtoPath + '"\n')
            f.write('test_net:"' + self.testProtoPath + '"\n')
            f.write('test_iter: 100\n')
            f.write('test_interval: 500\n')
            f.write('base_lr: 0.001\n')
            f.write('momentum: 0\n')
            f.write('weight_decay: 0.0005\n')
            f.write('lr_policy: "inv"\n')
            f.write('gamma: 0.0001\n')
            f.write('power: 0.75\n')
            f.write('display: 100\n')
            f.write('max_iter: 10000\n')
            f.write('snapshot: 50000\n')
            f.write('snapshot_prefix:""')
        self.deployProtoPath = os.path.join(self.captcha.caffePath, 'deploy.prototxt')
        f = open(self.trainProtoPath)
        a = f.read()
        a = a.split('layer')
        res = '\nlayer {name: "data" type: "Input" top: "data" input_param { shape: { dim: 1 dim: 1 dim: ' + str(self.captcha.height) + ' dim: ' + str(self.captcha.width) + ' }} }\n'
        for i in a[2:-1]:
            res += 'layer' + i
        res += 'layer {  name: "prob"  type: "Softmax"  bottom: "score"  top: "prob"}'
        open(self.deployProtoPath, 'w+').write(res)
            
  
    
    def train(self, niter=1000):
        
        caffe.set_mode_cpu()
        solver = caffe.AdaGradSolver(self.solverProtoPath)
    
        for k, v in solver.net.blobs.items():
            print (k, v.data.shape)
    
        test_interval = 100
        solver.step(1)
        train_loss = np.zeros(niter)
        test_acc = np.zeros(int(np.ceil(niter / test_interval)))

        for it in range(niter):
            solver.step(1)

            train_loss[it] = solver.net.blobs['loss'].data

            solver.test_nets[0].forward()

            if it % test_interval == 0:
                print 'Iteration', it, 'testing...'
                correct = 0
                for test_it in xrange(100):
                    solver.test_nets[0].forward()
                    correct += sum(solver.test_nets[0].blobs['score'].data.argmax(1)
                                   == solver.test_nets[0].blobs['label'].data)
                test_acc[it // test_interval] = correct / (100.0 * self.testBatch)
                print 'Test Accuracy: {:.5f}'.format(correct / (100.0 * self.testBatch))
                
        _, ax1 = pylab.subplots()
        ax2 = ax1.twinx()
        ax1.plot(np.arange(niter), train_loss)
        ax2.plot(test_interval * np.arange(len(test_acc)), test_acc, 'r')
        ax1.set_xlabel('iteration')
        ax1.set_ylabel('train loss')
        ax2.set_ylabel('test accuracy')
        ax2.set_title('Test Accuracy: {:.5f}'.format(test_acc[-1]))
        
        solver.net.save(self.model)
        
    def predict(self, imgPath):
        time1 = time.time()
        
        img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE);
        imgs = self.captcha.splitImage(img)
        net = caffe.Net(self.deployProtoPath, self.model, caffe.TEST)
        res = ''
        for img in imgs:
            net.blobs['data'].data[...] = np.array([img])
            output = net.forward()
            output_prob = output['prob'][0]
            res += self.decode(output_prob.argmax())
        
        time2 = time.time()
        print 'Predicted in',(time2 - time1) * 1000, 'ms'
        return res
        
cnn = Cnn(Zhengfang())
# cnn.genLmdb()
cnn.genConfig()
# cnn.train(100)

print cnn.predict('/home/myths/Desktop/CaptchaRecognition/CaptchaRecognition/data/zhengfang/recognized/7cjm.png')


