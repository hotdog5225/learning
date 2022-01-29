# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 3, 2, 4, 7, 9, 6], 3)

    # mapPartitions每次传给func的不是一个个的值, 而是一整个partition的数据
    def process(iter):
        result = list()
        for it in iter:
            result.append(it * 10)

        return result

    # 每次将一个partition的数据, 传给process
    print(rdd.mapPartitions(process).collect())