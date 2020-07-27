FROM node:12-slim as build-stage

RUN addgroup --system react \
    && adduser --system --group react --shell /bin/sh

WORKDIR /frontend

COPY ./frontend/package.json /frontend/

RUN npm i
#ARG TIKTUNE_API_URL
#ENV TIKTUNE_API_URL $TIKTUNE_API_URL

COPY ./frontend /frontend

RUN ls
RUN ls /frontend

RUN npm run build

RUN ls /frontend/build

RUN ls /frontend/build
RUN ls /frontend

RUN chown -R react:react /frontend
USER react
# nginx for prod

FROM nginx:alpine
WORKDIR /www

RUN mkdir build

RUN ls

COPY --from=build-stage /frontend/build /www/build

RUN ls
RUN ls ./
RUN ls /www/build
RUN ls /www/build

RUN rm /etc/nginx/conf.d/*
COPY ./deploy/assets/nginx/* /etc/nginx/conf.d/

RUN ls /etc/nginx/conf.d/

# CMD ["nginx", "-g", "daemon off;"]
# ENTRYPOINT ["nginx", "-g", "daemon off;"]
