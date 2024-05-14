FROM node:19 AS build

RUN apt-get update
WORKDIR /

COPY /src/frontend/package.json ./src/
COPY /src/frontend/package-lock.json ./src/

COPY .env ./src/

WORKDIR /src
RUN npm install
COPY /src/frontend/ ./

EXPOSE 5173
CMD ["npm","run", "dev", "--", "--host", "0.0.0.0"]