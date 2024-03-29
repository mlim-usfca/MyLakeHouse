from fastapi_router_controller import Controller
from fastapi import APIRouter, Depends
from ..service.table_properties_service import TableProperties
from fastapi import HTTPException
import logging
from ..schema.table_properties_schema import TablePropertiesRequest

# defining the fastapi router
router = APIRouter(prefix='/tp')
# create a controller descriptor and pass the router to bind
controller = Controller(router, openapi_tag={
    'name': 'table-properties-controller',
})

@controller.use()

@controller.resource()
class TablePropertiesController():
    def __init__(self, table_properties_service:  TableProperties = Depends()):
        self.table_properties_service = table_properties_service


    """
            Endpoint to test PyIceberg installation.
    """
    @controller.route.get('/catalog',
                            tags=['table-properties-controller'],
                            description="Endpoint to test PyIceberg Installation")
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

    @controller.route.post('/readProps',
                          tags=['table-properties-controller'],
                          description='GetRead Properties of a table')

    def get_read_properties(self, request : TablePropertiesRequest):
        try:
            status_code, data = self.table_properties_service.getReadProperties(request)
            if status_code == 200:
                return data
            else:
                return HTTPException(status_code=status_code, detail=data)
        except Exception as error:
            logging.error("Error: TablePropertiesController: /tp/readProp:", error)
            return HTTPException(status_code=500, detail="Internal server error.")