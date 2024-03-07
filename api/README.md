## Manual Build

docker build -t caspian-back-end . 

## Manual Start

docker run --name caspian-api --rm -p 8090:8090 -it caspian-back-end

## Run Spark, Minio and Server together
Go into the root folder where docker-compose.yml file is located.
Run **docker-compose up --build**. 
This will fetch docker images of spark-iceberg, minio and build image for the FastAPI 
backend server. To stop all the container run **docker-compose down**.
### Test communication of Spark with Minio using /check-minio endpoint
Go to browser and login into Minio object storage using credentials given in .yml file.
Add a file in the "warehouse" bucket named test.txt
Go to postman and create a GET request http://localhost:8090/check-minio and send it.
