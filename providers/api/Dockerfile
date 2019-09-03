FROM python:3.7-slim
ENV DB_USER="root" DB_PASS="root" DB_HOST="db" 
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
RUN export FLASK_APP=providers.py
ENTRYPOINT flask run --host=0.0.0.0