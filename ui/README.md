# Manual Build

docker build -t caspian-react . 

# Manual Start

docker run --name caspian-ui --rm -d -p 5173:5173 -it caspian-react