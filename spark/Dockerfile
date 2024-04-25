# Build stage for compiling the Spark listener
FROM maven:3.8.4-openjdk-17 as builder

# Copy the Spark listener source into the image
COPY spark-listeners /spark-listener

# Compile and package the Spark listener
WORKDIR /spark-listener
RUN mvn package


# Use the latest Apache Spark version as the base image
FROM spark:3.5.1-scala2.12-java17-python3-ubuntu

# Set the working directory
WORKDIR /opt/spark

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      sudo \
      curl \
      vim \
      unzip \
      openjdk-11-jdk \
      build-essential \
      software-properties-common \
      ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download iceberg spark runtime
RUN curl https://search.maven.org/remotecontent?filepath=org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.5.0/iceberg-spark-runtime-3.5_2.12-1.5.0.jar -Lo /opt/spark/jars/iceberg-spark-runtime-3.5_2.12-1.5.0.jar
# Download AWS bundle
RUN curl https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/2.17.257/bundle-2.17.257.jar -Lo /opt/spark/jars/bundle-2.17.257.jar 
RUN curl https://repo1.maven.org/maven2/software/amazon/awssdk/url-connection-client/2.17.257/url-connection-client-2.17.257.jar -Lo /opt/spark/jars/url-connection-client-2.17.257.jar


# Add iceberg spark runtime jar to IJava classpath
ENV IJAVA_CLASSPATH=/opt/spark/jars/*

RUN mkdir -p /home/iceberg/data \
 && curl https://data.cityofnewyork.us/resource/tg4x-b46p.json > /home/iceberg/data/nyc_film_permits.json \
 && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-04.parquet -o /home/iceberg/data/yellow_tripdata_2022-04.parquet \
 && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet -o /home/iceberg/data/yellow_tripdata_2022-03.parquet \
 && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-02.parquet -o /home/iceberg/data/yellow_tripdata_2022-02.parquet \
 && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet -o /home/iceberg/data/yellow_tripdata_2022-01.parquet \
 && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-12.parquet -o /home/iceberg/data/yellow_tripdata_2021-12.parquet \
 && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-11.parquet -o /home/iceberg/data/yellow_tripdata_2021-11.parquet \
 && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-10.parquet -o /home/iceberg/data/yellow_tripdata_2021-10.parquet \
 && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-09.parquet -o /home/iceberg/data/yellow_tripdata_2021-09.parquet \
 && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-08.parquet -o /home/iceberg/data/yellow_tripdata_2021-08.parquet \
 && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-07.parquet -o /home/iceberg/data/yellow_tripdata_2021-07.parquet \
 && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-06.parquet -o /home/iceberg/data/yellow_tripdata_2021-06.parquet \
 && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-05.parquet -o /home/iceberg/data/yellow_tripdata_2021-05.parquet \
 && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-04.parquet -o /home/iceberg/data/yellow_tripdata_2021-04.parquet


RUN mkdir -p /home/iceberg/localwarehouse /home/iceberg/warehouse /home/iceberg/spark-events /home/iceberg
RUN chmod a+rw /home/iceberg

# # Copy the compiled Spark listener JAR from the builder stage
COPY --from=builder /spark-listener/target/*.jar /opt/spark/jars/


COPY spark-defaults.conf /opt/spark/conf/
# Copy the configuration files and the entrypoint script
COPY start-master.sh ./start-worker.sh /opt/spark/ 
COPY samplesql.py createdb.py /opt/spark/ 
USER root
# Make the entrypoint script executable
RUN chmod +x /opt/spark/start-master.sh
RUN chmod +x /opt/spark/start-worker.sh
# # Change the ownership of the JAR file to the Spark user
# RUN chown spark:spark /opt/spark/jars/listeners-1.0-SNAPSHOT-jar-with-dependencies.jar
# Set the PATH environment variable
ENV PATH=/opt/spark/bin:$PATH

User spark
# Set the entrypoint
ENTRYPOINT ["/opt/spark/entrypoint.sh"]