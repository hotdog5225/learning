# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)

    # fold功能和reduce一样,都是聚合, 只不过fold会带有一个初始值.
    # 这个初始值会作用在: 1. 分区内聚合 2. 分区间聚合
    print(rdd.fold(10, lambda a, b: a + b))
