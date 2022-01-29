# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 3, 2, 4, 7, 9, 6], 1)

    # foreach 等同于没有返回值的map
    # 由executor直接输出, 不会汇聚到driver再输出.
    result = rdd.foreach(lambda x: print(x * 10))

    print(rdd.collect()) # 对原数据没有影响.
