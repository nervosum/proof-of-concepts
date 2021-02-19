#!/usr/bin/env bash
export PYTHONPATH=$PYTHONPATH:$PWD/wrapper:$PWD/model

spark-submit  --master local[*] \
--py-files $PWD/model_dependencies.zip \
--conf "spark.python.worker.memory=500m" \
--conf "spark.executor.memory=500m" \
wrapper/main.py --source_path data/input_large.csv --output_path data/output.csv
