from pyiceberg.catalog import load_catalog
from ..utils.SparkConnection import SparkConnection
import logging
from fastapi import HTTPException
class TableProperties():
    def __init__(self):
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()
        # Need to ask for the catalog log from configuration file instead of hardcoding.
        self.catalog = load_catalog('local')

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

