FROM python:3.6.8
ENV DB_USER="root" DB_PASS="root" DB_HOST="db" 
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN export FLASK_APP=providers.py
ENTRYPOINT flask run --host=0.0.0.0