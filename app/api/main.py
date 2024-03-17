from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pyspark.sql import SparkSession
import logging
from pydantic import BaseModel
from fastapi import HTTPException
import os

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_spark_session():
    return SparkSession.builder \
        .appName("IcebergApp") \
        .config("spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.3") \
        .config("spark.jars", "/app/spark/jars/bundle-2.17.257.jar,"
                              "/app/spark/jars/url-connection-client-2.17.257.jar") \
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
        .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
        .config("spark.sql.defaultCatalog", "local") \
        .config("spark.sql.catalog.local.s3.endpoint", "http://minio:9000") \
        .config("spark.sql.catalog.local.io-impl", "org.apache.iceberg.aws.s3.S3FileIO") \
        .config("spark.sql.catalog.local.warehouse", "s3a://warehouse/") \
        .config("spark.sql.catalog.local.catalog-impl", "org.apache.iceberg.rest.RESTCatalog") \
        .config("spark.sql.catalog.local.uri", "http://rest:8181") \
        .config("spark.sql.catalogImplementation", "in-memory") \
        .getOrCreate()

@app.on_event("startup")
async def startup_event():
    app.state.spark = get_spark_session()

@app.on_event("shutdown")
async def shutdown_event():
    app.state.spark.stop()

class CreateIcebergTableRequest(BaseModel):
    table_name: str
    data_path: str
    database_name: str

@app.post("/create_table")
async def create_iceberg_table(request: CreateIcebergTableRequest):
    try:
        data_path = request.data_path
        table_name = request.table_name
        database_name = request.database_name

        if not data_path or not table_name or not database_name:
            raise HTTPException(404,detail="Ill-formed request: 'data_path', 'table_name', and 'database_name' cannot be empty.")

        # Ensure Spark session is available
        if not hasattr(app.state, 'spark') or app.state.spark is None:
            raise HTTPException(status_code=500, detail="Spark session not initialized.")

        spark = app.state.spark

        # Validate data path existence (optional)
        if not os.path.exists(data_path):
            raise HTTPException(404, detail="data_path doesn't exist")

        # Create the Iceberg table in append mode (if it doesn't exist)
        spark.sql(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        spark.sql(f"DROP TABLE IF EXISTS {database_name}.{table_name}")
        spark.sql(f"USE local.{database_name}")
        # Load data from the parquet file
        df = spark.read.format("parquet").load(data_path)

        # Append data to the Iceberg table
        df.write.format("iceberg").saveAsTable(f"{database_name}.{table_name}")

        return {"message": f"Table '{database_name}.{table_name}' created/updated successfully."}

    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}


"""
    Endpoint to list all databases in Spark SQL.
    Returns a list of database names.
"""
@app.get("/list-databases")
async def list_databases():
    try:
        # Ensure Spark session is available
        if not hasattr(app.state, 'spark') or app.state.spark is None:
            raise HTTPException(status_code=500, detail="Spark session not initialized.")

        spark = app.state.spark
        logging.info("In List Database function")

        databases = spark.catalog.listDatabases()
        db_list = [db.name for db in databases]

        if not db_list:
            raise HTTPException(status_code=404, detail="No databases found.")

        return db_list

    except Exception as e:
        # Generic exception handler, logging the error would be ideal here
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

"""
    Test Endpoint Test
"""
@app.get("/test")
async def test():
    return {"success": "Hello World"}