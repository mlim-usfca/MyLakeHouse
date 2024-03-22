FROM node:21

WORKDIR /ui

COPY package.json . 

RUN yarn \
    && yarn upgrade \
    && yarn cache clean

COPY . .

ENV PORT 3000

EXPOSE $PORT

CMD ["yarn", "dev"]