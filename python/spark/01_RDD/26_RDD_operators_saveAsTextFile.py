# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 3, 2, 4, 7, 9, 6], 3)

    # rdd有几个分区, 就会写几个文件part-00000 .. part-0000N
    # 原因是因为, 这些文件有executor直接写. 不是通过driver写.
    # warn: 目录必须不存在!
    rdd.saveAsTextFile("../data/output/out1")
