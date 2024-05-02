from ..utils.SparkConnection import SparkConnection
import logging
from pyspark.sql.types import StructType, StructField,StringType, DoubleType, LongType, IntegerType
from pyiceberg.catalog import load_catalog


class DemoIcebergTables():
    def __init__(self):
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()
        self.catalog = spark_conn_obj.get_catalog()
        self.catalog_obj = load_catalog(self.catalog)

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
            table_name = "local.demo.my_iceberg_table"
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
            table = self.catalog_obj.load_table('local.demo.my_iceberg_table')

            snapshots = table.metadata.snapshots

            # Make branches from snapshot 3, 7 and 29
            if snapshots is not None:
                snapshot_id_3 = snapshots[2].snapshot_id
                snapshot_id_7 = snapshots[6].snapshot_id
                snapshot_id_28 = snapshots[27].snapshot_id
                branch_from_3_command = f"ALTER TABLE {table_name} CREATE BRANCH test_from_3 AS OF VERSION {snapshot_id_3}"
                branch_from_7_command = f"ALTER TABLE {table_name} CREATE BRANCH test_from_7 AS OF VERSION {snapshot_id_7}"
                branch_from_28_command = f"ALTER TABLE {table_name} CREATE BRANCH test_from_28 AS OF VERSION {snapshot_id_28} with SNAPSHOT RETENTION 5 SNAPSHOTS"
                self.spark.sql(branch_from_3_command)
                self.spark.sql(branch_from_7_command)
                self.spark.sql(branch_from_28_command)

                # Insert records into branches
                insert_31 = f"INSERT INTO TABLE {table_name}.branch_test_from_3 VALUES (99, 'Student_Ak', 67)"
                insert_32 = f"INSERT INTO TABLE {table_name}.branch_test_from_3 VALUES (123, 'Student_Amy', 97)"
                self.spark.sql(insert_31)
                self.spark.sql(insert_32)

                insert_71 = f"INSERT INTO TABLE {table_name}.branch_test_from_7 VALUES (129, 'Student_Rachel', 49)"
                insert_72 = f"INSERT INTO TABLE {table_name}.branch_test_from_7 VALUES (165, 'Student_Akon', 84)"
                self.spark.sql(insert_71)
                self.spark.sql(insert_72)

            # Make tags from snapshots 2 and 5
            if snapshots is not None:
                snapshot_id_2 = snapshots[1].snapshot_id
                snapshot_id_5 = snapshots[4].snapshot_id
                logging.info(f"In tags {snapshot_id_2}  {snapshot_id_5}")
                self.spark.sql(f"ALTER TABLE {table_name} CREATE TAG tag_3rd AS OF VERSION {snapshot_id_2}")
                self.spark.sql(f"ALTER TABLE {table_name} CREATE TAG tag_5th AS OF VERSION {snapshot_id_5}")

            return 200, "Operation completed successfully!"
        except Exception as error:
            logging.error(f"Error in snapshots_branching_and_tagging:  {error}")
            return 500, "Internal Server Error"

    def output_queries_to_file(self, table_name="local.demo.my_iceberg_table"):
        def write_query_results_to_file(query, file):
            result = self.spark.sql(query).collect()
            if result:
                headers = list(result[0].asDict().keys())
                rows = [list(row.asDict().values()) for row in result]

                # Write the query and headers
                file.write(f"Results for query: {query}\n")
                file.write("\t".join(headers) + "\n")

                # Write rows
                for row in rows:
                    file.write("\t".join(map(str, row)) + "\n")

                file.write("\n")  # Add a new line after each query's results
            else:
                file.write(f"\nNo results for query: {query}\n")
        try:
            queries = [
                f"SELECT * FROM {table_name}",
                f"SELECT * FROM {table_name} VERSION AS OF 'test_from_3'",
                f"SELECT * FROM {table_name} VERSION AS OF 'test_from_7'",
                f"SELECT * FROM {table_name} VERSION AS OF 'tag_3rd'",
                f"SELECT * FROM {table_name} VERSION AS OF 'tag_5th'"
            ]

            # Write the results of each query to the file
            with open("iceberg_branching.txt", "w") as file:
                for query in queries:
                    write_query_results_to_file(query, file)
            return 200, "Ok"
        except Exception as error:
            logging.error(f"Error in output_queries_to_file:  {error}")
            return 500, "Internal Server Error"