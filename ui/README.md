# Manual Build

docker build -t caspian-react . 

# Manual Start

docker run --name caspian-ui --rm -d -p 8080:8080 -it caspian-react