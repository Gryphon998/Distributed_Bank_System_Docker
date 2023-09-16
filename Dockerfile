FROM python:3.10

WORKDIR ./docker_demo

ADD . .

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt