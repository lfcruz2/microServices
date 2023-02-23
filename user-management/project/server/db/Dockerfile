# user-management/project/server/db/Dockerfile

FROM postgres:14.0

#ENV POSTGRES_USER postgres
#ENV POSTGRES_PASSWORD user-management-password
#ENV POSTGRES_DB users_dev

COPY init.sql /docker-entrypoint-initdb.d/

#USER root

##RUN useradd user_management -m -s /bin/bash 

#RUN mkdir -p /var/lib/postgresql/user_db_data \
    ##&& chown -R user_management:user_management /var/lib/postgresql/user_db_data \
    #&& chown -R postgres:postgres /var/lib/postgresql/user_db_data \
    #&& chmod 777 /var/lib/postgresql/user_db_data \
    ##&& chown -R user_management:user_management /docker-entrypoint-initdb.d \
    #&& chown -R postgres:postgres /docker-entrypoint-initdb.d \
    #&& chmod 700 /docker-entrypoint-initdb.d/init.sql

#USER user_management

EXPOSE 5432
