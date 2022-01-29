# coding:utf8
import time

from pyspark import SparkConf, SparkContext
from pyspark.storagelevel import StorageLevel

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 2)

    # Spark提供的累加器变量, 参数是初始值
    acmlt = sc.accumulator(0)

    def map_func(data):
        global acmlt
        acmlt += 1
        # print(acmlt)

    rdd2 = rdd.map(map_func)
    # 缓存rdd2, 因为rdd2.collect()后rdd2作为中间数据就消失了.
    rdd2.cache()
    rdd2.collect()

    # 如果rdd2消失, 则会进行溯源, 即重新构造rdd2(accumulator会再次+10)
    rdd3 = rdd2.map(lambda x:x)
    rdd3.collect()
    print(acmlt)


























