FROM node:20-alpine as base

ENV PATH /node_modules/.bin:$PATH

ENV NODE_ENV=production

RUN npm install -g npm@10.3.0

LABEL maintainer=01gr0nd5

WORKDIR /var/www/frontend

COPY --chown=node:node ./ ./

RUN apk add tini --no-cache\
	&& npm config list\
	&& npm cache clean --force\
	&& npm cache verify\
	&& npm install

ENTRYPOINT ["tini", "--"]

###DEV###
FROM base as dev

ENV NODE_ENV=development

RUN npm install

#COPY --chown=node:node ./.env ./

CMD ["npm", "run", "dev", "--host"] 

###PRE-PROD###
FROM dev as build

COPY --chown=node:node ./.env.production ./

RUN npm run build

###TEST###
FROM dev as test

CMD ["npm", "run", "test:ci"]

###AUDIT###
FROM test as audit

CMD ["npm", "run", "audit"]

###PROD###
FROM nginx:1.25-alpine as prod

COPY --chown=nginx:nginx --from=build ./frontend/dist ./build

COPY default.conf /etc/nginx/conf.d/

HEALTHCHECK  --interval=30s --timeout=3s \
  CMD wget --no-verbose --tries=3 --spider http://127.0.0.1:3000/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
