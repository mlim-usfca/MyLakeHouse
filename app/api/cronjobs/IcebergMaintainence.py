import json
import logging
from json import loads

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import Depends
from ..utils.SparkConnection import SparkConnection
from datetime import datetime

class IcebergMaintainence(object):

    def __init__(self, scheduler: AsyncIOScheduler):
        with open("./config.json") as configFile:
            self.config = json.load(configFile)
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()
        self.catalog = spark_conn_obj.get_catalog()
        self.scheduler = scheduler
        self.add_jobs()

    def add_jobs(self):
        ##### Expire snapshot
        expire_day, expire_hour, expire_minute = self.get_trigger_parameters("expire_snapshot_trigger")
        expire_snapshot_trigger = CronTrigger(day=expire_day, hour=expire_hour, minute=expire_minute)
        # expire_snapshot_trigger = CronTrigger(second=20)
        self.scheduler.add_job(self.expire_snapshot, expire_snapshot_trigger)

        # ##### Compaction Trigger
        compact_day, compact_hour, compact_minute= self.get_trigger_parameters("compaction_trigger")
        compaction_trigger = CronTrigger(day=compact_day, hour=compact_hour, minute=compact_minute)
        # compaction_trigger = CronTrigger(second=40)
        self.scheduler.add_job(self.compaction, compaction_trigger)

        #### Remove Orphan
        remove_orphan_day, remove_orphan_hour, remove_orphan_minute = self.get_trigger_parameters("remove_orphan_trigger")
        remove_orphan_trigger = CronTrigger(day=remove_orphan_day, hour=remove_orphan_hour, minute=remove_orphan_minute)
        # remove_orphan_trigger = CronTrigger(second=55)
        self.scheduler.add_job(self.remove_orphan, remove_orphan_trigger)

    def get_trigger_parameters(self, trigger):
        day = self.config["scheduler"][trigger]["day"]
        hour = self.config["scheduler"][trigger]["hour"]
        minute = self.config["scheduler"][trigger]["minute"]
        return day, hour, minute

    async def expire_snapshot(self):
        logging.info("In expire_snapshot")
        try:
            # Ensure Spark session is available
            if self.spark is None:
                logging.error("Spark session not initialized.")
                return

            # Get current year and month
            current_date = datetime.now()
            current_year = current_date.year # Extract current year
            current_month = "{:02d}".format(current_date.month) # Extract current month

            # get database name list
            databases = self.spark.catalog.listDatabases()
            db_list = [db.name for db in databases]
            for db in db_list:
                # get table names of every db
                tables = self.spark.catalog.listTables(db)
                table_list = [table.name for table in tables]
                for table_name in table_list:
                    # 1. Expire all snapshot except last 1 for each month.
                    all_snapshots = self.spark.sql(f'select * from {self.catalog}.{db}.{table_name}.snapshots order by committed_at;')
                    # all_snapshots = self.spark.sql(f'select * from local.{db}.{table_name}.snapshots WHERE committed_at LIKE \'{current_year}-{current_month}%\' order by committed_at;')
                    # Filter snapshots for the specified month
                    snapshot_ids = []
                    snapshots_json = all_snapshots.toJSON().collect()  # spark dataframe
                    for snapshot in snapshots_json:
                        json_data = loads(snapshot)
                        if json_data['committed_at'][:7] == f'{current_year}-{current_month}':
                            snapshot_ids.append(json_data['snapshot_id'])

                    if len(snapshot_ids) > 1:
                        # Construct the array string representation
                        snapshot_ids_str = ','.join(str(id) for id in snapshot_ids[0:-1])
                        expire_snapshot_query = f'CALL {self.catalog}.system.expire_snapshots(table => \'{db}.{table_name}\', snapshot_ids => ARRAY({snapshot_ids_str}))'
                        self.spark.sql(expire_snapshot_query)
                logging.info("Executed expire_snapshot query.")
        except Exception as error:
            logging.error("Error message:", error)

    async def compaction(self):
        logging.info("Compaction")
        try:
            # get database name list
            databases = self.spark.catalog.listDatabases()
            db_list = [db.name for db in databases]
            for db in db_list:
                # get table names of every db
                tables = self.spark.catalog.listTables(db)
                table_list = [table.name for table in tables]
                for table_name in table_list:
                    # 2. Just call Rewrite_data_files  query on the table.
                    compaction_query = f'CALL {self.catalog}.system.rewrite_data_files(table => \'{db}.{table_name}\')'
                    self.spark.sql(compaction_query)
            logging.info("Compaction ended")
        except Exception as error:
            logging.error("Error message:", error)

    async def remove_orphan(self):
        logging.info("In remove Orphans")
        try:
            # get database name list
            databases = self.spark.catalog.listDatabases()
            db_list = [db.name for db in databases]
            for db in db_list:
                # get table names of every db
                tables = self.spark.catalog.listTables(db)
                table_list = [table.name for table in tables]
                for table_name in table_list:
                    # 2. Call remove_orphan_files  query on the table.
                    delete_orphan_files_query = f'CALL {self.catalog}.system.remove_orphan_files(table => \'{db}.{table_name}\');'
                    self.spark.sql(delete_orphan_files_query)
            logging.info("Remove orphans ended")
        except Exception as error:
            logging.error("Error message:", error)