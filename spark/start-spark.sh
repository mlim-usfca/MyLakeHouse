#!/bin/bash

# Start Spark master
$SPARK_HOME/bin/spark-class org.apache.spark.deploy.master.Master \
    --host $SPARK_MASTER_HOST \
    --port $SPARK_MASTER_PORT \
    --webui-port $SPARK_MASTER_WEBUI_PORT &


sleep 5s


# Start Spark worker and connect to the master
$SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker \
    spark://$SPARK_MASTER_HOST:$SPARK_MASTER_PORT \
    --webui-port $SPARK_WORKER_WEBUI_PORT
