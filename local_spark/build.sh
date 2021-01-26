#!/usr/bin/env bash
pip install -r wrapper/requirements-wrapper.txt

pip install -r model/requirements.txt -t ./model_dependencies
cd model_dependencies
zip -r ../model_dependencies.zip .
