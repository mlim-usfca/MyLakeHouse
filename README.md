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
