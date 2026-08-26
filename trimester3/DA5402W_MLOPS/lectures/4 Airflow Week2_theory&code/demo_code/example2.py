from datetime import datetime

from airflow.sdk import DAG, task
from airflow.providers.standard.operators.bash import BashOperator
import pandas as pd

file_path = '/home/alka/MLOPs-Class/airflow_practice/data-creation/data.CSV'
output_path = '/home/alka/MLOPs-Class/airflow_practice/data-creation/data.json'
# A Dag represents a workflow, a collection of tasks
with DAG(dag_id="demo1", start_date=datetime(2022, 1, 1), schedule="0 0 * * *") as dag:
    # Tasks are represented as operators
    hello = BashOperator(task_id="hello", bash_command="echo 'reading data now...'")

    @task()
    def airflow():
        print("airflow")

    @task()
    def read_data():
        df = pd.read_csv(file_path)
        print(df.head())

    @task()
    def process_data():
        df = pd.read_csv(file_path)
        print(df.describe())

    @task()
    def write_data():
        df = pd.read_csv(file_path)
        df.to_json(output_path, orient='records', lines=True)

    # Set dependencies between tasks
    read_data_task = read_data()
    hello >> airflow() >> read_data_task >> process_data()
    read_data_task >> write_data()

    # each function reads csv file to avoid sharing data between tasks, which is not recommended in Airflow. In production, you would typically use a shared storage system or a database to pass data between tasks.