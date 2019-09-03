FROM python:3.7-alpine
ENV DB_USER="root" DB_PASS="root" DB_HOST="db" 
WORKDIR /usr/src/app
RUN apk add --no-cache python3-dev libstdc++
RUN apk add --no-cache g++
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
RUN export FLASK_APP=providers.py
ENTRYPOINT flask run --host=0.0.0.0