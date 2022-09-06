FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2
WORKDIR /app
COPY main.py main.py

ENTRYPOINT ["python", "main.py"]