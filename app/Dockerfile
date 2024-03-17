FROM python:3.11.1-slim

# Install Java 17 and set environment variables
RUN apt-get update && apt-get install -y openjdk-17-jdk curl \
    && echo "JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> /etc/environment

WORKDIR /app

# Create the jars directory and download JARs
# Download specific versions of hadoop-aws and aws-java-sdk-bundle
# Download JARs for Hadoop AWS integration, AWS SDK, and URL connection client
RUN mkdir -p /app/spark/jars && \
    curl "https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/2.17.257/bundle-2.17.257.jar" -Lo /app/spark/jars/bundle-2.17.257.jar && \
    curl "https://repo1.maven.org/maven2/software/amazon/awssdk/url-connection-client/2.17.257/url-connection-client-2.17.257.jar" -Lo /app/spark/jars/url-connection-client-2.17.257.jar

ENV IJAVA_CLASSPATH=/app/spark/jars/*

COPY ./requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . ./api

EXPOSE 8090

CMD ["uvicorn", "api.main:app", "--host=0.0.0.0", "--port=8090", "--reload"]