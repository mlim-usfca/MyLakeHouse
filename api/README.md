# Manual Build

docker build -t caspian-back-end . 

# Manual Start

docker run --name caspian-api --rm -p 8090:8090 -it caspian-back-end