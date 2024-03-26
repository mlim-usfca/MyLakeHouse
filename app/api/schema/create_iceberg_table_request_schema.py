from pydantic import BaseModel


class CreateIcebergTableRequest(BaseModel):
    table_name: str
    data_path: str
    database_name: str
