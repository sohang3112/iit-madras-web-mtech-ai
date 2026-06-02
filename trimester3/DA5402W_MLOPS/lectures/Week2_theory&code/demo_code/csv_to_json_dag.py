"""
DAG: csv_to_json
Reads csv from data/input/, converts it to JSON,
and writes it to data/output/output.json.
"""

#import csv
#import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

import pandas as pd

INPUT_FILE = "/home/alka/MLOPs-Class/airflow_practice/data-creation/data.CSV"
OUTPUT_FILE = "/home/alka/MLOPs-Class/airflow_practice/data-creation/output.json"


def CSVtoJSON(INPUT_FILE=INPUT_FILE, OUTPUT_FILE=OUTPUT_FILE):
    """Read CSV and print size, top 5 rows and column names."""
    df = pd.read_csv(INPUT_FILE)
    print(f"CSV has {len(df)} rows and {len(df.columns)} columns")
    print("Column names:")
    print(list(df.columns))
    print("Top 5 rows:")
    print(df.head(5))
    df.to_json(OUTPUT_FILE, orient="records", lines=True)  # save as JSON for next step
    


default_args = {
    "owner": "mlops",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="csv_to_json",
    description="Copy data from CSV to JSON",
    start_date=datetime(2026, 5, 18),
    schedule="@daily",   # monthly, weekly, quarterly, continuous, hourly,  etc. or cron expression (min, hour, day, month, day_of_week) like "0 0 * * *" for daily at midnight
    default_args=default_args,
    catchup=True,
    tags=["etl", "csv", "json"],
    #description="Reads and writes CSV data every day",
) as dag:

    print_starting = BashOperator(task_id='starting',
        bash_command='echo "I am reading the CSV now....."')

    CSVJson = PythonOperator(task_id='convertCSVtoJson',
        python_callable=CSVtoJSON)
    
    
    print_starting >> CSVJson
