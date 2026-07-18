"""Part A - Feature Engineering using Spark."""

#%%
import pyspark
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler, Imputer, StandardScaler
from pyspark.ml.classification import LogisticRegression

spark = SparkSession.builder.appName("Assignment2_PartA").getOrCreate()

train_df = spark.read.csv("data/playground-series-s5e8/train.csv", header=True, inferSchema=True)
test_df = spark.read.csv("data/playground-series-s5e8/test.csv", header=True, inferSchema=True)

#%%
categoricalCols = ["job", "marital", "education", "default", "housing", "loan", "contact", "month", "poutcome"]
numericalCols = ["age", "balance", "day", "duration", "campaign", "pdays", "previous"]

imputedNumericalCols = [c + "_imputed" for c in numericalCols]
indexedCategoricalCols = [c + "_indexed" for c in categoricalCols]

pipeline_stages = [
    # handle missing numerical data
    Imputer(inputCols=numericalCols, outputCols=imputedNumericalCols),
    # encode categorical data and handle missing categorical data
    StringIndexer(inputCols=categoricalCols, outputCols=indexedCategoricalCols, handleInvalid="keep"),
    # Assemble and scale the numerical features (required for model)
    VectorAssembler(inputCols=imputedNumericalCols, outputCol='num_features_assembled'),
    StandardScaler(inputCol='num_features_assembled', outputCol='num_features_scaled', withStd=True, withMean=False),
    # Combine all final (numerical, categorical) into 'features'
    VectorAssembler(inputCols=['num_features_scaled'] + indexedCategoricalCols, outputCol='features')
]

preprocessing_pipeline = Pipeline(stages=pipeline_stages)

# Fit and transform
preprocessor = preprocessing_pipeline.fit(train_df)
train_df_preprocessed = preprocessor.transform(train_df)
test_df_preprocessed = preprocessor.transform(test_df)

# in train output col 'y' automatically remained as it is as no transform was done on it

# train_df_preprocessed.show()
# test_df_preprocessed.show()

# lr = LogisticRegression(featuresCol='features', labelCol='y')

# create target label for training dataset
# %%
# NOTE: these actually create FOLDERS {train,test}_processed_DA25M622.parquet - folders contain actual parquet files
train_df_preprocessed.write.mode("overwrite").parquet("train_processed_DA25M622.parquet")
test_df_preprocessed.write.mode("overwrite").parquet("test_processed_DA25M622.parquet")

# %%
