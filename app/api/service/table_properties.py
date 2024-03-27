from pyiceberg.catalog import load_catalog
from ..utils.SparkConnection import SparkConnection


class TableProperties():
    def __init__(self):
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()


    def getCatalog(self):
        catalog = load_catalog('local')
        return 200, f"Catalog: {catalog}"

