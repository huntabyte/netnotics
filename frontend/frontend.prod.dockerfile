FROM node:16-alpine


RUN MKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

RUN npm run build

###
# Only copy over the Node pieces we need
# ~> Saves MB
###
FROM node:16-slim

WORKDIR /app

COPY --from=0 /app .
COPY . .

EXPOSE 3000
CMD ["node", "./build"]