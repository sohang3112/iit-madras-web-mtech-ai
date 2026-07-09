# /storage/data/datasets/
# /storage/models/
# /storage/runs/
# /storage/scratch/  # Tmp files
# /storage/code/

# Convention — sub-namespace by username so paths don't collide:

# /storage/models/<username>/<model-name>/
# /storage/runs/<username>/<job-name>/<timestamp>/
# /storage/data/datasets/<dataset-name>/


###### Snippets Example #####

# 1 — Read a dataset (PySpark)

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("nyc-trips").getOrCreate()

df = spark.read.csv(
    "/storage/data/datasets/citibike/202401.csv", header=True, inferSchema=True
)
# or Parquet:
df = spark.read.parquet("/storage/data/datasets/nyc-taxi/")
df.show(5)

# 2 — Write a Spark DataFrame as output

out = "/storage/runs/teststudent/citibike-summary/"
(df.groupBy("station_id").count().write.mode("overwrite").parquet(out))

# 3 — Save & load a scikit-learn model

import os

import joblib
from sklearn.linear_model import LogisticRegression

model = LogisticRegression().fit(X_train, y_train)

path = "/storage/models/teststudent/loan-default/model.joblib"
os.makedirs(os.path.dirname(path), exist_ok=True)
joblib.dump(model, path)

# In a later submission — exact same path
clf = joblib.load("/storage/models/teststudent/loan-default/model.joblib")
preds = clf.predict(X_test)
