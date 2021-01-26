#!/usr/bin/env bash
export PYTHONPATH=$PYTHONPATH:$PWD/wrapper:$PWD/model

spark-submit  --master local[*] \
 --py-files $PWD/model_dependencies.zip \
wrapper/main.py --source_path data/input.csv --output_path data/output.csv
