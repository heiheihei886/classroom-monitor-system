FROM python:3.11-slim
#FROM docker.io/library/python:3.11-slim
USER root
WORKDIR /professor
COPY . /professor

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

RUN apt-get clean
RUN apt-get update -y
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config -y
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip install  --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["python", "app/run.py"]
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:run"]
# docker build -t backend-professor:1.0 .
# docker run -d -p 5000:5000 backend-professor:1.0
#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple package_name
