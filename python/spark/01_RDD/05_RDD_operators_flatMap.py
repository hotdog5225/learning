# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize(["hadoop spark hadoop", "spark hadoop hadoop", "hadoop flink spark"])

    # flatMap功能: 先对rdd进行map操作, 然后进行"解除嵌套"操作
    # 嵌套的list
    lst = [[1,2,3], [4,5,6]]
    # 解除嵌套后:
    lst = [1,2,3,4,5,6]

    print(rdd.map(lambda line: line.split(" ")).collect()) # [['hadoop', 'spark', 'hadoop'], ['spark', 'hadoop', 'hadoop'], ['hadoop', 'flink', 'spark']]

    # 得到所有的单词, 组成RDD, flatMap的传入参数 和map一致, 就是给map解除嵌套用的
    rdd2 = rdd.flatMap(lambda line: line.split(" ")) #['hadoop', 'spark', 'hadoop', 'spark', 'hadoop', 'hadoop', 'hadoop', 'flink', 'spark']

    print(rdd2.collect())
