"""Sample (Airflow): parallel Monte-Carlo Pi (fan-out / fan-in).

Four shards estimate Pi independently; 'combine' averages them via XCom.
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

SHARDS = 4


def mc_pi(seed, **_):
    import random
    samples = 2_000_000
    rnd = random.Random(seed)
    inside = 0
    for _ in range(samples):
        x = rnd.random()
        y = rnd.random()
        if x * x + y * y < 1.0:
            inside += 1
    est = 4.0 * inside / samples
    print(f"shard {seed}: pi ~= {est}")
    return est


def combine(**context):
    vals = context["ti"].xcom_pull(task_ids=[f"shard_{i}" for i in range(SHARDS)])
    avg = sum(vals) / len(vals)
    print(f"combined Pi estimate over {SHARDS} shards: {avg}")


with DAG(
    dag_id="__STUDENT_DAG_ID__",
    description="parallel Monte-Carlo Pi",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    is_paused_upon_creation=False,
    tags=["student-ui", "montecarlo"],
) as dag:
    shards = [PythonOperator(task_id=f"shard_{i}", python_callable=mc_pi, op_kwargs={"seed": i})
              for i in range(SHARDS)]
    combine_task = PythonOperator(task_id="combine", python_callable=combine)
    shards >> combine_task
