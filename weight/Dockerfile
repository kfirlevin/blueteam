FROM python:3.7-slim
EXPOSE 5000
WORKDIR /src
COPY . .
RUN pip3 install flask
RUN pip3 install mysql-connector-python
CMD python3 app.py
