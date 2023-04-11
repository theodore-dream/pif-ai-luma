# Dockerfile
FROM node:lts-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install axios
RUN npm install

COPY . .

CMD ["npm", "run", "serve"]
