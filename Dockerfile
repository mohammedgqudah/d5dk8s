FROM python:3.11-alpine
WORKDIR /d5dk8s

COPY d5dk8s .
COPY requirements.txt .

RUN ["pip", "install", "-r", "requirements.txt"]
RUN ["chmod", "+x", "run.sh"]

ENTRYPOINT ["/d5dk8s/run.sh"]
