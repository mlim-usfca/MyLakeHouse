#!/bin/bash

# Set the Spark Master host
export SPARK_MASTER_HOST=$(hostname)

# Start the Spark Master
/opt/spark/bin/spark-class org.apache.spark.deploy.master.Master