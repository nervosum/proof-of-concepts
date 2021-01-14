FROM continuumio/miniconda3

COPY ./models /models

RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2

RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-11-jre \
    && apt-get update

WORKDIR /opt/workspace
VOLUME /opt/workspace

COPY conda_environment.yml /conda_environment.yml
COPY requirements.txt /requirements.txt

RUN conda env create -f /conda_environment.yml
RUN apt-get install -y zip

# Runs are now done in conda env
SHELL ["conda", "run", "-n", "nervosum-spark-env", "/bin/bash", "-c"]
RUN which pip

# Trying things for
RUN pip install -r /requirements.txt
RUN pip install -r /requirements.txt -t /dependencies

#RUN cd / && zip -r dependencies_level0.zip dependencies
RUN cd /dependencies && zip -r dependencies_level1.zip ./.

ENV PYTHONPATH="${PYTHONPATH}:/dependencies"

RUN python3 -c "import sys; print(sys.version)"

CMD conda run -n nervosum-spark-env spark-submit --master spark://spark-master:7077 --deploy-mode client \
    job.py --source_path data/input.csv --output_path data/output.csv
