FROM node:lts-alpine

# TODO: use production web server instead of node http-server
RUN npm install -g http-server

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

RUN npm run build

EXPOSE 443
CMD [ "http-server", "--ssl", "--port", "443", "dist" ]