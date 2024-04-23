from ..utils.SparkConnection import SparkConnection
import logging
from json import loads
from zoneinfo import ZoneInfo

class DashboardService():
    def __init__(self):
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()

    def list_databases(self):
        try:
            # Ensure Spark session is available
            if self.spark is None:
                return 500, "Spark session not initialized."

            spark = self.spark
            logging.info("In List Database function")

            databases = spark.catalog.listDatabases()
            db_list = [db.name for db in databases]

            if not db_list:
                return 404, "No databases found."

            return 200, db_list
        except Exception as error:
            logging.error("Error: DashboardService: list_databases:", error)
            return 500, error;

    def get_snapshot(self, branch_name, db_name, table_name):
        try:
            # Ensure Spark session is available
            if self.spark is None:
                return 500, "Spark session not initialized."

            spark = self.spark
            response = None
            if not db_name and not table_name:
                # Return Db names
                databases = spark.catalog.listDatabases()
                response = [db.name for db in databases]
            elif db_name and not table_name:
                # Return table names
                tables = spark.catalog.listTables(db_name)
                response = [table.name for table in tables]
            elif db_name and table_name and branch_name:
                # Return snapshot details from main branch
                snapshots = spark.sql(
                    f"select * from local.{db_name}.{table_name}.history h join local.{db_name}.{table_name}.snapshots s on h.snapshot_id = s.snapshot_id order by made_current_at;")
                # Convert DataFrame to JSON string
                snapshots_json = snapshots.toJSON().collect()  # spark dataframe
                # Convert json string to json
                response_data = []
                for json_str in snapshots_json:
                    json_data = loads(json_str)
                    response_data.append(json_data)
                # Append branch names list
                branches = spark.sql(f"SELECT * FROM local.{db_name}.{table_name}.refs where type = \"BRANCH\";")
                branches_json = branches.toJSON().collect()
                branches_data = []
                for brch_json_str in branches_json:
                    brch_json_data = loads(brch_json_str)
                    branches_data.append(brch_json_data)
                # Append tag list
                tags = spark.sql(f"SELECT * FROM local.{db_name}.{table_name}.refs where type = \"TAG\";")
                tags_json = tags.toJSON().collect()
                tags_data = []
                for tags_json_str in tags_json:
                    tags_json_data = loads(tags_json_str)
                    tags_data.append(tags_json_data)
                response = {"snapshots": response_data, "branches": branches_data, "tags": tags_data}
            else:
                return 404, "Invalid query parameters."
            return 200, response
        except Exception as error:
            logging.error("Error: DashboardService: get_snapshot:", error)
            return 500, error;

    def list_tables(self, db_name):
        if not db_name:
            return 404, "Database name cannot be empty or null"
        try:
            # Ensure Spark session is available
            if self.spark is None:
                return 500, "Spark session not initialized."

            spark = self.spark
            logging.info("In List Tables function")
            tables = spark.catalog.listTables(db_name)
            result = []
            for table in tables:
                table_name = table.name
                # Construct the query to access the snapshots table of the current table
                snapshot_query = f"SELECT * FROM {db_name}.{table_name}.snapshots ORDER BY committed_at DESC LIMIT 1"

                # Execute the query
                snapshot_df = spark.sql(snapshot_query)

                # Collect the result. Be cautious with `collect()` for larger datasets.
                last_snapshot = snapshot_df.collect()

                if last_snapshot:  # Check if there is at least one snapshot
                    # Extract and convert the committed_at datetime to a human-readable format
                    last_updated_timestamp_utc = last_snapshot[0]['committed_at']
                    if last_updated_timestamp_utc.tzinfo is None:
                        last_updated_timestamp_utc = last_updated_timestamp_utc.replace(tzinfo=ZoneInfo("UTC"))

                    last_updated_timestamp_pst = last_updated_timestamp_utc.astimezone(ZoneInfo("America/Los_Angeles"))
                    human_readable_last_updated = last_updated_timestamp_pst.strftime('%Y-%m-%d at %H:%M %Z')
                    result.append({"table_name": table_name, "last_updated": human_readable_last_updated})
                else:
                    logging.info(f"No snapshots found for table {table_name}")
                    result.append({"table_name": table_name, "last_updated": None})
            return 200, result
        except Exception as error:
            logging.error(f"Error: DashboardService: list_tables: {error}")
            return 500, error

