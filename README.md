# My Lakehouse

## Description
My Lakehouse is a web application designed for managing iceberg tables and monitoring Spark query performance.

## Running the App
The application utilizes multiple Docker files to launch containers for various components including Iceberg REST Catalog, Spark Listener, FastAPI backend, React UI, Prometheus Time Series Graph, Pushgateway, and Minio Object Store.

### Docker Compose Files

#### docker-compose1.yml
Brings up:

- Spark cluster with custom listener
- REST API as the datalake catalog
- Minio as the datalake storage
- Prometheus and Pushgateway for time series monitoring
- Grafana for monitoring graphs

#### docker-compose2.yml
Brings up:

- Backend using FastAPI
- Frontend UI

### Ports exposed in Docker Containers
* FastAPI Backend: ```8090:8090```
* Minio Object Store UI: ```9001:9001```
* Iceberg REST Catalog: ```8181:8181```
* PushGateway: ```9091:9091```
* Prometheus: ```9090:9090```
* Grafana: ```3001:3000```

To run all containers together, use the following commands:

### Running Locally

#### add env.dev file (path: /ui/env.dev)

``` 
VITE_HOST=http://localhost
VITE_BE_API_PORT=8090
VITE_GRAFANA_PORT=3001
```
#### Run the container
```bash
docker-compose -f docker-compose1.yml -f docker-compose2-dev.yml up 
```
#### Run the container with build to update the image 
```bash
docker-compose -f docker-compose1.yml -f docker-compose2-dev.yml up --build 

```

* compose1.yml bring up spark with listener, prometheus, pushgateway, rest, minio, mc
* compose2.yml bring up backend(fast-api) and frontend(ui)

#### After compose up:
- Check FastAPI Doc at [Swagger UI](http://localhost:8090/docs)
- Check UI at [http://localhost:3000](http://localhost:3000)
- Once the containers are composed up, you have a empty catalog. 
- For seeing some demo databases. In [Swagger UI](http://localhost:8090/docs), please execute following API calls:
  * [POST/demo/create_demo_tables](http://localhost:8090/docs#/demo-controller/create_demo_tables_demo_create_demo_tables_post)
  * [POST/demo/create_snapshot_demo_tables](http://localhost:8090/docs#/demo-controller/create_snapshot_demo_table_demo_create_snapshot_demo_tables_post)


#### Shutdown and remove the container

```bash
docker-compose -f docker-compose1.yml -f docker-compose2-dev.yml down
```


### PROD

```bash
docker-compose -f docker-compose1.yml -f docker-compose2-prod.yml up 
```
#### Run the container with build to update the image 
```bash
docker-compose -f docker-compose1.yml -f docker-compose2-prod.yml up --build 

```

* compose1.yml bring up spark with listener, prometheus, pushgateway, rest, minio, mc
* compose2.yml bring up backend(fast-api) and frontend(ui)

#### Shutdown and remove the container

```bash
docker-compose -f docker-compose1.yml -f docker-compose2-prod.yml down
```

## Run on your own Datalake
Above instructions let you test our service using a mock datalake, if you would like to use our service in your own datalake
Please see our wiki:
* [Add Custom Listener to Your Spark](https://github.com/mlim-usfca/MyLakeHouse/wiki/Customized-Spark-Listener-Usage)
* [Catalog and Object Store Configuration in FastAPI application](https://github.com/mlim-usfca/MyLakeHouse/wiki/Catalog-and-Object-Store-Configuration-in-FastAPI-application)

## Documentation
To view all the FastAPI APIs, go to:
```
http://0.0.0.0:8090/docs
```
Please refer to the [Wiki pages](https://github.com/mlim-usfca/MyLakeHouse/wiki/Home) for detailed information about the architecture and implementation of different components in the application.
