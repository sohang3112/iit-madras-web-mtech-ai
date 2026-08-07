"""
Part A: Feature Engineering using Spark ML.

Reads the Bank Marketing train.csv / test.csv (Kaggle playground-series-s5e8),
handles missing values, encodes categorical columns with StringIndexer, scales
numeric columns with StandardScaler (appropriate for the PyTorch MLP trained
in train_ic39149.py), assembles everything into a single feature vector with
VectorAssembler, builds the binary target label ("y") for the training set,
and writes both processed datasets to Parquet.

The preprocessing pipeline is fit on the training data only and then applied
to both the training and test datasets, so the test set is imputed/scaled/
encoded using statistics learned from the training data (no leakage). The
processed test dataset contains only the transformed feature vector (plus a
passthrough "id" column, if present, so predictions in Part C can be mapped
back to the right rows).

Usage:
    python features_ic39149.py \
        --train-csv /storage/data/datasets/assignment_2_dataset/train.csv \
        --test-csv /storage/data/datasets/assignment_2_dataset/test.csv \
        --output-dir data/processed
"""

import argparse
import os

from pyspark.ml import Pipeline
from pyspark.ml.feature import StandardScaler, StringIndexer, VectorAssembler
from pyspark.ml.functions import vector_to_array
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

ID_COLUMN = "id"
TARGET_COLUMN = "y"
NUMERIC_SPARK_TYPES = {"int", "bigint", "double", "float", "smallint", "tinyint"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Spark feature engineering for the Bank Marketing dataset"
    )
    parser.add_argument(
        "--train-csv", type=str,
        default="/storage/data/datasets/assignment_2_dataset/train.csv",
    )
    parser.add_argument(
        "--test-csv", type=str,
        default="/storage/data/datasets/assignment_2_dataset/test.csv",
    )
    parser.add_argument("--output-dir", type=str, default="/storage/models/web-mtech-ai")
    return parser.parse_args()


def build_spark_session():
    return (
        SparkSession.builder
        .appName("BankMarketingFeatureEngineering")
        .master("local[*]")
        .getOrCreate()
    )


def load_data(spark, path):
    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(path)
    )
    # normalize column names in case the source file has leading/trailing spaces
    return df.toDF(*[c.strip() for c in df.columns])


def get_column_types(df, exclude_cols):
    """Split columns into numeric / categorical buckets based on Spark's inferred schema."""
    numeric_cols, categorical_cols = [], []
    for field in df.schema.fields:
        if field.name in exclude_cols:
            continue
        if field.dataType.simpleString() in NUMERIC_SPARK_TYPES:
            numeric_cols.append(field.name)
        else:
            categorical_cols.append(field.name)
    return numeric_cols, categorical_cols


def handle_missing_values(df, numeric_cols, categorical_cols, fill_values=None):
    """Impute missing values.

    When `fill_values` is provided (computed on the training set), it is
    reused so the test set is imputed with training statistics instead of
    its own. Otherwise fill values (mode for categorical, median for
    numeric) are computed from `df` and returned alongside the imputed frame.
    """
    computed = fill_values is None
    if computed:
        fill_values = {}

    for col_name in categorical_cols:
        df = df.withColumn(
            col_name,
            F.when(F.trim(F.col(col_name)) == "", None).otherwise(F.trim(F.col(col_name))),
        )
        if computed:
            mode_row = (
                df.filter(F.col(col_name).isNotNull())
                .groupBy(col_name)
                .count()
                .orderBy(F.desc("count"))
                .first()
            )
            fill_values[col_name] = mode_row[0] if mode_row else "unknown"
        df = df.fillna({col_name: fill_values[col_name]})

    for col_name in numeric_cols:
        df = df.withColumn(col_name, F.col(col_name).cast(DoubleType()))
        if computed:
            fill_values[col_name] = df.approxQuantile(col_name, [0.5], 0.01)[0]
        df = df.fillna({col_name: fill_values[col_name]})

    return df, fill_values


def create_label(df, target_col=TARGET_COLUMN):
    """Binarize the target column into a numeric "label" column (0.0 / 1.0)."""
    distinct_vals = {
        str(row[0]).strip().lower()
        for row in df.select(target_col).distinct().collect()
        if row[0] is not None
    }
    if distinct_vals <= {"yes", "no"}:
        df = df.withColumn(
            "label",
            F.when(F.lower(F.trim(F.col(target_col))) == "yes", 1.0).otherwise(0.0),
        )
    else:
        df = df.withColumn("label", F.col(target_col).cast(DoubleType()))
    return df


def build_pipeline(numeric_cols, categorical_cols):
    indexers = [
        StringIndexer(inputCol=c, outputCol=f"{c}_idx", handleInvalid="keep")
        for c in categorical_cols
    ]
    numeric_assembler = VectorAssembler(inputCols=numeric_cols, outputCol="numeric_features")
    scaler = StandardScaler(
        inputCol="numeric_features", outputCol="scaled_numeric_features",
        withMean=True, withStd=True,
    )
    final_assembler = VectorAssembler(
        inputCols=["scaled_numeric_features"] + [f"{c}_idx" for c in categorical_cols],
        outputCol="features",
    )
    return Pipeline(stages=indexers + [numeric_assembler, scaler, final_assembler])


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    spark = build_spark_session()
    spark.sparkContext.setLogLevel("ERROR")

    print(f"Reading training data from {args.train_csv}")
    train_df = load_data(spark, args.train_csv)
    print(f"Reading test data from {args.test_csv}")
    test_df = load_data(spark, args.test_csv)

    has_id = ID_COLUMN in train_df.columns and ID_COLUMN in test_df.columns
    exclude_cols = {TARGET_COLUMN}
    if has_id:
        exclude_cols.add(ID_COLUMN)

    numeric_cols, categorical_cols = get_column_types(train_df, exclude_cols)
    print(f"Numeric columns ({len(numeric_cols)}): {numeric_cols}")
    print(f"Categorical columns ({len(categorical_cols)}): {categorical_cols}")

    print("Handling missing values (train statistics are reused for the test set)")
    train_df, fill_values = handle_missing_values(train_df, numeric_cols, categorical_cols)
    test_df, _ = handle_missing_values(
        test_df, numeric_cols, categorical_cols, fill_values=fill_values
    )

    print("Creating binary target label on the training set")
    train_df = create_label(train_df)

    print("Fitting preprocessing pipeline (StringIndexer -> StandardScaler -> VectorAssembler) on train")
    pipeline = build_pipeline(numeric_cols, categorical_cols)
    pipeline_model = pipeline.fit(train_df)

    print("Applying the fitted pipeline to the training and test datasets")
    train_processed = pipeline_model.transform(train_df)
    test_processed = pipeline_model.transform(test_df)

    # Store the feature vector as a plain array<double> so it can be read back
    # with pandas/pyarrow (no Spark dependency) in the training script.
    train_processed = train_processed.withColumn("features", vector_to_array("features"))
    test_processed = test_processed.withColumn("features", vector_to_array("features"))

    train_out_cols = ["features", "label"]
    test_out_cols = [ID_COLUMN, "features"] if has_id else ["features"]

    train_processed = train_processed.select(*train_out_cols)
    test_processed = test_processed.select(*test_out_cols)

    train_out_path = os.path.join(args.output_dir, "train_processed_ic39149.parquet")
    test_out_path = os.path.join(args.output_dir, "test_processed_ic39149.parquet")

    print(f"Writing processed training data to {train_out_path}")
    train_processed.write.mode("overwrite").parquet(train_out_path)
    print(f"Writing processed test data to {test_out_path}")
    test_processed.write.mode("overwrite").parquet(test_out_path)

    print(
        f"Done. Train rows: {train_processed.count()}, Test rows: {test_processed.count()}, "
        f"feature vector length: {len(numeric_cols) + len(categorical_cols)}"
    )

    spark.stop()


if __name__ == "__main__":
    main()
