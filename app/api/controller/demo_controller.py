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
        summary='Create Demo tables.')
    def create_demo_tables(self):
        try:
            status_code, data = self.demo.create_car_sales_table()
            if status_code == 200:
                return {"message": "Created demo database/tables successfully"}
            else:
                return HTTPException(status_code=status_code, detail="data")
        except Exception as error:
            logging.error(f"Error: DemoController: /create_demo_tables {error}")
            return HTTPException(status_code=500, detail="Internal server error.")