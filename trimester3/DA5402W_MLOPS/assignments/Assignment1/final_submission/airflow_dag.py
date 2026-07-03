from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import (
    BranchPythonOperator,
    PythonOperator,
)
from airflow.sdk import TaskGroup

# ------ Task functions ---------


def generate_data():
    import os

    marker = "/tmp/generate_data_failed_once"
    if not os.path.exists(marker):
        with open(marker, "w") as f:
            f.write("failed")
        raise Exception("Simulated failure to demonstrate retry behavior")
    print("Generating synthetic data for the pipeline...")
    return "Data generated successfully."


def validate_data():
    print("Simulating a validation check...")
    data_is_valid = True
    if data_is_valid:
        return ["data_processing_group.DataPreprocessing", "Analytics"]
    else:
        return "ReportGeneration"


def preprocess_data():
    print("Cleaning missing values and normalizing data...")


def feature_engineer():
    print("Creating engineering features for analytics...")


def run_analytics():
    print("Running parallel analytics and aggregations on raw/validated data...")


def generate_report():
    print("Compiling results and generating the final pipeline report.")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "retries": 3,
    "retry_delay": timedelta(minutes=1),
}

# ------ DAG Definition ---------

with DAG(
    dag_id="data_pipeline_ml_workflow",
    default_args=default_args,
    description="An advanced data pipeline with TaskGroups, Branching, and Parallelism",
    schedule="*/5 * * * *",  # Scheduled to execute every 5 minutes
    catchup=False,
    tags=["machine_learning", "analytics"],
) as dag:
    data_generation = PythonOperator(
        task_id="DataGeneration",
        python_callable=generate_data,
        priority_weight=10,
    )

    data_validation = BranchPythonOperator(
        task_id="DataValidation",
        python_callable=validate_data,
    )

    with TaskGroup(group_id="data_processing_group") as data_processing_group:
        data_preprocessing = PythonOperator(
            task_id="DataPreprocessing",
            python_callable=preprocess_data,
        )

        feature_engineering = PythonOperator(
            task_id="FeatureEngineering",
            python_callable=feature_engineer,
            priority_weight=5,  # Higher priority than standard analytics
        )

        # Dependency within the TaskGroup
        data_preprocessing >> feature_engineering

    # Analytics Task (Will run in parallel with the data processing group)
    analytics = PythonOperator(
        task_id="Analytics",
        python_callable=run_analytics,
    )

    # Report Generation Task
    # trigger_rule='none_failed_min_one_success' ensures this runs whether it
    # comes from the validation failure branch OR the successful processing pipeline.
    report_generation = PythonOperator(
        task_id="ReportGeneration",
        python_callable=generate_report,
        trigger_rule="none_failed_min_one_success",
    )

    # --- Task Dependencies & Parallelism ---

    data_generation >> data_validation

    # Branching routes
    # Route A (Success): Branch into both the processing group and parallel Analytics
    data_validation >> [data_processing_group, analytics]

    # Route B (Failure): Branch directly to Report Generation (skipping processing/analytics)
    data_validation >> report_generation

    # Step 3: Reconverge successful parallel paths into the final report
    [data_processing_group, analytics] >> report_generation
