import argparse
import logging

from pyspark.context import SparkContext, SparkConf
from pyspark.sql.session import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType

from pydzipimport_linux import install
from model import predict

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_path", help="CSV source path")
    parser.add_argument("--output_path", help="CSV output path")
    args = parser.parse_args()
    install()
    if args.source_path and args.output_path:

        conf = SparkConf().setAppName("Nervosum-Job")

        sc = SparkContext(conf=conf)
        spark = SparkSession(sc)

        # load data
        spark_df = spark.read.option("header", True).csv(args.source_path)

        @F.udf(returnType=IntegerType())
        def predict_udf(*cols):
            try:
                install()
            except Exception:
                pass
            return int(predict([[*cols]])[0])

        # predict
        predictions = spark_df.select(
            predict_udf(*spark_df.columns).alias("predictions")
        )

        predictions.write.mode("overwrite").format("csv").save("data/output")

    else:
        logger.info(
            "Not all arguments were given."
            " Please specify source and output path"
        )
