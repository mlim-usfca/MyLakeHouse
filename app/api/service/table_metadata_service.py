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

    def getTableSchema(self, db_name, table_name):
        logging.info("In Get Table Schema service")
        if not db_name or not table_name:
            return 404, "Ill-formed request: 'table_name', and 'database_name' cannot be empty."
        try:
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
                       if key is not "metadata":
                           fieldVals[key] = val
                   returnVal.append(fieldVals)
               return 200, returnVal
        except Exception as error:
            logging.info(f"Error in getTableSchema: {error}")
            return 500, error


    def getTableInfo(self, db_name, table_name):
        logging.info("In Get Table Info service")
        if not db_name or not table_name:
            return 404, "Ill-formed request: 'table_name', and 'database_name' cannot be empty."
        try:
            table = self.catalog.load_table(f'{db_name}.{table_name}')
            returnDict = {}
            #Table Location
            location = table.location()
            if location and len(location) > 0:
                returnDict["TableLocation"] = location

            #Table UUID
            table_uuid = table.metadata.table_uuid.__str__()
            if table_uuid:
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
            files = self.spark.sql(f"SELECT file_path, file_format, record_count, file_size_in_bytes,\
                                            null_value_counts, nan_value_counts, lower_bounds, upper_bounds \
                                            FROM local.{db_name}.{table_name}.all_data_files LIMIT {limit} OFFSET {offset}")

            if not files:
                return 404, f"Cannot get any data files for table {db_name}.{table_name}"

            for row in files.collect():
                return row
        except Exception as error:
            logging.info(f"Error in getDataFiles: {error}")
            return 500, error