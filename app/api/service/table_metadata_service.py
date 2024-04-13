from pyiceberg.catalog import load_catalog
from ..utils.SparkConnection import SparkConnection
import logging
from zoneinfo import ZoneInfo
from datetime import datetime, timezone
class TableMetadata():
    def __init__(self):
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()
        # Need to ask for the catalog log from configuration file instead of hardcoding.
        self.catalog = load_catalog('local')

    def decode_byte_array(self, byte_array):
        try:
            return int.from_bytes(byte_array, byteorder='little', signed=True)
        except:
            try:
                return byte_array.decode('utf-8')
            except UnicodeDecodeError:
                return str(byte_array)

    def getTableSchema(self, db_name, table_name):
        """
            Retrieves the schema of a specified table in a given database using Spark. It logs the process,
            checks for valid input, queries the table schema, and formats it into a list of dictionaries excluding metadata.

            Args:
                db_name (str): The name of the database containing the table.
                table_name (str): The name of the table whose schema is to be fetched.

            Returns:
                tuple:
                    - First element is an integer (HTTP status code)
                    - Second element is either a list of dictionaries (each representing a field in the table schema) or a string error message.

            Raises:
                Exception: Captures and logs any exception that occurs within the method, then returns a 500 status with the error message.
        """
        logging.info("In Get Table Schema service")
        if not db_name or not table_name:
            return 404, f"Ill-formed request: 'table_name', and 'database_name' cannot be empty."
        try:
            if not self.spark.catalog.tableExists(f'{db_name}.{table_name}'):
                return 404, f"The specified table {db_name}.{table_name} does not exist"

            table = self.spark.table(f'local.{db_name}.{table_name}')

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
                       if key != "metadata":
                           fieldVals[key] = val
                   returnVal.append(fieldVals)
               return 200, returnVal
        except Exception as error:
            logging.info(f"Error in getTableSchema: {error}")
            return 500, error


    def getTableInfo(self, db_name, table_name):
        logging.info("In Get Table Info service")
        """
            Retrieves comprehensive information about a specified table in a given database, including location,
            UUID, properties like owner and creation time, current snapshot ID, and the last update time. It formats
            time-related data to Pacific Daylight Time (PDT) and handles all data fetching and conversions with robust
            error checking and logging.

            Args:
                db_name (str): The name of the database containing the table.
                table_name (str): The name of the table from which information is to be retrieved.

            Returns:
                tuple:
                    - First element is an integer (HTTP status code): 
                    - Second element is either a dictionary containing key information about the table.

            Raises:
                Exception: Captures and logs any exception that occurs within the method, then returns a 500 status with the error message.
            """
        if not db_name or not table_name:
            return 404, "Ill-formed request: 'table_name', and 'database_name' cannot be empty."
        try:
            if not self.spark.catalog.tableExists(f'{db_name}.{table_name}'):
                return 404, f"The specified table {db_name}.{table_name} does not exist"

            table = self.catalog.load_table(f'{db_name}.{table_name}')
            returnDict = {}
            #Table Location
            location = table.location()
            if location and len(location) > 0:
                returnDict["TableLocation"] = location

            #Table UUID
            table_uuid = table.metadata.table_uuid.__str__()
            if table_uuid and len(table_uuid) > 0 :
                returnDict["TableUUID"] = table_uuid

            #Table Properties: Owner and Created At
            properties = table.metadata.properties
            for key, val in properties.items():
                if key == "owner":
                    returnDict["Owner"] = val
                if key == "created-at":
                    created_at_timestamp_utc = val
                    # Convert string to datetime object
                    try:
                        created_at_timestamp_utc = datetime.fromisoformat(
                                                    created_at_timestamp_utc.replace('Z', '+00:00'))
                        if created_at_timestamp_utc.tzinfo is None:
                            created_at_timestamp_utc = created_at_timestamp_utc.replace(tzinfo=ZoneInfo("UTC"))

                        created_at_timestamp_utc = created_at_timestamp_utc.astimezone(ZoneInfo("America/Los_Angeles"))
                        human_readable_created_at = created_at_timestamp_utc.strftime('%Y-%m-%d at %H:%M %Z')
                        returnDict["Created-At"] = human_readable_created_at
                    except Exception as error:
                        logging.info(f"Cannot convert the created at time string to PDT timestamp : {error}")

            #Table Current Snapshot Id
            currentSnapshotId = table.metadata.current_snapshot_id
            if currentSnapshotId:
                returnDict["CurrentSnapshotId"] = currentSnapshotId

            #Table Last Updated At
            last_updated_timestamp_utc = table.metadata.last_updated_ms
            try:
                last_updated_seconds = last_updated_timestamp_utc / 1000.0
                # Create a UTC datetime object from the timestamp
                utc_datetime = datetime.fromtimestamp(last_updated_seconds, timezone.utc)
                # Convert the datetime object to the PDT timezone
                pdt_datetime = utc_datetime.astimezone(ZoneInfo('America/Los_Angeles'))
                # Format the datetime object to a human-readable form in PDT
                readable_date_pdt = pdt_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')
                # Example of using it in a dictionary
                returnDict["LastUpdatedAt"] = readable_date_pdt
            except Exception as error:
                logging.info(f"Cannot convert the last updated time in milliseconds to PDT timestamp : {error}")

            return 200, returnDict
        except Exception as error:
            logging.info(f"Error in getTableInfo {error}")
            return 500, error


    def getDataFiles(self, db_name, table_name, limit, offset):
        logging.info("In Get Data files service")
        if not db_name or not table_name:
            return 404, "Ill-formed request: 'table_name', and 'database_name' cannot be empty."
        try:
            if not self.spark.catalog.tableExists(f'{db_name}.{table_name}'):
                return 404, f"The specified table {db_name}.{table_name} does not exist"

            files = self.spark.sql(f"SELECT file_path, file_format, record_count, file_size_in_bytes,\
                                            null_value_counts, nan_value_counts, lower_bounds, upper_bounds \
                                            FROM local.{db_name}.{table_name}.all_data_files LIMIT {limit} OFFSET {offset}")

            table = self.spark.table(f'local.{db_name}.{table_name}')
            colNames = table.columns

            if not files:
                return 404, f"Cannot get any data files for table {db_name}.{table_name}"
            result = []
            for row in files.collect():
                # Initialize the dictionary with simple fields
                row_dict = {
                    'file_path': row.file_path,
                    'file_format': row.file_format,
                    'record_count': row.record_count,
                    'file_size_in_bytes': row.file_size_in_bytes
                }
                # Adjust index for 0-based list index by subtracting 1 from the data structure keys
                null_value_counts = {colNames[k - 1]: v for k, v in row['null_value_counts'].items()}
                nan_value_counts = {colNames[k - 1]: v for k, v in row['nan_value_counts'].items()}

                # Process bounds, decode byte arrays, adjust index
                lower_bounds = {colNames[k - 1]: self.decode_byte_array(v) for k, v in row['lower_bounds'].items()}
                upper_bounds = {colNames[k - 1]: self.decode_byte_array(v) for k, v in row['upper_bounds'].items()}

                # Add processed dictionaries to the result
                row_dict['null_value_counts'] = null_value_counts
                row_dict['nan_value_counts'] = nan_value_counts
                row_dict['lower_bounds'] = lower_bounds
                row_dict['upper_bounds'] = upper_bounds

                result.append(row_dict)

            return 200, result
        except Exception as error:
            logging.info(f"Error in getDataFiles: {error}")
            return 500, error
