import os
import logging
import json

from typing import Dict, Any

logger = logging.getLogger(__name__)


def load_json(filepath: str) -> Dict[Any, Any]:
    with open(filepath) as json_file:
        data = json.load(json_file)
    return data


def load_most_recent_model(model_dir: str,):
    """load model from file. If it does not yet exist, train a model

    Args:
        model_dir (str): Directory where models are stored.

    Returns:
        Pipeline: A trained model object
    """
    import joblib

    try:
        version = max(os.listdir(model_dir))
        logger.info("Load model")
        model_dir = os.path.join(model_dir, version)

        return (
            joblib.load(os.path.join(model_dir, "model.joblib")),
            load_json(os.path.join(model_dir, "schema.json")),
            load_json(os.path.join(model_dir, "metadata.json")),
        )

    except Exception as e:
        logger.error(e)
        logger.info("No model found")
        raise e


# def predict(data: pd.DataFrame) -> pd.DataFrame:
#     """Predict iris flower type
#
#     Args:
#         data (pd.DataFrame): Input dataframe
#
#     Returns:
#         pd.DataFrame: Output dataframe
#     """
#     return pd.DataFrame(data={"prediction": trained_model.predict(data)})


def predict(x):
    model, model_schema, _metadata = load_most_recent_model(
        "/Users/guidotournois/Projects/nervosum/"
        "proof-of-concepts/local_spark/model/models"
    )
    return model.predict(x)
