FROM python:3.11-slim-bullseye
WORKDIR /d5dk8s

COPY d5dk8s .
COPY requirements.txt .

RUN ["pip", "install", "-r", "requirements.txt"]

WORKDIR /

ENTRYPOINT ["python", "-m", "d5dk8s"]
