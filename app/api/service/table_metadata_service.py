from pyiceberg.catalog import load_catalog
from ..utils.SparkConnection import SparkConnection
import logging
from fastapi import HTTPException

class TableMetadata():
    def __init__(self):
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()
        # Need to ask for the catalog log from configuration file instead of hardcoding.
        self.catalog = load_catalog('local')

    def getTableSchema(self, db_name, table_name):
        return 200, "Ok"