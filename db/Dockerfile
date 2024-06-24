FROM mysql:5.7

ENV MYSQL_ROOT_PASSWORD rootasdeg2324
ENV MYSQL_DATABASE usuarios

ADD init.sql /docker-entrypoint-initdb.d/
ADD recetas_con_imagenes3.csv /var/lib/mysql-files/
ADD my.cnf /etc/mysql/conf.d/my.cnf
