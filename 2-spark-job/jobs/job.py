import argparse
import os
import logging
import json
import joblib
import sys

from sklearn.pipeline import Pipeline
from typing import Tuple, Dict, Any

from pyspark.context import SparkContext, SparkConf
from pyspark.sql.session import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import DoubleType

logger = logging.getLogger(__name__)


logger.warning(sys.version)


def load_json(filepath: str) -> Dict[Any, Any]:
    with open(filepath) as json_file:
        data = json.load(json_file)
    return data


def load_most_recent_model(
    model_dir: str,
) -> Tuple[Pipeline, Dict[str, str], Dict[str, str]]:
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
            joblib.load(os.path.join(model_dir, "model.joblib")),
            load_json(os.path.join(model_dir, "schema.json")),
            load_json(os.path.join(model_dir, "metadata.json")),
        )

    except Exception as e:
        logger.error(e)
        logger.info("No model found")
        raise e


if __name__ == "__main__":
    # get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_path", help="CSV source path")
    parser.add_argument("--output_path", help="CSV output path")
    args = parser.parse_args()

    if args.source_path and args.output_path:

        conf = SparkConf().setAppName("Nervosum-Job")

        sc = SparkContext(conf=conf)
        sc.addPyFile("/dependencies/dependencies_level1.zip")
        # sc.addPyFile('local://opt/workspace/Guido.zip')
        # sc.addPyFile('local://opt/workspace/dependencies.zip')

        spark = SparkSession(sc)

        # load data - both don't work.....
        spark_df = spark.read.option("header", True).csv(args.source_path)

        # load model
        model_path = "/models"

        model, model_schema, _metadata = load_most_recent_model(model_path)

        # doesn't work!
        @F.udf(returnType=DoubleType())
        def predict_udf(*cols):
            return model.predict(cols)

        # # does work!
        # def cool_function():
        #     return '1'
        #
        # @F.udf(returnType=StringType())
        # def predict_udf(*cols):
        #     return cool_function()

        # predict
        predictions = spark_df.select(
            predict_udf(*spark_df.schema.names).alias("predictions")
        )

        # export to CSV
        predictions.toPandas().to_csv(
            args.output_path, header=True, index=False
        )
        # predictions.write.mode('overwrite').format('csv').save('data/output')

    else:
        logger.info(
            "Not all arguments were given."
            " Please specify source and output path"
        )
