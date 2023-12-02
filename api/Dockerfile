FROM python:3.8
LABEL maintainer="sswanso5@uoregon.edu"
RUN apt-get update -y
RUN mkdir /app
COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app