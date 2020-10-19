import os
import logging
import pandas as pd
from flask import Flask, request
from model.model import trained_model, model_schema, _metadata


logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict endpoint.

    Returns:
        Output of request. A json containing either the field `classification`
        or `error` in case of an error.
    """
    try:
        input = request.json
        data = pd.DataFrame(input, index=[0])
        return {"classification": str(trained_model.predict(data)[0])}
    except Exception as err:
        return {"error": err}


@app.route("/schema", methods=["GET"])
def schema():
    """
    Schema endpoint

    Returns:
        The schema for the predict method
    """
    return model_schema


@app.route("/metadata", methods=["GET"])
def metadata():
    """
    Metadata endpoint

    Returns:
        Metadata of the model that is used for predicting.
    """
    return _metadata


if __name__ == "__main__":
    app.run(debug=True)
