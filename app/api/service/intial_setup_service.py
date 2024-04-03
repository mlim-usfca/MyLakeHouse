from ..utils.SparkConnection import SparkConnection
import os
from ..schema.create_iceberg_table_request_schema import CreateIcebergTableRequest
import logging
from pyspark.sql.types import StructType, StructField,StringType, DoubleType, LongType, FloatType, IntegerType
import time

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

    """
       This is a test function to create a toy database containing two tables:
            toyDb.taxis1
            toyDb.taxis2
       Inserts records in it to create snapshot history and also alters a column name in taxis2 tables     
    """
    def create_toy_iceberg_database(self):
        # Ensure Spark session is available
        if self.spark is None:
            return 500, "Spark session not initialized."

        spark = self.spark
        try:
            spark.sql("DROP TABLE IF EXISTS local.toyDb.taxis1")
            spark.sql("DROP TABLE IF EXISTS local.toyDb.taxis2")
            #Create Table 1 : local.toyDb.taxis1
            schema1 = StructType([
                            StructField("vendor_id", LongType(), True),
                            StructField("trip_id", LongType(), True),
                            StructField("trip_distance", FloatType(), True),
                            StructField("fare_amount", DoubleType(), True),
                            StructField("store_and_fwd_flag", StringType(), True)
                        ])
            df = spark.createDataFrame([], schema1)
            df.writeTo("local.toyDb.taxis1").create()
            schema_table1 = spark.table("local.toyDb.taxis1").schema
            data1 = [
                (3, 1000371, 0.8, 5.32, "Y"),
                (3, 1000372, 4.5, 52.15, "N"),
                (4, 1000373, 2.9, 32.01, "N"),
                (4, 1000374, 10.4, 102.13, "Y")
            ]
            df = spark.createDataFrame(data1, schema_table1)
            df.writeTo("local.toyDb.taxis1").append()
            data2 = [
                (3, 1000375, 1.8, 25.32, "N"),
                (3, 1000376, 4.5, 52.15, "N"),
                (4, 1000377, 1.9, 19.01, "N"),
                (4, 1000378, 18.4, 142.13, "Y")
            ]
            df = spark.createDataFrame(data2, schema_table1)
            df.writeTo("local.toyDb.taxis1").append()
            #Wait for 1 minute to create next table
            time.sleep(60)
            # Create Table 2 : local.toyDb.taxis2
            schema2 = StructType([
                StructField("vendor_id", LongType(), True),
                StructField("trip_id", LongType(), True),
                StructField("trip_distance", FloatType(), True),
                StructField("fare_amount", DoubleType(), True),
                StructField("tolls_amount", DoubleType(), True),
                StructField("num_of_passengers", IntegerType(), True),
                StructField("store_and_fwd_flag", StringType(), True)
            ])
            df = spark.createDataFrame([], schema2)
            df.writeTo("local.toyDb.taxis2").create()
            schema_table2 = spark.table("local.toyDb.taxis2").schema
            data3 = [
                (1, 1000234, 1.8, 34.23, 1.34, 3, "N"),
                (2, 1000235, 4.58, 54.23, 2.34, 2, "N"),
                (2, 1000236, 10.58, 134.343, 5.34, 4, "N"),
                (3, 1000237, 5.37, 18.93, 0.34, 1, "N"),
            ]
            df = spark.createDataFrame(data3, schema_table2)
            df.writeTo("local.toyDb.taxis2").append()
            data4 = [
                (1, 1000238, 1.8, 34.23, 1.34, 3, "N"),
                (2, 1000239, 4.58, 58.23, 4.34, 2, "Y"),
                (2, 1000240, 11.58, 134.343, 5.34, 4, "N"),
                (3, 1000241, 5.37, 19.93, 5.34, 1, "N"),
            ]
            df = spark.createDataFrame(data4, schema_table2)
            df.writeTo("local.toyDb.taxis2").append()
            spark.sql("ALTER TABLE local.toyDb.taxis2 RENAME COLUMN num_of_passengers TO passengers_count;")
            return 200, "toyDb created successfully"
        except Exception as error:
            logging.info(f"Error creating toy database Error: {error}")
            return 500, error