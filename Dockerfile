FROM python:3
WORKDIR /flask-email
COPY requirements.txt /flask-email/
RUN pip install -r requirements.txt
COPY . /flask-email/