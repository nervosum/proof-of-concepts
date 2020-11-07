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
# Install all package dependencies
pip install -r requirements.txt
# Start flask app.
python wrapper/main.py
```


## Static analysis

For performing static analysis we use [Pre-Commit](https://calmcode.io/pre-commit/the-problem.html).
Pre-commit allows us to easily run a suite of tests, as defined in the
[.pre-commit-config.yaml](.pre-commit-config.yaml) in this project.
This project will make use of the folowing checks:

* Trivial checks:
    * The encoding of the files
    * If it is valid Python in the files
    * If the YAML files are nicely formatted
    * The code is free of debug statements
* [**Flake8**](https://pypi.org/project/flake8/) is a Python library that wraps PyFlakes,
pycodestyle and Ned Batchelder's McCabe script.
It is a great toolkit for checking your code base against coding style
([PEP 8](https://www.python.org/dev/peps/pep-0008/), programming errors
 (like “library imported but unused” and “Undefined name”) and to check complexity.
* [**Black**](https://github.com/psf/black) is the Python code formatter and makes sure that we
format our Python code in the same way. By using it, you agree to cede control over minutiae of hand-formatting.
In return, Black gives you speed, determinism, and freedom from pycodestyle nagging about formatting.
You will save time and mental energy for more important matters.
* [**MyPy**](https://github.com/python/mypy) is an optional static type checker for Python.
You can add type hints ([PEP 484](https://www.python.org/dev/peps/pep-0484/)) to your Python programs,
and use mypy to type check them statically. Find bugs in your programs without even running them!

If you want to run this automatically before each commit, you can install it as a pre-commit hook:
```bash
pip install pre-commit  # install the package in your environment
pre-commit install  # add the git hook
```

You can easily run it also manually using:
```bash
pre-commit run --all-files
```

The setttings for the pre-commit hooks of flake8 and mypy can be found within `tox.ini`.

## Calling the API's

```bash
$ curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"sepal_length": 1.2,"sepal_width": 3.4,"petal_length": 3.4,"petal_width": 5.9}' \
  http://localhost:5000/predict
{
  "classification": "2"
}

```
