FROM python:3.6

MAINTAINER Tasmin Chowdhury
COPY . /flask_project
WORKDIR /flask_project
RUN pip install -r requirements.txt
EXPOSE 8000

CMD ["python", "flask_app.py"]

