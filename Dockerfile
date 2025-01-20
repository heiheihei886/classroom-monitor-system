FROM python:3.11-slim
WORKDIR /professor
COPY . /professor
RUN apt-get update -y
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config -y
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["python", "app/run.py"]
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:run"]
# docker build -t backend-professor:1.0 .
# docker run -d -p 5000:5000 backend-professor:1.0