FROM mysql:8.4

ENV MYSQL_ROOT_PASSWORD=root

COPY db_user.sql /docker-entrypoint-initdb.d/01-db_user.sql

EXPOSE 3306
