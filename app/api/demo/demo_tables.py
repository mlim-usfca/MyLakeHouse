from ..utils.SparkConnection import SparkConnection
import logging
from pyspark.sql.types import StructType, StructField,StringType, DoubleType, LongType

class DemoIcebergTables():
    def __init__(self):
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()
        self.catalog = spark_conn_obj.get_catalog()

    def create_car_sales_table(self):
        try:
            # Drop existing tables if they exist
            self.spark.sql(f"DROP TABLE IF EXISTS {self.catalog}.carsales.may")
            self.spark.sql(f"DROP TABLE IF EXISTS {self.catalog}.carsales.june")
            self.spark.sql(f"DROP TABLE IF EXISTS {self.catalog}.carsales.july")

            # Create Table 1: local.carsales.may
            schema1 = StructType([
                StructField("sale_id", LongType(), True),
                StructField("car_model", StringType(), True),
                StructField("sale_date", StringType(), True),
                StructField("sale_price", DoubleType(), True),
                StructField("customer_id", LongType(), True)
            ])

            # Create an empty DataFrame with the defined schema
            df = self.spark.createDataFrame([], schema1)
            df.writeTo(f"{self.catalog}.carsales.may").create()

            # Define the schema of the table (for consistency)
            schema_table1 = self.spark.table(f"{self.catalog}.carsales.may").schema

            # Sample data to insert into the table
            data1 = [
                (101, "Toyota Corolla", "2022-05-15", 19200.00, 5001),
                (102, "Honda Civic", "2022-05-18", 18500.00, 5002),
                (103, "Ford Focus", "2022-05-21", 17800.00, 5003),
                (104, "Chevrolet Impala", "2022-05-25", 21000.00, 5004)
            ]

            # Create DataFrame from data1 using the schema of the table
            df = self.spark.createDataFrame(data1, schema_table1)
            df.writeTo(f"{self.catalog}.carsales.may").append()

            # Additional records for May car sales
            additional_data_may = [
                (105, "Nissan Altima", "2022-05-28", 22000.00, 5005),
                (106, "Hyundai Sonata", "2022-05-30", 19500.00, 5006)
            ]

            # Create DataFrame for additional May data and append it
            df_additional_may = self.spark.createDataFrame(additional_data_may, schema_table1)
            df_additional_may.writeTo(f"{self.catalog}.carsales.may").append()

            schema_june = StructType([
                StructField("sale_id", LongType(), True),
                StructField("car_model", StringType(), True),
                StructField("sale_price", DoubleType(), True),
                StructField("customer_name", StringType(), True)  # Different column for customer details
            ])

            # Create Table 2: local.carsales.june
            df_june = self.spark.createDataFrame([], schema_june)
            df_june.writeTo(f"{self.catalog}.carsales.june").create()

            data_june = [
                (201, "Ford Explorer", 32000.00, "John Doe"),
                (202, "Chevrolet Tahoe", 47000.00, "Jane Smith")
            ]

            df_june = self.spark.createDataFrame(data_june, schema_june)
            df_june.writeTo(f"{self.catalog}.carsales.june").append()

            # Create Table for July: local.carsales.july
            schema_july = StructType([
                StructField("sale_id", LongType(), True),
                StructField("car_model", StringType(), True),
                StructField("sale_price", DoubleType(), True),
                StructField("sale_date", StringType(), True),
                StructField("payment_method", StringType(), True)  # Additional column for payment method
            ])

            df_july = self.spark.createDataFrame([], schema_july)
            df_july.writeTo(f"{self.catalog}.carsales.july").create()

            data_july = [
                (301, "Toyota Camry", 23000.00, "2022-07-05", "Credit Card"),
                (302, "Honda Accord", 24000.00, "2022-07-15", "Cash"),
                (310, "Lexus ES350", 49000.00, "2022-07-16", "Credit Card"),
                (311, "Toyota Corolla", 32500.00, "2022-07-16", "Debit Card")
            ]

            df_july = self.spark.createDataFrame(data_july, schema_july)
            df_july.writeTo(f"{self.catalog}.carsales.july").append()
            return 200, "Created successfully"
        except Exception as error:
            logging.info(error)
            return 500, "Internal Server Error"