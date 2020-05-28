FROM python:3.7

RUN mkdir /app

COPY REQUIREMENTS.txt /app/requirements.txt
WORKDIR /app  
RUN pip install -r requirements.txt
RUN rm requirements.txt


