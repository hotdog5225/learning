#!/usr/bin/env python
# coding: utf-8

'''
自己定义权重参数W, b
自己定义Model (一个隐藏层, 一个输出层)
    全链接层 WX+b
'''

import torch

# 下载数据
from pathlib import Path
import requests
DATA_PATH = Path("data")
PATH = DATA_PATH / "mnist"
PATH.mkdir(parents=True,exist_ok=True)
URL = "http://deeplearning.net/data/mnist/"
FILENAME = "mnist.pkl.gz"

if not (PATH/FILENAME).exists():
    content = requests.get(URL + FILENAME).content
    (PATH / FILENAME).open("wb").write(content)

# 加载数据
import pickle
import gzip

with gzip.open((PATH / FILENAME).as_posix(), "rb")as f:
    ((x_train, y_train),(x_valid, y_valid),_) = pickle.load(f, encoding="latin-1") # pickle格式的包, 得到numpy.ndarray

# 展示数据
from matplotlib import pyplot
pyplot.imshow(x_train[0].reshape((28, 28)), cmap="gray")
# print(x_train.shape) # (50000, 784)

# 注意数据需转换成tensor才能参与后续建模训练
import torch
# ndarray -> tensor转换
x_train,y_train,x_valid,y_valid, y_valid = map(
    torch.tensor, (x_train,y_train, x_valid,y_valid, y_valid)
)
n,c=x_train.shape
x_train, x_train.shape, y_train.min(), y_train.max

# torch.nn.functional & nn.Module
    # torch.nn.functional中有很多功能,后续会常用的。那什么时候使用nn.Module,什么时候使用nn.functional呢?
    # 一般情况下,如果模型有可学习的参数,最好用nn.Module,其他情况nn.functional相对更简单一些
import torch.nn.functional as F

loss_func=F.cross_entropy # loss_func(model(xb), yb)
def model(xb):
    return xb.mm(weights) + bias

bs = 64 # bach_size
xb = x_train[:bs] # mini-batch
yb = y_train[:bs]
weights = torch.randn([784, 10], dtype=torch.float, requires_grad=True)
bias = torch.randn([10], requires_grad=True)


# 创建一个model来更简化代码
    # 必须继承nn.Module且在其构造函数中需调用nn.Module的构造函数
    # 无需写反向传播函数,nn.Module能够利用autograd自动实现反向传幸播
    # Module中的可学习参数可以通过named_parameters()或者parameters()返回迭代器
from torch import nn # 神经网络
class Mnist_NN(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden1 = nn.Linear(784, 128)
        self.hidden2 = nn.Linear(128,256)
        self.out = nn.Linear(256,10)
        self.dropout=nn.Dropout(0.5)

    def forward(self, x):
        x = F.relu(self.hiddenl(x))
        x=self.dropout(x)
        x = F.relu(self.hidden2(x))
        x = self.dropout(x)
        x = self.out(x)
        return x





