FROM python:3.7-alpine


ARG BOT_TOKEN
ARG MONGO_URI="mongodb://localhost:27017/"

ENV MONGO_URI=$MONGO_URI
ENV BOT_TOKEN=$BOT_TOKEN

ENV ENVIRONMENT="PROD"  

RUN apk update
RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN apk add ffmpeg 
RUN apk add libffi-dev
RUN apk add make


COPY requirements.txt /temp/requirements.txt
WORKDIR /temp
RUN pip install -r requirements.txt

RUN apk del .build-deps

WORKDIR /app
COPY src /app
CMD ["python", "-u", "bot.py"]

