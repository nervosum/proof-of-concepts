#!/usr/bin/env bash
export PYTHONPATH=$PYTHONPATH:$PWD/model

spark-submit  --master local[*] \
wrapper/main.py --source_path data/input.csv --output_path data/output.csv

#--py-files $PWD/model_dependencies.zip \

#export PYSPARK_PYTHON=/Users/guidotournois/miniconda3/envs/nervosum_job/bin/python
#export PYSPARK_DRIVER_PYTHON=/Users/guidotournois/miniconda3/envs/nervosum_job/bin/python
#export HADOOP_CONF_DIR=$PWD/config
#spark-submit  --master yarn \
#--deploy-mode client \
#--num-executors 2 --executor-cores 2 \
#--driver-memory 1g --executor-memory 1g \
#wrapper/main.py --source_path data/input.csv --output_path data/output.csv
#--archives /Users/guidotournois/Projects/nervosum/proof-of-concepts/local_spark/model_dependencies.zip \
#--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=./environment/bin/python
#--conf spark.submit.pyFiles=/Users/guidotournois/Projects/nervosum/proof-of-concepts/local_spark/model_dependencies.zip \
#--conf spark.files=/Users/guidotournois/Projects/nervosum/proof-of-concepts/local_spark/model_dependencies.zip \
