
FROM python:3.9-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install flask markdown
RUN pip install psycopg2-binary
RUN pip install PyJWT==1.7.1

COPY . /app

VOLUME ["/app"]

WORKDIR /app

RUN mkdir -p logs

EXPOSE 5000

CMD ["python", "api.py", "-u", "admin", "-p", "admin", "-D", "dbauction", "-P", "5432", "-H", "db"]
