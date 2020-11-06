

## Prerequisites
Model directory with trained models.

To generate a trained some IRIS models you can run the following command multiple times. <br>

`python 1-python-wrapper/training/train.py <path-to-model-dir>`

## Build the docker
`docker build --tag=modelwrapper .`

## Execute the docker
`docker run  -p 5000:5000 -v <path-to-model-dir>:/trained_models:ro modelwrapper`
