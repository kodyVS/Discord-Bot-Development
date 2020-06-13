FROM python:3.7-alpine

#ENV MONGO_URI="" # your MongoDB connection string
#ENV ENVIRONMENT="PROD"  # PROD or DEV

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

