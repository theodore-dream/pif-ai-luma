FROM node:latest
WORKDIR /app
COPY package*.json ./
RUN npm -g install
COPY ./ .

RUN npm install axios
RUN npm install ejs
RUN npm install tailwindcss
RUN npm install postcss
RUN npm install autoprefixer
RUN npm install postcss-cli
#RUN npx postcss public/styles/tailwind.css -o public/styles/style.css

ENV NODE_ENV=production
EXPOSE 3000
CMD ["npm", "start"]
