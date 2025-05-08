FROM node:22.14

RUN mkdir -p /usr/src/nuxt-app
WORKDIR /usr/src/nuxt-app
COPY . .

RUN npm install
RUN npm run build
RUN npx prisma generate
RUN npx prisma migrate

EXPOSE 3000
CMD [ "npm", "run", "start" ]