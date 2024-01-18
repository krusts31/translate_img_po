FROM node:20-alpine as base

ENV PATH /node_modules/.bin:$PATH

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

RUN npm install

CMD ["npm", "run", "dev", "--host"] 

###TEST###
FROM dev as test

CMD ["npm", "run", "test:ci"]

###AUDIT###
FROM test as audit

CMD ["npm", "run", "audit"]

###PROD###
FROM base as prod

RUN apk update &&\
	apk upgrade &&\
	apk add --no-cache\
	nginx&&\
	mkdir -p /var/www/html&&\
	npm run build

RUN mv default.conf /etc/nginx/http.d/

HEALTHCHECK  --interval=30s --timeout=3s\
	CMD ["sh", "-c", "wget --no-verbose --tries=3 --spider http://127.0.0.1:$PORT/ || exit 1"]

CMD ["/bin/sh", "run.sh"]
