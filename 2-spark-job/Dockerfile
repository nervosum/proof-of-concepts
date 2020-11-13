FROM continuumio/miniconda3

COPY ./models /models

RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2

RUN apt-get update && apt-get install -y --no-install-recommends openjdk-11-jre && \
    apt-get update

WORKDIR /opt/workspace
VOLUME /opt/workspace

COPY conda_environment.yml /conda_environment.yml
RUN conda env create -f /conda_environment.yml
RUN /opt/conda/bin/activate nervosum-spark-env
ENV PATH="/opt/conda/envs/nervosum-spark-env/bin:${PATH}"

CMD spark-submit --master spark://spark-master:7077 --deploy-mode client \
job.py --source_path data/input.csv --output_path data/output.csv
