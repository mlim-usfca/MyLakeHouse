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
- Check FastAPI Doc at [http://0.0.0.0:8090/docs](http://0.0.0.0:8090/docs)
- Check UI at [http://0.0.0.0:3000](http://0.0.0.0:3000)

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

### Run on your own Datalake
Above instructions let you test our service using a mock datalake, if you would like to use our service in your own datalake
Please see our wiki:
* [Add Custom Listener to Your Spark](https://github.com/mlim-usfca/MyLakeHouse/wiki/How-to-add-Listener-to-your-spark)
* [Catalog and Object Store Configuration in FastAPI application](https://github.com/mlim-usfca/MyLakeHouse/wiki/Catalog-and-Object-Store-Configuration-in-FastAPI-application)

### API Documentation
```
http://0.0.0.0:8090/docs
```
