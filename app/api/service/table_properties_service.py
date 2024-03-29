from pyiceberg.catalog import load_catalog
from ..utils.SparkConnection import SparkConnection
from ..schema.table_properties_schema import TablePropertiesRequest
import logging
from typing import Dict
class TableProperties():
    def __init__(self):
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()
        self.catalog = load_catalog('local')


    def getCatalog(self):
        return 200, f"Catalog: {self.catalog}"

    def getReadProperties(self, request : TablePropertiesRequest):

            database_name = request.database_name
            table_name = request.table_name

            if not database_name or not table_name:
                return 404, "Ill-formed request: 'table_name', and 'database_name' cannot be empty."

            read_property_keys = [
                "read.split.target-size",
                "read.split.metadata-target-size",
                "read.split.planning-lookback"
            ]
            table = self.catalog.load_table(f'{database_name}.{table_name}')
            logging.info("Loaded table correctly")
            logging.info(table.name())
            properties = table.metadata.properties.keys()
            properties1 = table.properties.keys()
            spec1 = table.specs()
            '''logging.info(spec1)
            logging.info(properties)
            logging.info(properties1)
            for key in properties:
                logging.info(key)'''
            read_properties: Dict[str, str] = {
                "read.split.target-size": "128 * 1024 * 1024",  # Example: 128 MB as a string
                "read.split.metadata-target-size": "4 * 1024 * 1024",  # Example: 4 MB as a string
                "read.split.planning-lookback": "100",  # Example: Lookback for 100 files as a string
            }
            #properties_sql = " \n".join([f"'{k}'='{v}'" for k, v in read_properties.items()])

            '''logging.info("In trry block")
            transaction = table.transaction()
            logging.info("New transaction")

            #transaction.set_properties(PARQUET_ROW_GROUP_LIMIT="128 * 1024 * 1024").commit_transaction()
            #logging.info("Set Properties1")
            transaction.set_properties(properties=properties_sql).commit_transaction()
            logging.info("Set Properties2")
            logging.info(f"'Successfully set read properties for table '{database_name}.{table_name}'")'''

            '''create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS local.db_march.table2 (
                id INT,
                name STRING,
                data STRING
            ) USING iceberg
            OPTIONS (
                {properties_sql}
            )
            """
            self.spark.sql(create_table_sql)
            # Insert records using Spark SQL
            self.spark.sql("""
            INSERT INTO local.db_march.table2 VALUES 
            (1, 'Alice', 'Data1'), 
            (2, 'Bob', 'Data2'), 
            (3, 'Cara', 'Data3')
            """)'''
            #self.spark.sql("ALTER TABLE local.db_march.table2 SET TBLPROPERTIES (\'read.split.metadata-target-size\'=\'4 * 1024 * 1024\');")
            #self.spark.sql("ALTER TABLE local.db_march.table2 SET TBLPROPERTIES (\'read.split.planning-lookback\'=\'100\');")
            #self.spark.sql("ALTER TABLE local.db_march.table2 SET TBLPROPERTIES (\'read.split.target-size\'=\'128 * 1024 * 1024\');")
            #self.spark.sql("ALTER TABLE local.db_march.table2 UNSET TBLPROPERTIES (\'PARQUET_ROW_GROUP_LIMIT\');" )
            #self.spark.sql("ALTER TABLE local.db_march.table2 UNSET TBLPROPERTIES (\'properties\');")
            # Execute the SQL command

            table1 = self.catalog.load_table('db_march.table2')
            table1.transaction().remove_properties("properties").commit_transaction()
            properties1 = table1.properties.keys()
            logging.info(f'table1 properties: {properties1}')
            logging.info(f'table1 values: {table1.properties.values()}')
            logging.info(f'taxis_march properties: {table.properties.keys()}')
            logging.info(f'Catalog Properties: {self.catalog.properties}')
            '''properties2 = {}
            for key in read_property_keys:
                logging.info(key)
                try:
                    value = table.properties().get(key)
                    logging.info(value)
                    if value is not None:
                        properties2[key] = value
                except:
                    logging.info("Error")
                    pass  # Ignore missing properties
            logging.info(properties2)'''
            logging.info(table1.metadata.properties)
            return 200, "Ok"


