import json
import logging
from pyspark.sql import SparkSession
from pyspark import SparkConf


class SparkConnection(object):

    def __init__(self):
        with open("./config.json") as configFile:
            self.config = json.load(configFile)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SparkConnection, cls).__new__(cls)
        return cls.instance

    def create_spark_session(self):
        spark_builder = SparkSession.builder.appName("IcebergApp")
        conf = SparkConf().setAppName("IcebergApp")
        # Build the SparkSession with configurations
        for key, value in self.config["sparkConfig"].items():
            #logging.info(f'{key}     {value}')
            #spark_builder = spark_builder.config(key, value)
            conf.set(key, value)
        # Now create the SparkSession
        self.spark = SparkSession.builder.config(conf=conf).getOrCreate()
        logging.info("Spark started.")

    def get_spark_session(self):
        return self.spark

    def stop_spark_session(self):
        self.spark.stop

    def get_catalog(self):
        return self.config["catalogName"]