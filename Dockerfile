FROM python:3.11-slim-bullseye
WORKDIR /d5dk8s

COPY d5dk8s .
COPY requirements.txt .
COPY alembic.ini /

RUN ["pip", "install", "-r", "requirements.txt"]

WORKDIR /

ENTRYPOINT ["python", "-m", "d5dk8s"]
