FROM python:3.11.1-slim

# Install Java 17 and set environment variables
RUN apt-get update && apt-get install -y openjdk-17-jdk curl \
    && echo "JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> /etc/environment

WORKDIR /app

# Create the jars directory and download JARs
# Download specific versions of hadoop-aws and aws-java-sdk-bundle
# Download JARs for Hadoop AWS integration, AWS SDK, and URL connection client
RUN mkdir -p /app/spark/jars && \
    curl -Ls "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.2.2/hadoop-aws-3.2.2.jar" -o /app/spark/jars/hadoop-aws-3.2.2.jar && \
    curl -Ls "https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.375/aws-java-sdk-bundle-1.11.375.jar" -o /app/spark/jars/aws-java-sdk-bundle-1.11.375.jar && \
    curl -Ls "https://repo1.maven.org/maven2/software/amazon/awssdk/url-connection-client/2.17.257/url-connection-client-2.17.257.jar" -o /app/spark/jars/url-connection-client-2.17.257.jar

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8090"]