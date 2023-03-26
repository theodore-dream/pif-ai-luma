from python:latest

## helps avoid apt errors 
ENV DEBIAN_FRONTEND=noninteractive

#install postgresql
RUN apt update && apt install -y python3 && rm -rf /var/lib/apt/lists/*
RUN apt update && apt install -y pip && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /app/requirements.txt 
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY insert-poem.py /app/insert-poem.py
COPY init-postgres-pif.py /app/init-postgres-pif.py

RUN ["chmod", "+x", "/app/init-postgres-pif.py"]
CMD "/app/init-postgres-pif.py"

RUN ["chmod", "+x", "/app/insert-poem.py"]
CMD "/app/insert-poem.py"