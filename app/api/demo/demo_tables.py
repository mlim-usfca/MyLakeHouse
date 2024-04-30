from ..utils.SparkConnection import SparkConnection
import logging
from pyspark.sql.types import StructType, StructField,StringType, DoubleType, LongType, IntegerType

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

    def create_wildlife_database(self):
        try:
            animal_types = ['reptiles', 'birds', 'mammals', 'amphibians']
            for animal_type in animal_types:
                # Drop existing table if it exists
                self.spark.sql(f"DROP TABLE IF EXISTS {self.catalog}.wildlife.{animal_type}")

            # Define schema
            schema = StructType([
                StructField("id", IntegerType(), True),
                StructField("common_name", StringType(), True),
                StructField("scientific_name", StringType(), True),
                StructField("conservation_status", StringType(), True),
                StructField("habitat_type", StringType(), True),
                StructField("geographic_distribution", StringType(), True)
            ])

            for animal_type in animal_types:
                # Create an empty DataFrame with the defined schema
                df = self.spark.createDataFrame([], schema)
                df.writeTo(f"{self.catalog}.wildlife.{animal_type}").create()

            # Sample data for each animal type with additional fields
            data = {
                'reptiles': [
                    (1, "Eastern Box Turtle", "Terrapene carolina", "Not Threatened", "Woodlands", "Eastern USA"),
                    (2, "American Alligator", "Alligator mississippiensis", "Least Concern", "Freshwater", "Southeast USA"),
                    (3, "Gila Monster", "Heloderma suspectum", "Near Threatened", "Desert", "Southwestern USA")
                ],
                'birds': [
                    (1, "Bald Eagle", "Haliaeetus leucocephalus", "Least Concern", "Lakes and Rivers", "North America"),
                    (2, "Peregrine Falcon", "Falco peregrinus", "Least Concern", "Urban & Cliffs", "Worldwide"),
                    (3, "California Condor", "Gymnogyps californianus", "Critically Endangered", "Rocky Shrubs",
                             "California and Baja California")
                ],
                'mammals': [
                    (1, "Gray Wolf", "Canis lupus", "Endangered", "Forests and Plains", "North America and Eurasia"),
                    (2, "American Bison", "Bison bison", "Near Threatened", "Plains", "North America"),
                    (3, "Florida Panther", "Puma concolor coryi", "Endangered", "Swamps and Forests", "Florida")
                ],
                'amphibians': [
                    (1, "American Bullfrog", "Lithobates catesbeianus", "Least Concern", "Lakes and Ponds", "North America"),
                    (2, "Axolotl", "Ambystoma mexicanum", "Critically Endangered", "Lakes", "Mexico"),
                    (3, "Red-eyed Tree Frog", "Agalychnis callidryas", "Least Concern", "Rainforests", "Central America")
                ]
            }
            # For each animal type, create DataFrame from data using the schema of the table and append it
            for animal_type, entries in data.items():
                df = self.spark.createDataFrame(entries, schema)
                df.writeTo(f"{self.catalog}.wildlife.{animal_type}").append()
            return 200, "Created wildlife database successfully."
        except Exception as error:
            logging.info(error)
            return 500, "Internal Server Error"

    def create_demo_databases(self):
        try:
            self.create_wildlife_database()
            self.create_car_sales_table()
            return 200, "Created demo databases successfully!"
        except Exception as error:
            logging.info(error)
            return 500, "Internal Server Error"

    def snapshots_branching_and_tagging(self):
        try:
            # Drop existing table if it exists
            self.spark.sql("DROP TABLE IF EXISTS local.demo.my_iceberg_table")

            # Create a new Iceberg table
            self.spark.sql("""
                        CREATE TABLE local.demo.my_iceberg_table (
                            id INT,
                            name STRING,
                            score INT
                        ) USING iceberg
                    """)

            # Insert data into the table to create 30 snapshots
            for i in range(30):
                # Simulate data insertion
                self.spark.sql(f"INSERT INTO local.demo.my_iceberg_table VALUES ({i}, 'Student_{i}', {100 - i})")

            # Retrieve the current table
            table = self.spark.table("local.demo.my_iceberg_table")

            # Get the snapshot ID after 30 inserts
            current_snapshot_id = table.currentSnapshot().snapshotId()
            logging.info(f"Current Snapshot ID after 30 inserts: {current_snapshot_id}")

            # Tag the top 5 students with the highest scores
            top_students = self.spark.sql("""
                        SELECT id, name FROM local.demo.my_iceberg_table
                        ORDER BY score DESC
                        LIMIT 5
                    """)

            for student in top_students.collect():
                tag_name = f"top_score_{student.name}"
                table.updateProperties().set(tag_name, str(current_snapshot_id)).commit()

            # Enable Write-Audit-Publish (WAP) before creating a branch
            self.spark.sql("""
                        ALTER TABLE local.demo.my_iceberg_table SET TBLPROPERTIES (
                            'write.wap.enabled'='true'
                        )
                    """)

            # Create an audit branch from the third snapshot
            third_snapshot_id = table.history()[2].snapshotId()  # This is conceptual
            self.spark.sql("SET spark.wap.branch = 'audit-branch'")
            self.spark.sql(
                f"CALL spark_catalog.system.branch('local.demo.my_iceberg_table', 'audit-branch', {third_snapshot_id})")

            # Perform writes on the audit branch
            self.spark.sql("INSERT INTO local.demo.my_iceberg_table VALUES (999, 'Audit_Student', 50)")

            # A validation workflow can validate the state of the audit branch here
            # Assuming validation passes, fast-forward main to the head of audit branch
            self.spark.sql(
                "CALL spark_catalog.system.fast_forward('local.demo.my_iceberg_table', 'main', 'audit-branch')")

            return 200, "Operation completed successfully!"
        except Exception as error:
            logging.error(error)
            return 500, "Internal Server Error"