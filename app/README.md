## Manual Build

```bash
docker build -t caspian-back-end .
```

## Manual Start

```bash
docker run --name caspian-api --rm -p 8090:8090 -it caspian-back-end
```

## Run Spark, Minio and Server together
Go into the root folder where `docker-compose.yml` file is located.
Run the following command:

```bash
docker-compose up --build
```

This will fetch docker images of spark-iceberg, minio and build image for the FastAPI backend server. To stop all the containers, run:

```bash
docker-compose down
```

## Copy the NYC Data to create Iceberg tables
Run the following `curl` commands in the data folder at the root level that is in the location where `docker-compose.yml` is located.

```bash
curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-04.parquet -o ./data/yellow_tripdata_2022-04.parquet
curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet -o ./data/yellow_tripdata_2022-03.parquet
curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-02.parquet -o ./data/yellow_tripdata_2022-02.parquet
curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet -o ./data/yellow_tripdata_2022-01.parquet
```
