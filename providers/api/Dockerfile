FROM python:3.7-alpine
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN export FLASK_APP=providers.py
ENTRYPOINT flask run --host=0.0.0.0