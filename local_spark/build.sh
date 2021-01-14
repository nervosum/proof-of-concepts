#!/usr/bin/env bash

pip install -r model/requirements.txt -t ./model_dependencies --no-compile --upgrade
cd model_dependencies
zip -r ../model_dependencies.zip .
