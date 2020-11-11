import argparse
import os
import logging
import json
import joblib

from sklearn.pipeline import Pipeline
from typing import Tuple, Dict

from pyspark.context import SparkContext, SparkConf
from pyspark.sql.session import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import DoubleType
from pyspark import SparkFiles

logger = logging.getLogger(__name__)

def load_json(filepath):
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


if __name__ == "__main__":

	# get arguments

	parser = argparse.ArgumentParser()
	parser.add_argument("--source_path", help="CSV source path")
	parser.add_argument("--output_path", help="CSV output path")
	args = parser.parse_args()

	if args.source_path and args.output_path:

		# start Spark session

		conf = SparkConf().setAppName("Nervosum-Job")
		sc = SparkContext(conf=conf)

		sc.addFile(args.source_path)

		spark = SparkSession(sc)

		# load data - both don't work.....

		spark_df = spark.read.option("header", True).csv(SparkFiles.get(args.source_path))
		#spark_df = spark.read.option("header", True).csv(args.source_path)

		# load model

		model_path = './models'

		model, model_schema, _metadata = load_most_recent_model(model_path)

		# define UDF

		@F.udf(returnType=DoubleType())
		def predict_udf(*cols):
			return float(model.predict((cols,)))

		# predict

		predictions = spark_df.select(
			predict_udf(*spark_df.schema.names).alias('predictions')
		)

		# export to CSV

		predictions.select("*").toPandas().to_csv(
			args.output_path,
			index=False,
			header=True)

	else:
		logger.info("Not all arguments were given. Please specify source and output path")

