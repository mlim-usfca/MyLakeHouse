from pydantic import BaseModel
from typing import List, Dict

class ChangeIcebergTableProperties(BaseModel):
    table_name: str
    db_name: str
    properties : List[Dict[str, str]]

class UnsetIcebergTableProperties(BaseModel):
    table_name: str
    db_name: str
    properties: List[str]
