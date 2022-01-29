# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 3, 2, 4, 7, 9, 6], 1)

    # 升序, 取前三个
    print(rdd.takeOrdered(3))

    # 升序, 取前三个(这里在排序时, 加上了-号, 所以相当于倒序, 不会影响原数据!)
    print(rdd.takeOrdered(3, lambda x: -x))
