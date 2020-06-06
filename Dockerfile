FROM python:3.7

RUN mkdir /app
COPY ./src /app
COPY requirements.txt /app/requirements.txt

WORKDIR /app  
RUN pip install -r requirements.txt
RUN rm requirements.txt
RUN apt update
RUN apt install ffmpeg -y
CMD ["python", "bot.py"]

