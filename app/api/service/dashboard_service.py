from api.utils.SparkConnection import SparkConnection
import logging
from json import loads


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
