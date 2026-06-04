"""Sample (Airflow): a multi-task compute pipeline.

    start >> [count_primes, fibonacci] >> report
Two compute tasks run in parallel; 'report' aggregates their results via XCom.
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def count_primes(**context):
    import math
    n = 1_000_000
    sieve = bytearray([1]) * n
    sieve[0] = 0
    sieve[1] = 0
    for p in range(2, math.isqrt(n) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytes(len(sieve[p * p::p]))
    count = sum(sieve)
    print(f"primes below {n}: {count}")
    context["ti"].xcom_push(key="primes", value=count)


def fibonacci(**context):
    n = 1000
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    digits = len(str(a))
    print(f"F({n}) has {digits} digits")
    context["ti"].xcom_push(key="fib_digits", value=digits)


def report(**context):
    ti = context["ti"]
    primes = ti.xcom_pull(task_ids="count_primes", key="primes")
    fib_digits = ti.xcom_pull(task_ids="fibonacci", key="fib_digits")
    print(f"REPORT: primes below 1,000,000 = {primes}; F(1000) has {fib_digits} digits")


with DAG(
    dag_id="__STUDENT_DAG_ID__",
    description="multi-task compute pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    is_paused_upon_creation=False,
    tags=["student-ui", "compute"],
) as dag:
    start = BashOperator(task_id="start", bash_command="echo 'pipeline start'")
    primes = PythonOperator(task_id="count_primes", python_callable=count_primes)
    fib = PythonOperator(task_id="fibonacci", python_callable=fibonacci)
    rep = PythonOperator(task_id="report", python_callable=report)
    start >> [primes, fib] >> rep
