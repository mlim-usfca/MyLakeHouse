from fastapi_router_controller import Controller
from fastapi import APIRouter, Depends
from ..service.table_properties import TableProperties
from ..utils.SparkConnection import SparkConnection
from fastapi import HTTPException
import logging


# defining the fastapi router
router = APIRouter(prefix='/tp')
# create a controller descriptor and pass the router to bind
controller = Controller(router, openapi_tag={
    'name': 'table_properties-controller',
})

@controller.use()

@controller.resource()
class TablePropertiesController():
    def __init__(self, table_properties_service:  TableProperties = Depends()):
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()
        self.table_properties_service = table_properties_service


    """
            Endpoint to list all databases in Spark SQL.
            Returns a list of database names.
    """
    @controller.route.get(
        '/catalog')
    def test_pyiceberg(self):
        try:
            status_code, data = self.table_properties_service.getCatalog()

            if status_code == 404 or status_code == 500:
                return HTTPException(status_code=status_code, detail=data)
            elif status_code == 200:
                return {"catalog": data}
        except Exception as error:
            logging.error("Error: TableProperties: /catalog:",error)
            return HTTPException(status_code=500, detail="Internal server error.")

