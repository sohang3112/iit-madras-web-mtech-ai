import pyspark
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator
import ray
from ray import tune
from ray.tune.schedulers import ASHAScheduler
import ray.train
import mlflow
import time
import os  # <-- Required for path resolution
import tempfile
import pandas as pd
import traceback

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

from ray.air.integrations.mlflow import setup_mlflow

ray.init()

# --- FIX HERE: Get absolute path relative to where you execute the script ---
DATASET_PATH = os.path.abspath("train_processed_DA25M622.parquet")

def trainable(config):
    try:
        setup_mlflow(
            config,
            experiment_name="assignment 2 DA25M622",
            create_experiment_if_not_exists=True
        )
        
        spark = SparkSession.builder \
            .appName(f"Trial_{ray.tune.get_context().get_trial_id()}") \
            .config("spark.driver.bindAddress", "127.0.0.1") \
            .getOrCreate()
        
        # Workers can now successfully open the file from anywhere on the machine
        df = spark.read.parquet(DATASET_PATH)
        train_df, val_df = df.randomSplit([0.8, 0.2], seed=42)
        
        f1_evaluator = MulticlassClassificationEvaluator(labelCol="y", predictionCol="prediction", metricName="f1")
        acc_evaluator = MulticlassClassificationEvaluator(labelCol="y", predictionCol="prediction", metricName="accuracy")
        prec_evaluator = MulticlassClassificationEvaluator(labelCol="y", predictionCol="prediction", metricName="weightedPrecision")
        rec_evaluator = MulticlassClassificationEvaluator(labelCol="y", predictionCol="prediction", metricName="weightedRecall")
        roc_evaluator = BinaryClassificationEvaluator(labelCol="y", rawPredictionCol="rawPrediction", metricName="areaUnderROC")

        start_time = time.time()
        
        lr = LogisticRegression(
            regParam=1/config["C"], 
            maxIter=config["max_iter"], 
            featuresCol='features', 
            labelCol='y'
        )
        
        model = lr.fit(train_df)
        training_time = time.time() - start_time
        
        predictions = model.transform(val_df)
        
        f1_score = f1_evaluator.evaluate(predictions)
        accuracy = acc_evaluator.evaluate(predictions)
        precision = prec_evaluator.evaluate(predictions)
        recall = rec_evaluator.evaluate(predictions)
        roc_auc = roc_evaluator.evaluate(predictions)
        
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1_score)
        mlflow.log_metric("roc_auc", roc_auc)
        mlflow.log_metric("training_time", training_time)
        
        eval_pd = predictions.select("y", "prediction").toPandas()
        y_true = eval_pd["y"]
        y_pred = eval_pd["prediction"]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = os.path.join(tmpdir, "classification_report.txt")
            with open(report_path, "w") as f:
                f.write(classification_report(y_true, y_pred))
            mlflow.log_artifact(report_path)
            
            cm = confusion_matrix(y_true, y_pred)
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
            ax.set_ylabel('Actual')
            ax.set_xlabel('Predicted')
            ax.set_title('Confusion Matrix')
            cm_path = os.path.join(tmpdir, "confusion_matrix.png")
            fig.savefig(cm_path)
            plt.close(fig)
            mlflow.log_artifact(cm_path)
            
            pred_path = os.path.join(tmpdir, "validation_predictions.csv")
            eval_pd.to_csv(pred_path, index=False)
            mlflow.log_artifact(pred_path)
            
            mlflow.spark.log_model(model, artifact_path="model")

        spark.stop()
        ray.tune.report({"f1": f1_score, "accuracy": accuracy})

    except Exception as e:
        print("--- WORKER EXCEPTION ENCOUNTERED ---")
        traceback.print_exc()
        ray.tune.report({"f1": 0.0, "accuracy": 0.0})

search_space = {
    "C": tune.loguniform(1e-3, 1e2, 1e1),
    "max_iter": tune.choice([50, 100, 200, 400]),
}

tuner = tune.Tuner(
    trainable,
    param_space=search_space,
    tune_config=tune.TuneConfig(
        num_samples=8,
        scheduler=ASHAScheduler(metric="f1", mode="max"),
    ),
)

results = tuner.fit()
best = results.get_best_result(metric="f1", mode="max")
print("Best config:", best.config)
print("Best F1 score recorded:", best.metrics.get("f1"))