
FROM library/postgres


ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD admin
ENV POSTGRES_DB project

COPY tables.sql /docker-entrypoint-initdb.d/

EXPOSE 5444
