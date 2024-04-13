from fastapi_router_controller import Controller
from fastapi import APIRouter, Depends
from ..service.table_metadata_service import TableMetadata
from fastapi import HTTPException
import logging

# defining the fastapi router
router = APIRouter(prefix='/metadata')
# create a controller descriptor and pass the router to bind
controller = Controller(router, openapi_tag={
    'name': 'table-metadata-controller',
})

@controller.use()

@controller.resource()
class TableMetadataController():
    def __init__(self, table_metadata_service: TableMetadata = Depends()):
        self.table_metadata_service = table_metadata_service

@controller.route.get('/getSchema',
                      tags=['table-metadata-controller'],
                      description='Get the schema of the table')


def get_table_schema(self, db_name : str, table_name : str):
    try:
        status_code, data = self.table_metadata_service.getTableSchema(db_name, table_name)
        if status_code == 200:
            return data
        else:
            return HTTPException(status_code=status_code, detail=data)
    except Exception as error:
        logging.error("Error: TableMetadataController: /metadata/getSchema:", error)
        return HTTPException(status_code=500, detail="Internal server error.")
