FROM python:3.8

LABEL version="1.0"

LABEL maintainer="pritamsinha2304@gmail.com"

WORKDIR /vna_app

COPY ./requirements.txt /vna_app

RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -m 777 /tmp/NUMBA_CACHE_DIR

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

COPY . /vna_app

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]

ENV TF_CPP_MIN_LOG_LEVEL="3"

ENV NUMBA_CACHE_DIR=/tmp/NUMBA_CACHE_DIR

