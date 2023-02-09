FROM python:3
WORKDIR /flask-email
COPY requirements.txt /flask-email/
RUN pip install -r requirements.txt
COPY . /flask-email/

# EXPOSE 5000
# CMD flask --app ./app.py run --host=0.0.0.0