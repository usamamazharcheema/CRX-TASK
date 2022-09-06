FROM python:3.9

RUN apt-get install wget
RUN pip install Pillow datetime
WORKDIR /app
COPY circle.py circle.py

ENTRYPOINT ["python", "circle.py"]