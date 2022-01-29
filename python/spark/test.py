# SparkSession对象的导包, 对象是来自于 pyspark.sql包中
from pyspark.sql import SparkSession

if __name__ == "__main__":
    sc = SparkSession.builder.enableHiveSupport().getOrCreate().sparkContext

    sc.setLogLevel("DEBUG")
    log4jLogger = sc._jvm.org.apache.log4j
    LOGGER = log4jLogger.LogManager.getLogger("test")

    LOGGER.info("this is spark log")
    print(type(LOGGER))

    rdd_1 = sc.parallelize([1,2,3,4], 2)
