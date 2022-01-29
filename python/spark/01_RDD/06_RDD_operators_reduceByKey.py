# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([('a', 1), ('a', 1), ('b', 1), ('b', 1), ('a', 1)])

    # reduceByKey 对相同key进行分组, 然后对各个分组进行组内的value聚合(下例聚合操作为相加)
    print(rdd.reduceByKey(lambda a, b: a + b).collect())

