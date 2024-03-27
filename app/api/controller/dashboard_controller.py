from typing import Optional
from fastapi_router_controller import Controller
from fastapi import APIRouter, Depends
from ..utils.SparkConnection import SparkConnection
from fastapi import HTTPException
import logging
from ..service.dashboard_service import DashboardService


# defining the fastapi router
router = APIRouter(prefix='/dashboard')
# create a controller descriptor and pass the router to bind
controller = Controller(router, openapi_tag={
    'name': 'dashboard-controller',
})


# Mark SampleController Class to use it automatically
@controller.use()
# Mark SampleController Class as resource of the given Controller router
@controller.resource()
class DashboardController():
    def __init__(self, dashboard_service: DashboardService = Depends()):
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()
        self.dashboard_service = dashboard_service

    """
            Endpoint to list all databases in Spark SQL.
            Returns a list of database names.
    """
    @controller.route.get(
        '/list-databases',
        tags=['dashboard-controller'],
        summary='List databases.')
    def list_databases(self):
        try:
            status_code, data = self.dashboard_service.list_databases()

            if status_code == 404 or status_code == 500:
                return HTTPException(status_code=status_code, detail=data)
            elif status_code == 200:
                return {"db_list": data}
        except Exception as error:
            logging.error("Error: DashboardController: /list-databases:",error)
            return HTTPException(status_code=500, detail="Internal server error.")

    """
        Endpoint to list all databases, tables, branches and tags.
        Query Params:
            db_name = ""
            table_name = ""
            branch_name = ""
        API usage:
            API without using any Query param - returns database list.
            API with db_name - returns tablename list within the specified database.
            API with pass db_name and table_name- returns snapshot details from main branch along with branch list.
            API with db_name, table_name and branch_name - returns snapshot details from specified branch along with branch list. 
    """
    @controller.route.get(
        '/snapshots',
        tags=['dashboard-controller'],
        summary='List all databases, tables, branches and tags.')
    def get_snapshot(self, branch_name: str = "main", db_name: Optional[str] = None, table_name: Optional[str] = None):
        try:
            status_code, data = self.dashboard_service.get_snapshot(branch_name, db_name, table_name)

            if status_code == 404 or status_code == 500:
                return HTTPException(status_code=status_code, detail=data)
            elif status_code == 200:
                return {"message": "Success.", "response": data}
        except Exception as e:
            logging.error("Error: DashboardController: /snapshots:", e)
            return HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")