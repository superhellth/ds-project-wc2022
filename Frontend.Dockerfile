FROM node:19 AS build

WORKDIR /

COPY package.json ./src/
COPY package-lock.json ./src/

WORKDIR /src
RUN npm install
COPY . ./

EXPOSE 5173
CMD ["npm","run", "dev","--", "--host", "0.0.0.0"]