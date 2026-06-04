"""Template (c): a simple multi-task Airflow DAG.

Four tasks with dependencies:  start >> [work_a, work_b] >> finish.
Replace the task bodies with your own logic. The platform sets the dag_id.
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def _work(name):
    print(f"running task: {name}")
    return name


with DAG(
    dag_id="__STUDENT_DAG_ID__",
    description="student multi-task example",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    is_paused_upon_creation=False,
    tags=["student-ui", "airflow-template"],
) as dag:
    start = BashOperator(task_id="start", bash_command="echo 'starting pipeline'")
    work_a = PythonOperator(task_id="work_a", python_callable=lambda: _work("A"))
    work_b = PythonOperator(task_id="work_b", python_callable=lambda: _work("B"))
    finish = BashOperator(task_id="finish", bash_command="echo 'pipeline done'")

    start >> [work_a, work_b] >> finish
