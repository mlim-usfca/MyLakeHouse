from fastapi_router_controller import Controller
from fastapi import APIRouter, Depends
from fastapi import HTTPException
import logging
from ..demo.demo_tables import DemoIcebergTables


# defining the fastapi router
router = APIRouter(prefix='/demo')
# create a controller descriptor and pass the router to bind
controller = Controller(router, openapi_tag={
    'name': 'demo-controller',
})


# Mark SampleController Class to use it automatically
@controller.use()
# Mark SampleController Class as resource of the given Controller router
@controller.resource()
class DemoController():
    def __init__(self, demo: DemoIcebergTables = Depends()):
        self.demo = demo

    @controller.route.post(
        '/create_demo_tables',
        tags=['demo-controller'],
        summary='Create Demo databases: carsales and wildlife.')
    def create_demo_tables(self):
        try:
            status_code, data = self.demo.create_demo_databases()
            if status_code == 200:
                return {"message": "Created demo database/tables successfully"}
            else:
                return HTTPException(status_code=status_code, detail="data")
        except Exception as error:
            logging.error(f"Error: DemoController: /create_demo_tables {error}")
            return HTTPException(status_code=500, detail="Internal server error.")

    @controller.route.post(
        '/create_snapshot_demo_tables',
        tags=['demo-controller'],
        summary='Creates a table for Snapshots branching and tagging demo. The table inserts 30 records into the tables, thus creating 30 snapshots. \
                .Then alters the table to create 3 branches from snapshots version 3rd, 7th and 29th. Also creates two tags from snapshot version 2nd and 5th')
    def create_snapshot_demo_table(self):
        try:
            status_code, data = self.demo.snapshots_branching_and_tagging()
            if status_code == 200:
                return {"message": "Created snapshot branching database/table successfully"}
            else:
                return HTTPException(status_code=status_code, detail="data")
        except Exception as error:
            logging.error(f"Error: DemoController: /create_snapshot_demo_tables {error}")
            return HTTPException(status_code=500, detail="Internal server error.")

    @controller.route.post(
        '/visualize_branches_and_tags',
        tags=['demo-controller'],
        summary='Dumps the data inserted into tables after branching and tagging in a file \'iceberg_branching.txt\'.')
    def create_snapshot_demo_table(self):
        try:
            status_code, data = self.demo.output_queries_to_file()
            if status_code == 200:
                return {"message": "Created file successfully. Look into your container at path /app"}
            else:
                return HTTPException(status_code=status_code, detail="data")
        except Exception as error:
            logging.error(f"Error: DemoController: /visualize_branches_and_tags {error}")
            return HTTPException(status_code=500, detail="Internal server error.")