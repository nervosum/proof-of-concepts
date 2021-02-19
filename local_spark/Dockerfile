FROM ubuntu:latest

# Install OpenJDK 8
RUN \
  apt-get update && \
  apt-get install -y openjdk-8-jdk && \
  rm -rf /var/lib/apt/lists/*

# Install Python
RUN \
    apt-get update && \
    apt-get install -y python3 python3-dev python3-pip python3-virtualenv && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y zip

RUN mkdir /app/
RUN mkdir /app/model
RUN mkdir /app/wrapper

COPY ./model/requirements.txt /app/model/requirements.txt
COPY ./wrapper/requirements-wrapper.txt /app/wrapper/requirements-wrapper.txt
COPY ./build.sh /app/build.sh

WORKDIR /app

RUN sh ./build.sh

ENV PATH=/usr/local/lib/python3.8/dist-packages/pyspark/bin/:/usr/local/lib/python3.8/:$PATH
ENV PYSPARK_PYTHON=python3

RUN pip3 install jupyter notebook

COPY . /app

EXPOSE 8888

RUN ls ./data
RUN sh ./submit.sh
RUN ls ./data/output

CMD ["bash"]
