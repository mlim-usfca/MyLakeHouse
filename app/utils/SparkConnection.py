import logging

from pyspark.sql import SparkSession

#To
class SparkConnection(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SparkConnection, cls).__new__(cls)
        return cls.instance

    def create_spark_session(self):
        self.spark = SparkSession.builder \
            .appName("IcebergApp") \
            .config("spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.3") \
            .config("spark.jars", "/app/spark/jars/bundle-2.17.257.jar,"
                                  "/app/spark/jars/url-connection-client-2.17.257.jar") \
            .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
            .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
            .config("spark.sql.defaultCatalog", "local") \
            .config("spark.sql.catalog.local.s3.endpoint", "http://minio:9000") \
            .config("spark.sql.catalog.local.io-impl", "org.apache.iceberg.aws.s3.S3FileIO") \
            .config("spark.sql.catalog.local.warehouse", "s3a://warehouse/") \
            .config("spark.sql.catalog.local.catalog-impl", "org.apache.iceberg.rest.RESTCatalog") \
            .config("spark.sql.catalog.local.uri", "http://rest:8181") \
            .config("spark.sql.catalogImplementation", "in-memory") \
            .getOrCreate()
        logging.info("Spark started.")

    def get_spark_session(self):
        return self.spark

    def stop_spark_session(self):
        self.spark.stop()
