import argparse
import logging
import time

from pyspark.context import SparkContext, SparkConf
from pyspark.sql.session import SparkSession

from pyspark.sql.types import IntegerType
from pyspark.sql.types import StructType, StructField

from pydzipimport_linux import install
from model.model import Model


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

        # sc.addPyFile('/app/model_dependencies.zip')
        spark = SparkSession(sc)

        # load data
        spark_df = spark.read.option("header", True).csv(args.source_path)

        start = time.time()

        # # Approach pandas udf
        # schema = StructType([
        #     StructField("predictions",IntegerType(),True),
        # ])
        #
        # @pandas_udf(schema, PandasUDFType.GROUPED_MAP)
        # def predict_udf(df):
        #     install()
        #     import pandas as pd
        #     model = Model("/model/models")
        #     df = df.drop('a', axis=1)
        #     return pd.DataFrame(model.predict(df))
        #
        # predictions = spark_df.withColumn('a', F.lit(1))
        # .groupby('a').apply(predict_udf)

        # Aproach mapInPandas
        schema = StructType([StructField("predictions", IntegerType(), True)])

        def predict(iterator):
            install()
            import pandas as pd

            model = Model("/model/models")
            for df in iterator:
                yield pd.DataFrame(model.predict(df))

        predictions = spark_df.mapInPandas(predict, schema=schema)

        # # Approach memoization
        # @F.udf(returnType=IntegerType())
        # def predict_udf(*cols):
        #     if not 'model' in globals():
        #         install()
        #         globals()['model'] = Model("/model/models")
        #     model = globals()['model']
        #     return int(model.predict([[*cols]])[0])
        #
        # # predict
        # predictions = spark_df.select(
        #     predict_udf(*spark_df.columns).alias("predictions")
        # )

        predictions.write.mode("overwrite").format("csv").save("data/output")

        logger.info(f"TIME: {time.time() - start}")
    else:
        logger.info(
            "Not all arguments were given."
            " Please specify source and output path"
        )
