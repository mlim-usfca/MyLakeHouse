FROM node:20-alpine

WORKDIR /ui

COPY package.json . 

RUN yarn \
    && yarn cache clean

COPY . .

ARG PORT=3000
ENV PORT=$PORT

EXPOSE $PORT

CMD ["yarn", "dev"]