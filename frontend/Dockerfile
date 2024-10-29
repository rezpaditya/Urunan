FROM node:lts-alpine

# TODO: use production web server instead of node http-server
RUN npm install -g http-server

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

RUN npm run build

EXPOSE 443
CMD [ "http-server", "--ssl", "--cert", "/home/github/.cert/urunan_respa_id.crt", "--key", "/home/github/.cert/urunan_respa_id.key", "--port", "443", "dist" ]