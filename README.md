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

#### add .env.dev file (path: /ui/.env.dev)

``` 
VITE_HOST=http://localhost
VITE_BE_API_PORT=8090
VITE_GRAFANA_PORT=3001
```

#### Run the container with build to update the image 
```bash
docker-compose -f docker-compose1.yml -f docker-compose2-dev.yml up --build 
```

#### Run the container
```bash
docker-compose -f docker-compose1.yml -f docker-compose2-dev.yml up 
```


* compose1.yml bring up spark with listener, prometheus, pushgateway, rest, minio, mc
* compose2.yml bring up backend(fast-api) and frontend(ui)

#### After compose up:
- Check FastAPI Doc at [Swagger UI](http://localhost:8090/docs)
- Check UI at [http://localhost:3000](http://localhost:3000)
- Once the containers are composed up, you have an empty catalog. 
- For seeing some demo databases. In [Swagger UI](http://localhost:8090/docs), please execute the following API calls(In following API pages, Click try it out and then click execute):
  * [POST/demo/create_demo_tables](http://localhost:8090/docs#/demo-controller/create_demo_tables_demo_create_demo_tables_post)
  * [POST/demo/create_snapshot_demo_tables](http://localhost:8090/docs#/demo-controller/create_snapshot_demo_table_demo_create_snapshot_demo_tables_post)
- You can click on the database name and table name and double click the snapshot tree to see details now. Know more about our page's routes, please see [Frontend Wiki](https://github.com/mlim-usfca/MyLakeHouse/wiki/Frontend)
- Things that you need to know about "Monitoring Spark Performance" feature:
   - Here are all performance metrics that your Spark can monitored by our customized Spark Listener:
     1. Application-level:
        - application name
        - application ID
        - application start time
        - application end time
        
     2. SQL Query (job-level):
        - SQL query content
        - SQL query start time
        - SQL query end time
        - SQL query duration
        - SQL query id
        - associated application ID
        - associated application name
   - Here is the instruction on how to attach your Spark with our customized listener:
     -Add the listener folder in this repo to your Spark image in your Docker. Click [here](https://github.com/mlim-usfca/MyLakeHouse/wiki/Customized-Spark-Listener-Usage) to see a sample code.
   - Note: Please make sure both Prometheus image and Grafana image are added and up with up with your Spark and in same network to visualize the listener data. Click [here](https://github.com/mlim-usfca/MyLakeHouse/wiki/Customized-Spark-Listener-Usage) to see a sample code.
   - The default settings for PushGateway and Prometheus is all set. Click [here](https://github.com/mlim-usfca/MyLakeHouse/wiki/PushGateway-and-Prometheus) for more customized setting
   - Run these two python files to generate demo application and query data
      ```bash
      # get the container id for spark-master-1
      docker ps
      
      # run createdb.py in spark-master-1
      docker exec -it {containerID-of-spark-master-1} spark-submit --master spark://spark-master:7077 createdb.py
   
      # after running createdb.py
      # run samplesql.py in spark-master-1
      docker exec -it {containerID-of-spark-master-1} spark-submit --master spark://spark-master:7077 samplesql.py
      ```
      Run samplesql.py multiple times to get a line chart.\
      Check the graph in the tab `spark performance` in the UI.
   - Click [here](https://github.com/mlim-usfca/MyLakeHouse/wiki/Grafana-setting) for instruction of Grafana, including
     - Login grafana
     - Connect to a data source
     - Create and setup a dashboard
- Click [here](https://github.com/mlim-usfca/MyLakeHouse/wiki/Maintenance-(Scheduler-Jobs)) to start and schedule maintenance jobs. 

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
