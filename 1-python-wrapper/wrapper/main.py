from flask import Flask, request
from model.model import load_most_recent_model
import pandas as pd
import logging


logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/predict', methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        print(schema)
        input = request.json
        data = pd.DataFrame(input, index=[0])
        return {"classification": str(model.predict(data)[0])}
    else:
        return "Please provide post request according to schema"


@app.route('/schema', methods=["GET"])
def schema():
    return schema


@app.route('/metadata', methods=["GET"])
def metadata():
    return metadata


if __name__=="__main__":
    model, schema, metadata = load_most_recent_model('../models')
    app.run(debug=True)