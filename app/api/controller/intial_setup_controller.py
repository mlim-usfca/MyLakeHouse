from fastapi_router_controller import Controller
from fastapi import APIRouter, Depends
from fastapi import HTTPException
import logging
from ..service.intial_setup_service import IntialSetupService
from ..schema.create_iceberg_table_request_schema import CreateIcebergTableRequest


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

    @controller.route.post(
        '/create_toy_db',
        tags=['intial-setup-controller'],
        summary='Creates a toy database: toyDb and two mini tables  local.toyDb.taxis1, local.toyDb.taxis2 and \
                inserts some records in these to have a snapshot history. For testing purposes only. The script sleeps for 60 secs \
                to create tables 1 minute apart.')
    def create_toy_iceberg_table(self):
        try:
            status_code, data = self.initial_setup_service.create_toy_iceberg_database()
            if status_code == 200:
                return {"message": "Created toy database successfully"}
            else:
                return HTTPException(status_code=status_code, detail="data")
        except Exception as error:
            logging.error("Error: InitialSetupController: /create_toy_db")
            return HTTPException(status_code=500, detail="Internal server error.")

