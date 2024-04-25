#!/bin/bash
$SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker \
    $SPARK_MASTER_URL
