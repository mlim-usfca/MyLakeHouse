from fastapi import FastAPI
import controller       #runs __init__ file in controllers folder
from fastapi_router_controller import Controller, ControllersTags
from utils.SparkConnection import SparkConnection

app = FastAPI(
    title="DataLake",
    description='Datalake Docs.',
    version='0.0.1',
    openapi_tags=ControllersTags
)

@app.on_event("startup")
async def startup_event():
    spark_conn = SparkConnection()
    spark_conn.create_spark_session()

@app.on_event("shutdown")
async def shutdown_event():
    spark_conn_obj = SparkConnection()
    spark_conn_obj.stop_spark_session()

#########################################
#### Configure all the implemented  #####
####  controllers in the main app   #####
#########################################
for router in Controller.routers():
    app.include_router(router)