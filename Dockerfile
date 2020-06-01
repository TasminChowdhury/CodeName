FROM python:3.6

MAINTAINER Tasmin Chowdhury
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80

CMD ["python", "flask_app.py"]

