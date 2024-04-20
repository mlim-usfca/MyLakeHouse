import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..cronjobs.IcebergMaintainence import IcebergMaintainence

class CronScheduler(object):

    def __init__(self):
        # Instantiate the scheduler
        self.create_scheduler()

        #Add jobs
        IcebergMaintainence(self.scheduler)

        #start scheduler
        self.start_scheduler()

    def create_scheduler(self):
        # Initialize an AsyncIOScheduler with the jobstore
        self.scheduler = AsyncIOScheduler()
        logging.info("Scheduler instantiated.")

    def start_scheduler(self):
        self.scheduler.start()
        logging.info("Scheduler Started")