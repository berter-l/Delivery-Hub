FROM python:3.12-alpine3.23
WORKDIR /project
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .