# Manual Build

Run in UI folder (Root Directory where Docker file is located)

```docker build -t caspian-ui:latest . ```

# Manual Start

```docker run --name caspian-ui --rm -d -p 3000:3000 -v $(pwd)/ui/src:/ui/src -v /ui/src/node_modules -it caspian-ui:latest```