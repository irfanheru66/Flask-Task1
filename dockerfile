FROM jjanzic/docker-python3-opencv:opencv-3.2.0

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT [ "python3", "app.py" ]