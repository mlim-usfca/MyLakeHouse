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
        logging.info("In Get Table Schema service")
        if not db_name or not table_name:
            return 404, "Ill-formed request: 'table_name', and 'database_name' cannot be empty."
        try:
            table = self.spark.table(f'local.{db_name}.{table_name}')
            schema = table.schema
            if not schema:
                return 404, f"Cannot fetch the schema of table {db_name}.{table_name}"
            else:
               returnVal = []
               for field in schema.fields:
                   fieldVals = {}
                   jsonObj = field.jsonValue()
                   for key, val in jsonObj.items():
                       # metadata field is empty
                       if key is not "metadata":
                           fieldVals[key] = val
                   returnVal.append(fieldVals)
               return 200, returnVal
        except Exception as error:
            logging.info(f"Error in getTableSchema: {error}")
            return 500, error
