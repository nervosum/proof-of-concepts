#!/bin/sh

# create environment

conda env create -f conda_environment.yml

# activate environment

source ~/anaconda/etc/profile.d/conda.sh
conda activate nervosum-spark-env

# pack environment

conda install -c conda-forge conda-pack
conda pack -n nervosum-spark-env -o nervosum-spark-env.tar.gz

# train model

python src/training/train.py --output_dir ./models

# wrap job in package

python setup.py bdist_egg

# spin up spark cluster and mount input data and model to master and worker
# command: docker-compose -f docker-compose.yml up

# submit job
# command: spark-submit --master spark://0.0.0.0:7077 --archives nervosum-spark-env.tar.gz --py-files dist/poc_spark_job-0.0.1-py3.7.egg jobs/job.py --source_path ./jobs/data/input.csv --output_path ./jobs/data/output.csv


