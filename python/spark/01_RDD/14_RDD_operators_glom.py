# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)

    # glom: 根据partition, 给数据加上嵌套
    # e.g. 假设有两个分区, RDD的的数据[1,2,3,4,5]
    # rdd.glom() [[1,2,3], [4,5]]
    print(rdd.glom().collect())
    print(rdd.glom().flatMap(lambda x: x).collect())
