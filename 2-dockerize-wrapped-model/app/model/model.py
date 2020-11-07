import os
import logging
import json
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from typing import Dict, Any

logger = logging.getLogger(__name__)


def load_json(filepath: str) -> Dict[Any, Any]:
    """
    Wrapper around json.load

    Args:
        filepath:

    Returns:
        dict
    """

    with open(filepath) as json_file:
        data = json.load(json_file)
    return data


def load_model(model_path: str) -> Dict[str, Any]:
    """
    Load model files from path

    Args:
        model_path: the model path

    Returns:
        a tuple with pipeline, metadata and schema.
    """
    try:
        logger.info("Load model")

        return {
            "model": joblib.load(os.path.join(model_path, "model.joblib")),
            "schema": load_json(os.path.join(model_path, "schema.json")),
            "metadata": load_json(os.path.join(model_path, "metadata.json")),
        }

    except Exception as e:
        logger.error(e)
        logger.info("No model found")
        raise e


def load_models(model_dir: str) -> Dict[str, Dict[str, Any]]:
    """load models from dir.

        Args:
            model_dir (str): Directory where models are stored.

        Returns:
            Dict with named pipelines: A trained model object
        """

    versions = os.listdir(model_dir)
    models = {}
    for version in versions:
        model_path = os.path.join(model_dir, version)
        models[version] = load_model(model_path)
    return models


def predict(model: Pipeline, data: pd.DataFrame) -> pd.DataFrame:
    """Predict iris flower type

    Args:
        data (pd.DataFrame): Input dataframe

    Returns:
        pd.DataFrame: Output dataframe
    """

    # TODO: Validation of data with metadata
    return pd.DataFrame(data={"prediction": model.predict(data)})


model_path = "/trained_models"
models = load_models(model_path)
