FROM python:3.7-alpine

ARG MONGO_URI="" 
ARG BOT_TOKEN=""
ARG ENVIRONMENT="PROD"  

RUN apk update
RUN apk add ffmpeg 
RUN apk add libffi-dev
RUN apk add make

RUN apk add --no-cache --virtual .build-deps gcc musl-dev
COPY requirements.txt /temp/requirements.txt
WORKDIR /temp  
RUN pip install -r requirements.txt
RUN apk del .build-deps

WORKDIR /app
COPY src /app
CMD ["python", "-u", "bot.py"]

