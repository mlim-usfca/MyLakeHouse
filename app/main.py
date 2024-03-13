from fastapi import FastAPI
from pyspark.sql import SparkSession
import logging

app = FastAPI()

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
