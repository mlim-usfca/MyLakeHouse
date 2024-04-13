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
            tableC = self.catalog.load_table(f'{db_name}.{table_name}')
            logging.info(tableC.location())

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


    def getDataFiles(self, db_name, table_name, limit, offset):
        logging.info("In Get Data files service")
        if not db_name or not table_name:
            return 404, "Ill-formed request: 'table_name', and 'database_name' cannot be empty."
        try:
            files = self.spark.sql(f"SELECT file_path, file_format, record_count, file_size_in_bytes,\
                                            null_value_counts, nan_value_counts, lower_bounds, upper_bounds \
                                            FROM local.{db_name}.{table_name}.all_data_files LIMIT {limit} OFFSET {offset}")

            if not files:
                return 404, f"Cannot get any data files for table {db_name}.{table_name}"

            for row in files.collect():
                return row
        except Exception as error:
            logging.info(f"Error in getDataFiles: {error}")
            return 500, error