FROM jjanzic/docker-python3-opencv:opencv-3.2.0

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENV NAME World

ENTRYPOINT [ "python3", "app.py" ]