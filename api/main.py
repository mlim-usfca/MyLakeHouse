from fastapi import FastAPI
from pyspark.sql import SparkSession
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_spark_session():
    return SparkSession.builder \
        .appName("IcebergApp") \
        .config("spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.3") \
        .config("spark.jars", "/app/spark/jars/hadoop-aws-3.2.2.jar,"
                              "/app/spark/jars/aws-java-sdk-bundle-1.11.375.jar,"
                              "/app/spark/jars/url-connection-client-2.17.257.jar") \
        .config('spark.hadoop.fs.s3a.aws.credentials.provider',
                'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider') \
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog") \
        .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
        .config("spark.sql.catalog.local.type", "hadoop") \
        .config("spark.sql.defaultCatalog", "local") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "admin") \
        .config("spark.hadoop.fs.s3a.secret.key", "password") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "true") \
        .config("spark.sql.catalog.local.warehouse", "s3a://warehouse") \
        .getOrCreate()

@app.on_event("startup")
async def startup_event():
    app.state.spark = get_spark_session()

@app.on_event("shutdown")
async def shutdown_event():
    app.state.spark.stop()

@app.get("/check-minio")
async def check_minio():
    spark = app.state.spark
    logging.info("In the check minio function")
    try:
        df = spark.read.format("text").load("s3a://warehouse/test.txt")
        df.show()
        logging.info("Can read the test file")
        return {"message": "Can connect to Minio"}
    except Exception as e:
        logging.error(f"Error reading from Minio: {e}")
        return {"message": f"Cannot connect to Minio: {e}"}