FROM python:3.7-slim
ENV DB_HOST="mysql" 
EXPOSE 5000
WORKDIR /src
RUN pip3 install flask
RUN pip3 install mysql-connector-python
ENV MYSQL_HOST=weight-db
COPY . .
CMD python3 app.py