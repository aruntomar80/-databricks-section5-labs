# Pipeline source file. Do not Run all as a normal notebook.
from pyspark import pipelines as dp
from pyspark.sql import functions as F

source = f"{spark.conf.get('lab.catalog')}.{spark.conf.get('lab.schema')}.raw_results"

@dp.materialized_view(name="silver_results")
def silver_results():
    return (
        spark.read.table(source)
        .select("transaction_name", F.expr("try_cast(p90_raw AS DOUBLE)").alias("p90_time"))
        .where(F.col("transaction_name").isNotNull())
        .where(F.col("p90_time").isNotNull() & (F.col("p90_time") >= 0))
    )
