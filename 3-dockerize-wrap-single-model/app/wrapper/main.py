import logging
import pandas as pd
from flask import Flask, request
from model.model import load_model
from typing import Any, Dict

logger = logging.getLogger(__name__)
app = Flask(__name__)

model = load_model("/trained_model")


@app.route("/predict", methods=["POST"])
def predict() -> Dict[str, Any]:
    """
    Predict endpoint.

    Returns:
        Output of request. A json containing either the field `classification`
        or `error` in case of an error.
    """
    try:
        input = request.json
        data = pd.DataFrame(input, index=[0])
        return {"classification": str(model["model"].predict(data)[0])}
    except Exception as err:
        return {"error": err}


@app.route("/schema")
def schema():
    """
    Schema endpoint

    Returns:
        The schema for the predict method

    """
    # page = request.args.get('page', default=1, type=int)
    return model["metadata"]


@app.route("/metadata")
def metadata():
    """
    Metadata endpoint

    Returns:
        Metadata of the model that is used for predicting.
    """
    return model["metadata"]


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
