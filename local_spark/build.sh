#!/usr/bin/env bash
pip3 install -r wrapper/requirements-wrapper.txt

pip3 install -r model/requirements.txt -t ./model_dependencies
cd model_dependencies
zip -r ../model_dependencies.zip .
