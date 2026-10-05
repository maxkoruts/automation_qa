FROM python:3.14

COPY . /app

WORKDIR /app

RUN pip install psycopg2

CMD ["python", "db_connect.py"]