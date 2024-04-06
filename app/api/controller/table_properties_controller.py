from fastapi_router_controller import Controller
from fastapi import APIRouter, Depends
from ..service.table_properties_service import TableProperties
from fastapi import HTTPException
import logging
from ..schema.alter_iceberg_table_request import ChangeIcebergTableProperties, UnsetIcebergTableProperties

# defining the fastapi router
router = APIRouter(prefix='/props')
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

    """
           Endpoint to get all the table properties.
    """
    @controller.route.get('/getTableProps',
                          tags=['table-properties-controller'],
                          description='Get all Properties of a table')

    def get_table_properties(self, db_name : str, table_name : str):
        try:
            status_code, data = self.table_properties_service.getTableProperties(db_name, table_name)
            if status_code == 200:
                return data
            else:
                return HTTPException(status_code=status_code, detail=data)
        except Exception as error:
            logging.error("Error: TablePropertiesController: /props/getTableProps:", error)
            return HTTPException(status_code=500, detail="Internal server error.")

    """
            Endpoint to get all the current Catalog Properties. 
    """
    @controller.route.get('/getCatalogProps',
                           tags=['table-properties-controller'],
                           description='Get all Properties of the current catalog')
    def get_catalog_properties(self):
        try:
            status_code, data = self.table_properties_service.getCatalogProperties()
            if status_code == 200:
                return data
            else:
                return HTTPException(status_code=status_code, detail=data)
        except Exception as error:
            logging.error("Error: TablePropertiesController: /props/getCatalogProps:", error)
            return HTTPException(status_code=500, detail="Internal server error.")


    """
             Endpoint to alter Table Properties
    """
    @controller.route.post('/alterTableProps',
                           tags=['table-properties-controller'],
                           description='Alter the properties of the table specified')
    def alter_table_properties(self, request: ChangeIcebergTableProperties):
        try:
            status_code, data = self.table_properties_service.alter_table_properties(request)
            if status_code == 200:
                return data
            else:
                return HTTPException(status_code=status_code, detail=data)
        except Exception as error:
            logging.info("Error: TablePropertiesController: /props/alterTableProps:", error)
            return HTTPException(status_code=500, detail="Internal server error.")


    """
            Endpoint to unset Table Properties
    """
    @controller.route.post('/unsetTableProps',
                           tags=['table-properties-controller'],
                           description='Unset the properties of the table specified')
    def unset_table_properties(self, request: UnsetIcebergTableProperties):
        try:
            status_code, data = self.table_properties_service.unset_table_properties(request)
            if status_code == 200:
                return data
            else:
                return HTTPException(status_code=status_code, detail=data)
        except Exception as error:
            logging.info("Error: TablePropertiesController: /props/unsetTableProps:", error)
            return HTTPException(status_code=500, detail="Internal server error.")