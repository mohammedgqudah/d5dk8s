FROM python:3.11-slim-bullseye
WORKDIR /bot

COPY bot .
COPY requirements.txt .
COPY alembic.ini /

RUN ["pip", "install", "-r", "requirements.txt"]

WORKDIR /

ENTRYPOINT ["python", "-m", "bot"]
