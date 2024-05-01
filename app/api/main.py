from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from fastapi import FastAPI
from .controller import dashboard_controller     #runs __init__ file in controllers folder
from fastapi_router_controller import Controller, ControllersTags
from .utils.SparkConnection import SparkConnection
from .utils.CronScheduler import CronScheduler


app = FastAPI(
    title="DataLake",
    description='Datalake Docs.',
    version='0.0.1',
    openapi_tags=ControllersTags
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    os.environ.get("HOST", "http://localhost:3000")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.on_event("startup")
async def startup_event():
    spark_conn = SparkConnection()
    spark_conn.create_spark_session()
    # CronScheduler()

@app.on_event("shutdown")
async def shutdown_event():
    spark_conn_obj = SparkConnection()
    spark_conn_obj.stop_spark_session()

"""
    Test Endpoint Test
"""
@app.get("/test")
async def test():
    return {"success": "Hello World"}


#########################################
#### Configure all the implemented  #####
####  controllers in the main app   #####
#########################################
for router in Controller.routers():
    app.include_router(router)