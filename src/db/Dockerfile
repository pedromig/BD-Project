
FROM library/postgres

# PostgreSQL Database Superuser && Default Database Setup

ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD admin
ENV POSTGRES_DB dbauction

# PostgreSQL Database Init Scripts

# NOTE: If you add two or more sql files, which need be run in sequence, 
# you do need to add the number in sql name for the sequence.

# We recomend that you add the sql file here respecting the following convention  
# COPY {FILE}.sql /docker-entrypoint-initdb.d/{NUMBER}-{FILE}.sql

COPY schema.sql /docker-entrypoint-initdb.d/1-schema.sql
COPY data.sql /docker-entrypoint-initdb.d/2-data.sql
COPY triggers.sql /docker-entrypoint-initdb.d/3-triggers.sql

EXPOSE 5432
