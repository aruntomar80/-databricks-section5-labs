# Databricks notebook source
# Run through the deployed job. This overwrites only the configured lab source.
import re
dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.text("schema_name", "s5_arun_dev")
catalog = dbutils.widgets.get("catalog")
schema_name = dbutils.widgets.get("schema_name")
for value in (catalog, schema_name):
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
        raise ValueError("This lab uses simple catalog/schema identifiers only.")
if not schema_name.startswith("s5_"):
    raise ValueError("Use a dedicated schema beginning with s5_.")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{catalog}`.`{schema_name}`")
rows = [("Login", "3.5"), ("Search", "6.8"),
        ("Checkout", "4.7"), ("Broken", "unknown")]
spark.createDataFrame(rows, "transaction_name STRING, p90_raw STRING").write.format(
    "delta").mode("overwrite").saveAsTable(f"{catalog}.{schema_name}.raw_results")
print("SEED_OK", f"{catalog}.{schema_name}.raw_results", "rows=4")
