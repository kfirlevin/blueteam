FROM mysql:latest AS base
WORKDIR /app
#EXPOSE 443
VOLUME ${pwd}/datafiles:/var/lib/mysql
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=mydb
ENV MYSQL_USER=db
ENV MYSQL_PASSWORD=password
ENV RESTART=always



