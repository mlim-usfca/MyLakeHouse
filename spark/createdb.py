# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, LongType, FloatType, DoubleType, StringType, IntegerType
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def create_toy_iceberg_database(spark):
    try:
        # Drop existing tables if they exist
        spark.sql("DROP TABLE IF EXISTS local.toyDb.taxis1")
        spark.sql("DROP TABLE IF EXISTS local.toyDb.taxis2")
        
        # Create Table 1: local.toyDb.taxis1
        schema1 = StructType([
            StructField("vendor_id", LongType(), True),
            StructField("trip_id", LongType(), True),
            StructField("trip_distance", FloatType(), True),
            StructField("fare_amount", DoubleType(), True),
            StructField("store_and_fwd_flag", StringType(), True)
        ])
        df = spark.createDataFrame([], schema1)
        df.writeTo("local.toyDb.taxis1").create()
        
        # Populate table 1 with data
        data1 = [
            (3, 1000371, 0.8, 5.32, "Y"),
            (3, 1000372, 4.5, 52.15, "N"),
            (4, 1000373, 2.9, 32.01, "N"),
            (4, 1000374, 10.4, 102.13, "Y")
        ]
        df = spark.createDataFrame(data1, schema1)
        df.writeTo("local.toyDb.taxis1").append()

        # Wait for 1 minute before creating the next table
        time.sleep(15)

        # Create Table 2: local.toyDb.taxis2
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
        
        # Populate table 2 with data
        data3 = [
            (1, 1000234, 1.8, 34.23, 1.34, 3, "N"),
            (2, 1000235, 4.58, 54.23, 2.34, 2, "N"),
            (2, 1000236, 10.58, 134.343, 5.34, 4, "N"),
            (3, 1000237, 5.37, 18.93, 0.34, 1, "N")
        ]
        df = spark.createDataFrame(data3, schema2)
        df.writeTo("local.toyDb.taxis2").append()

        # Rename column in table 2
        spark.sql("ALTER TABLE local.toyDb.taxis2 RENAME COLUMN num_of_passengers TO passengers_count;")
    except Exception as error:
        logging.error(f"Error creating toy database: {error}")
def create_nyc_iceberg_database(spark):
    try:
        # Drop existing tables if they exist
        spark.sql("DROP TABLE IF EXISTS local.nyc.taxis")
        df = spark.read.parquet("/home/iceberg/data/yellow_tripdata_2021-04.parquet")
        df.writeTo("local.nyc.taxis").create()

    except Exception as error:
        logging.error(f"Error creating nyc database: {error}")

if __name__ == "__main__":
    # Initialize Spark sessionToy Iceberg Database Creator
    spark = SparkSession.builder.appName("Toy Iceberg Database Creator").getOrCreate()

    # Call the function to create the database
    create_toy_iceberg_database(spark)
    create_nyc_iceberg_database(spark)
    spark.stop()
