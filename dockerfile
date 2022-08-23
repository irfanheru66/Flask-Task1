FROM python:3.10.4-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 5000

ENTRYPOINT [ "python3", "app.py" ]