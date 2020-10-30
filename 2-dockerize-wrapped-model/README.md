

## Prerequisites
Model directory with trained models

## Build the docker
docker build --tag=modelwrapper .

## Execute the docker
docker run  -p 5000:5000 -v <path-to-model-dir>:/trained_models:ro distrotest
