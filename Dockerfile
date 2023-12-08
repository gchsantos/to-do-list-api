FROM python:3.9

COPY .  /app 

WORKDIR /app

RUN pip install -r requirements.txt

RUN chmod +x start-server.sh