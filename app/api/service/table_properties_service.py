from pyiceberg.catalog import load_catalog
from ..utils.SparkConnection import SparkConnection
import logging
from fastapi import HTTPException
from ..schema.alter_iceberg_table_request import  ChangeIcebergTableProperties, UnsetIcebergTableProperties
class TableProperties():
    def __init__(self):
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()
        # Need to ask for the catalog log from configuration file instead of hardcoding.
        self.catalog = load_catalog(spark_conn_obj.get_catalog())

    def getCatalog(self):
        """
            Retrieves the current catalog instance.

            @return A tuple containing the HTTP status code (200) and a string representation of the catalog.
        """
        return 200, f"Catalog: {self.catalog}"

    def getTableProperties(self, database_name, table_name):
        """
            Fetches and returns the properties of a specific table identified by the database and table name provided in the request.

            @param database_name, table_name: Actual 'database_name' and 'table_name'
            @return A tuple containing the HTTP status code (200 for success, 404 for ill-formed request) and
                    either the properties of the specified table as a dictionary or an error message.
            @throws HTTPException: If an error occurs while loading the table or fetching its properties
        """

        if not database_name or not table_name:
            return 404, "Ill-formed request: 'table_name', and 'database_name' cannot be empty."
        try:
            if not self.spark.catalog.tableExists(f'{database_name}.{table_name}'):
                return 404, f"The specified table {database_name}.{table_name} does not exist"

            table = self.catalog.load_table(f'{database_name}.{table_name}')
            logging.info(f"GetTableProperties: Loaded table correctly: {table.name()}")
            # Assuming properties is a dictionary of table properties
            properties = {key: table.properties[key] for key in table.properties.keys()}
            logging.info(f"Table {database_name}.{table_name} Properties: {properties}")

            # Return properties as JSON
            return 200, properties

        except Exception as exception:
            logging.error(f"Error in getProperties: {exception}")
            raise HTTPException(status_code=500, detail=str(exception))

    def getCatalogProperties(self):
        """
            Retrieves and returns properties of the current catalog, including its name.

            @return A tuple containing the HTTP status code (200) and
                    a dictionary of the catalog properties with an additional key 'catalog_name'
            @throws HTTPException: If an error occurs while accessing catalog properties, an HTTPException is raised.
        """
        try:
            catalogProperties = self.catalog.properties
            # Assuming properties is a dictionary of catalog properties
            properties = {key: catalogProperties[key] for key in catalogProperties}
            result = {"catalog_name" : self.catalog.name, "properties" : properties}
            logging.info(f"Catalog Properties: {properties}")
            # Return properties as JSON
            return 200, result

        except Exception as exception:
            logging.error(f"Error in getProperties: {exception}")
            raise HTTPException(status_code=500, detail=str(exception))


    def alter_table_properties(self, request: ChangeIcebergTableProperties):
        """
                Alter table properties using Spark SQL.

                Parameters:
                - dbname: Database name as a string
                - table_name: Table name as a string
                - properties: Dictionary of properties to alter, in the format of [{'propertytype.name': value}, ...]
                """
        # Iterate over the properties dictionary
        db_name = request.db_name
        table_name = request.table_name
        properties = request.properties

        if not db_name or not table_name:
            return 404, "Ill-formed request: 'table_name', and 'database_name' cannot be empty."

        if not properties or properties == []:
            return 404, f"No properties specified to alter for the table {db_name}.{table_name}"

        try:
            if not self.spark.catalog.tableExists(f'{db_name}.{table_name}'):
                return 404, f"The specified table {db_name}.{table_name} does not exist"

            print(f"In alter table properties for table {db_name}.{table_name}")
            for prop in properties:
                for key, value in prop.items():
                    # Generate and execute the ALTER TABLE command to set each property
                    alter_command = f"ALTER TABLE {db_name}.{table_name} SET TBLPROPERTIES ('{key}' = '{value}')"
                    self.spark.sql(alter_command)
                    print(f"Executed: {alter_command}")
            return 200, "Table properties altered successfully."

        except Exception as error:
            return 500, error


    def unset_table_properties(self, request: UnsetIcebergTableProperties):
        """
                Unset table properties using Spark SQL.

                Parameters:
                - dbname: Database name as a string
                - table_name: Table name as a string
                - properties: Dictionary of properties to alter, in the format of [{'propertytype.name': value}, ...]
                """
        # Iterate over the properties dictionary
        db_name = request.db_name
        table_name = request.table_name
        properties = request.properties

        if not db_name or not table_name:
            return 404, "Ill-formed request: 'table_name', and 'database_name' cannot be empty."

        if not properties or properties == []:
            return 404, f"No properties specified to unset for the table {db_name}.{table_name}"

        try:
            if not self.spark.catalog.tableExists(f'{db_name}.{table_name}'):
                return 404, f"The specified table {db_name}.{table_name} does not exist"

            logging.info(f"In unset table properties for table {db_name}.{table_name}")
            for prop in properties:
                # Generate and execute the ALTER TABLE command to set each property
                unset_command = f"ALTER TABLE {db_name}.{table_name} UNSET TBLPROPERTIES ('{prop}')"
                self.spark.sql(unset_command)
                logging.info(f"Executed: {unset_command}")

            return 200, "Table properties unset successfully."
        except Exception as error:
            return 500, error

