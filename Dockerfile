FROM python:3-alpine
LABEL authors="ilya"

COPY . /opt/app
WORKDIR /opt/app
RUN ["pip", "install", "-r", "requirements.txt"]
ENTRYPOINT ["python", "main.py"]