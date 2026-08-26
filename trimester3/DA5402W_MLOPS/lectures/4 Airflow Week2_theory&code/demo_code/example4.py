from datetime import datetime, timedelta

from airflow.sdk import DAG, task

ALERT_FILE = '/tmp/airflow_failure_alerts.txt'

def notify_failure(context):
    ti = context['task_instance']
    msg = (
        f"[ALERT] Task '{ti.task_id}' in DAG '{ti.dag_id}' FAILED\n"
        f"        Run: {context['run_id']}\n"
    )
    # Write to a file so the alert is visible outside task logs
    with open(ALERT_FILE, 'a') as f:
        f.write(msg)
    print(msg)   # also visible in task log (click task → Log in UI)


# ═══════════════════════════════════════════════════════════════
# DAG 1: One task fails → others still run + notification sent
#
# Flow: task_a → task_b (FAILS) → task_c → task_d
#       task_b fires notify_failure on failure
#       task_c and task_d use trigger_rule='all_done' so they
#       run regardless of upstream success/failure
# trigger rules: https://airflow.apache.org/docs/apache-airflow/stable/concepts/operators.html#trigger-rules
# trigger_rule='all_done', 'all_success' (default), 'all_failed', always', 'none_failed', 'one_success', 'one_failed', etc.
# ═══════════════════════════════════════════════════════════════
with DAG(
    dag_id="pipeline_continues_on_failure",
    start_date=datetime(2025, 1, 1),   # fixed date — avoids parse-time warning
    schedule=None,                      # trigger manually from UI
    catchup=False,
    tags=["example", "failure-handling"],
) as dag1:

    @task()
    def task_a():
        print("task_a: completed successfully")

    @task(on_failure_callback=notify_failure)
    def task_b():
        raise Exception("Intentional failure in task_b!")

    @task(trigger_rule='all_done')
    def task_c():
        print("task_c: running despite task_b failure")

    @task(trigger_rule='all_done')
    def task_d():
        print("task_d: pipeline end — always reached")

    task_a() >> task_b() >> task_c() >> task_d()


# ═══════════════════════════════════════════════════════════════
# DAG 2: One task fails → all subsequent tasks are skipped
#
# Default trigger_rule='all_success' means task_c and task_d
# are marked UPSTREAM_FAILED and never execute
# ═══════════════════════════════════════════════════════════════
with DAG(
    dag_id="pipeline_stops_on_failure",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["example", "failure-handling"],
) as dag2:

    @task()
    def task_a():
        print("task_a: completed successfully")

    @task()
    def task_b():
        raise Exception("Intentional failure in task_b!")

    @task()
    def task_c():
        print("task_c: this will NOT run")

    @task()
    def task_d():
        print("task_d: this will NOT run either")

    task_a() >> task_b() >> task_c() >> task_d()
