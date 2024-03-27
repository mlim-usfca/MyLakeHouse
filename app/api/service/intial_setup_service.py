from ..utils.SparkConnection import SparkConnection
import os
from ..schema.create_iceberg_table_request_schema import CreateIcebergTableRequest
import logging


class IntialSetupService():
    def __init__(self):
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()

    def create_iceberg_table(self, request: CreateIcebergTableRequest):
        try:
            data_path = request.data_path
            table_name = request.table_name
            database_name = request.database_name

            if not data_path or not table_name or not database_name:
                return 404, "Ill-formed request: 'data_path', 'table_name', and 'database_name' cannot be empty."

            # Ensure Spark session is available
            if self.spark is None:
                return 500,"Spark session not initialized."

            spark = self.spark

            # Validate data path existence (optional)
            if not os.path.exists(data_path):
                return 404, "data_path doesn't exist"

            # Create the Iceberg table in append mode (if it doesn't exist)
            spark.sql(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            spark.sql(f"DROP TABLE IF EXISTS {database_name}.{table_name}")
            spark.sql(f"USE local.{database_name}")
            # Load data from the parquet file
            df = spark.read.format("parquet").load(data_path)

            # Append data to the Iceberg table
            df.write.format("iceberg").saveAsTable(f"{database_name}.{table_name}")

            return 200, f"Table '{database_name}.{table_name}' created/updated successfully."
        except Exception as error:
            logging.error("Error: InitialSetupService: create_iceberg_table:", error)
            return 500, error;