# Databricks notebook source
import re
from pyspark.sql import functions as F
RELEASE = "v1"  # Lab 5.3 changes this to v2, then promotes the same commit.
for name, default in [("catalog", "workspace"), ("schema_name", "s5_arun_dev"),
                      ("environment", "dev"), ("slow_threshold", "5.0"),
                      ("run_key", "interactive")]:
    dbutils.widgets.text(name, default)
catalog = dbutils.widgets.get("catalog")
schema_name = dbutils.widgets.get("schema_name")
environment = dbutils.widgets.get("environment")
threshold = float(dbutils.widgets.get("slow_threshold"))
run_key = dbutils.widgets.get("run_key")
for value in (catalog, schema_name):
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
        raise ValueError("Use simple lab identifiers.")
if not schema_name.startswith("s5_") or environment not in {"dev", "test", "prod"}:
    raise ValueError("Unexpected lab destination.")
if not (0 < threshold < 100):
    raise ValueError("Threshold must be positive and below 100 seconds.")
silver = spark.table(f"{catalog}.{schema_name}.silver_results")
actual = {r.transaction_name: r.p90_time for r in silver.collect()}
assert actual == {"Login": 3.5, "Search": 6.8, "Checkout": 4.7}, actual
gold = (silver
        .withColumn("performance_status", F.when(F.col("p90_time") > threshold, "SLOW").otherwise("OK"))
        .withColumn("environment", F.lit(environment))
        .withColumn("release", F.lit(RELEASE))
        .withColumn("run_key", F.lit(run_key)))
gold.write.format("delta").mode("overwrite").saveAsTable(f"{catalog}.{schema_name}.gold_results")
stored = spark.table(f"{catalog}.{schema_name}.gold_results")
assert stored.count() == 3
expected_slow = sum(value > threshold for value in actual.values())
assert stored.where(F.col("performance_status") == "SLOW").count() == expected_slow
assert stored.where((F.col("environment") != environment) | (F.col("release") != RELEASE)).count() == 0
print("VERIFY_OK", "environment=" + environment, "release=" + RELEASE,
      "threshold=" + str(threshold), "rows=3", "slow=" + str(expected_slow))
display(stored.orderBy("transaction_name"))
