import os
import logging
import json
import joblib
import pandas as pd
from training.train import train
from sklearn.pipeline import Pipeline
from typing import Tuple, Any
from pathlib import Path

logger = logging.getLogger(__name__)

def load_json(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
    return data


def load_most_recent_model(model_dir: str) -> Tuple[Any, Any, Any]:
    """load model from file. If it does not yet exist, train a model

    Args:
        model_dir (str): Directory where models are stored.

    Returns:
        Pipeline: A trained model object
    """

    try:
        version = max(os.listdir(model_dir))
        logger.info("Load model")
        model_dir = os.path.join(model_dir, version)

        return (
            joblib.load(os.path.join(model_dir, 'model.joblib')),
            load_json(os.path.join(model_dir, 'schema.json')),
            load_json(os.path.join(model_dir, 'metadata.json')))

    except Exception as e:
        logger.info("Create model")
        train(model_dir=model_dir)
        return load_most_recent_model(model_dir)


def predict(data: pd.DataFrame) -> pd.DataFrame:
    """Predict iris flower type

    Args:
        data (pd.DataFrame): Input dataframe

    Returns:
        pd.DataFrame: Output dataframe
    """
    return pd.DataFrame(data={'prediction': model.predict(data)})

model_path = os.path.join(os.path.dirname(__file__), '../models')
model = load_most_recent_model(model_path)
