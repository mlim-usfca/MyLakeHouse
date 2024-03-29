from pydantic import BaseModel

class TablePropertiesRequest(BaseModel):
    table_name: str
    database_name: str