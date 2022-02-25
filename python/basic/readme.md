# 00_object
- type object class的关系
- object的四个属性
- build-in 内置类型概览

# 01_magic_function
- __repr__  , __str__
- __getitem__
- __len__
- __abs__, __add__

# 02_multi_thread
- GIL
- 实现多线程方式1: 通过Thread()实例化线程
- 实现多线程方式2: 构造Thread类(继承Thread), 然后在实例化线程
- 线程间通信: Queue
- 多线程同步: Lock / RLock / Condition

# 03_oop 面向对象
- duck_type : 什么类型,支持什么操作,就按class实现了什么magic function
- abc : 抽象基类(2个用途)
- isinstance()可以判断继承链
- 类变量(类似static) vs 对象变量
- 静态方法@staticmethod 类方法@classmethod 实例方法
- 类的私有变量 __privateName
- 自省机制: dir() __dict__

# third_lib
- argparse
- logging

# tools
- copy_file 实时监控一个文件, 并将内容追加到另外一个文件.