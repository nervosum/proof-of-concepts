# 1 - Python wrapper

We take the iris data set and train a simple classification model for it.

* Example training code is present in `training`
* The model object with the `predict` function can be found in the `model` module
* A flask interface and main app can be found in `wrapper`

## Expected format

predict: { "sepal_length": 0, "sepal_width" :1, "petal_length": 2, "petal_width": 3} => { "classification": "predicted_class" }

## How to install and start the api

Install the package in your environment using:

``` bash
# Install package with all dependencies
pip install -e . 
# Start flask app.
python wrapper/main.py
```


