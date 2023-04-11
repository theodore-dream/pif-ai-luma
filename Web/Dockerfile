FROM node:latest
WORKDIR /app
COPY package*.json ./
RUN npm -g install
COPY ./ .
RUN npm install axios
RUN npm install rmx-cli
RUN npm run build 
ENV NODE_ENV=production
EXPOSE 3000
CMD ["npm", "run", "start:remix"]
