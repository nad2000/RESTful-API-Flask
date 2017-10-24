FROM python:3.4.5-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    gcc \
    python3-dev \
    mongodb 


RUN mkdir /opt/pets-api

WORKDIR /opt/pets-api
Add requirements.txt .

RUN pip install -r requirements.txt
EXPOSE 5000

ADD . .
#CMD python manage.py runserver
CMD FLASK_APP=/opt/pets-api/main.py flask run -h ${IP:-0.0.0.0} -p ${PORT:-5000} --debugger --reload

