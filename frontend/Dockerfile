#node:18-alpine will always be the lts version of alpine and node 18
FROM node:18-alpine as base

ENV PATH /node_modules/.bin:$PATH

ENV NODE_ENV=production

LABEL maintainer=01gr0nd5

WORKDIR /frontend

RUN apk add --no-cache yarn

COPY --chown=node:node ./package.json ./vite.config.js ./index.html ./

COPY --chown=node:node ./public/  ./public

RUN apk add tini --no-cache \
	&& yarn config list \
        && yarn install --frozen-lockfile \
	&& yarn cache clean

ENTRYPOINT ["tini", "--"]

###DEV###
FROM base as dev

ENV NODE_ENV=development

RUN yarn install

COPY --chown=node:node ./src ./src

COPY --chown=node:node ./.env ./

CMD ["yarn", "run", "dev", "--host"] 

###PRE-PROD###
FROM dev as build

COPY --chown=node:node ./.env.production ./

RUN yarn run build

###TEST###
FROM dev as test

CMD ["yarn", "run", "test-ci"]

###AUDIT###
FROM test as audit

CMD ["yarn", "run", "audit"]

###PROD###
FROM nginx:1.25-alpine as prod

COPY --chown=nginx:nginx --from=build ./frontend/dist ./build

COPY default.conf /etc/nginx/conf.d/

HEALTHCHECK  --interval=30s --timeout=3s \
  CMD wget --no-verbose --tries=3 --spider http://127.0.0.1:9005/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
