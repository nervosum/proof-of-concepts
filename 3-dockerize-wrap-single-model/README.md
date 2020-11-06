

## Prerequisites
Model directory with trained models.

To generate a trained some IRIS models you can run the following command multiple times. <br>

`python ../1-python-wrapper/training/train.py ./models`

## Build the docker
`docker build --tag=modelwrapper .`

## Execute the docker
`docker run  -p 5000:5000 -v <path-to-model-dir>:/trained_models:ro modelwrapper`



## Calling the API's
You can either call the API without specifying a version. This would result in
calling the latest model and is done as follows.
```bash
$ curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"sepal_length": 1.2,"sepal_width": 3.4,"petal_length": 3.4,"petal_width": 5.9}' \
  http://localhost:5000/predict
{
  "classification": "1"
}
```
Also you can specify the version as seen below.
```bash
$ curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"sepal_length": 1.2,"sepal_width": 3.4,"petal_length": 3.4,"petal_width": 5.9}' \
  http://localhost:5000/<version>/predict
{
  "classification": "2"
}

```
