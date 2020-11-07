import logging
import pandas as pd
from flask import Flask, request
from model.model import models
from typing import Any, Dict

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/predict", methods=["POST"], defaults={"version": "latest"})
@app.route("/<version>/predict", methods=["POST"])
def predict(version: str) -> Dict[str, Any]:
    """
    Predict endpoint.

    Returns:
        Output of request. A json containing either the field `classification`
        or `error` in case of an error.
    """
    if version == "latest":
        version = max(models.keys())

    try:
        input = request.json
        data = pd.DataFrame(input, index=[0])
        return {
            "classification": str(models[version]["model"].predict(data)[0])
        }
    except Exception as err:
        return {"error": err}


@app.route("/schema", defaults={"version": "latest"})
@app.route("/<version>/schema", methods=["GET"])
def schema(version: str):
    """
    Schema endpoint

    Returns:
        The schema for the predict method

    """
    # page = request.args.get('page', default=1, type=int)
    if version == "latest":
        version = max(models.keys())
    return models[version]["metadata"]


@app.route("/metadata", defaults={"version": "latest"})
@app.route("/<version>/metadata", methods=["GET"])
def metadata(version: str):
    """
    Metadata endpoint

    Returns:
        Metadata of the model that is used for predicting.
    """
    if version == "latest":
        version = max(models.keys())
    return models[version]["metadata"]


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
