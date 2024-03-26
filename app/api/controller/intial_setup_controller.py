from fastapi_router_controller import Controller
from fastapi import APIRouter, Depends
from fastapi import HTTPException
import logging
from api.service.intial_setup_service import IntialSetupService
from api.schema.create_iceberg_table_request_schema import CreateIcebergTableRequest
from api.utils.SparkConnection import SparkConnection


# defining the fastapi router
router = APIRouter(prefix='/intial-setup')
# create a controller descriptor and pass the router to bind
controller = Controller(router, openapi_tag={
    'name': 'intial-setup-controller',
})


# Mark SampleController Class to use it automatically
@controller.use()
# Mark SampleController Class as resource of the given Controller router
@controller.resource()
class InitialSetupController():
    def __init__(self, initial_setup_service: IntialSetupService = Depends()):
        spark_conn_obj = SparkConnection()
        self.spark = spark_conn_obj.get_spark_session()
        self.initial_setup_service = initial_setup_service

    """
    Endpoint to create table.
    Returns success or failure message.
    """
    @controller.route.post(
        '/create_table',
        tags=['intial-setup-controller'],
        summary='Create table.')
    def create_iceberg_table(self, request: CreateIcebergTableRequest):
        try:
            status_code, data = self.initial_setup_service.create_iceberg_table(request)
            if status_code == 404 or status_code == 500:
                return HTTPException(status_code=status_code, detail=data)
            elif status_code == 200:
                return {"message": data}
        except Exception as error:
            logging.error("Error: InitialSetupController: /create_table:", error)
            return HTTPException(status_code=500, detail="Internal server error.")