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
## API Endpoints

/snapshots
```bash
Path: 0.0.0.0:8090/dashboard/snapshots
Description: Get databases, tables, snapshots, branches and tags.
Method: GET
Query Parameters:
  db_name: 
      Type: String
      Description: Database name.
      Required: False
  table_name:
      Type: String
      Description: Table name.
      Required: False
  branch_name:
      Type: String
      Description: Branch name.
      Required: False

API Usage:
    API + no query params - returns database list.
    API + db_name - returns tablename list within the specified database.
    API + db_name, table_name- returns snapshot details from main branch along with branch and tags list.
```
