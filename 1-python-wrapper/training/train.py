import os
import logging
import glob
import datetime
import joblib
import pandas as pd
from pathlib import Path

from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import json

logger = logging.getLogger(__name__)


def write_to_json(obj, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)

def process_dtypes(schema):
    return (schema
            .apply(lambda dt: dt.name)
            .reset_index()
            .rename(columns={'index': 'name', 0: 'type'})
            .to_dict('records'))

def save_model(pipe: Pipeline, model_dir: str, input_schema) -> None:
    version = int(datetime.datetime.utcnow().timestamp())
    model_version_dir = os.path.join(model_dir, str(version))
    file_name = os.path.join(model_version_dir , 'model.joblib')

    # First make sure directory exists
    Path(file_name).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, file_name)

    schema = {'input': process_dtypes(input_schema),
              'output' : {'prediction':'int64'}}

    write_to_json(schema, os.path.join(model_version_dir, 'schema.json'))

    metadata = {
        'training_date': datetime.datetime.utcnow().date().isoformat(),
        'model_version': version}

    write_to_json(metadata, os.path.join(model_version_dir, 'metadata.json'))


def train(model_dir: str) -> Pipeline:
    """Train a model for the IRIS model and dump at specified location

    Args:
        output_dir (str): directory to save the model in
    """
    #load data
    logger.info("loading IRIS data")
    iris = load_iris()
    data = pd.DataFrame(iris.data)
    data.columns = [x[:-5].replace(' ','_') for x in iris.feature_names]
    target = pd.DataFrame(iris.target)
    target = target.rename(columns = {0: 'target'})

    # Assuming that using proper evaluation, we found out RFC and Scaler is optimal
    # Create model
    logger.info("Creating and fitting model")
    pipe = Pipeline([('scaler', StandardScaler()),
                     ('model', RandomForestClassifier())])

    pipe.fit(data, target.values.ravel())

    logger.info("Save model")
    save_model(pipe, model_dir, data.dtypes)


if __name__=="__main__":
    train(model_dir='./models')
