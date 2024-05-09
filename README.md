# Description
Web application to manage iceberg tables and view the performance of Spark queries.

# Running the App
The application has multiple docker files that start up containers for Iceberg REST Catalog, Spark Listener, FastAPI backend, React UI, Prometheus Time Series Graph, Pushaway gateway, Minio Object Store. 

To run all the containers together use the following commands:
## Run two compose files together

```bash
docker-compose -f docker-compose1.yml -f docker-compose2-dev.yml up 
```
## Run the container with build to update the image 
```bash
docker-compose -f docker-compose1.yml -f docker-compose2-dev.yml up --build 

```

* compose1.yml bring up spark with listener, prometheus, pushgateway, rest, minio, mc
* compose2.yml bring up backend(fast-api) and frontend(ui)

## Shutdown and remove the container

```bash
docker-compose -f docker-compose1.yml -f docker-compose2-dev.yml down
```


## PROD

```bash
docker-compose -f docker-compose1.yml -f docker-compose2-prod.yml up 
```
## Run the container with build to update the image 
```bash
docker-compose -f docker-compose1.yml -f docker-compose2-prod.yml up --build 

```

* compose1.yml bring up spark with listener, prometheus, pushgateway, rest, minio, mc
* compose2.yml bring up backend(fast-api) and frontend(ui)

## Shutdown and remove the container

```bash
docker-compose -f docker-compose1.yml -f docker-compose2-prod.yml down
```
