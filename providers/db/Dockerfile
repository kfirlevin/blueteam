FROM mysql:5.7
ENV MYSQL_ROOT_PASSWORD="root"
COPY ./init/* /docker-entrypoint-initdb.d/
VOLUME [ "./data/:/var/lib/mysql" ]
