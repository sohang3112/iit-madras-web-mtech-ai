from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.task_group import TaskGroup

# Define core Python functions for the tasks
def generate_data():
    print("Generating synthetic data for the pipeline...")
    # Logic for data generation goes here
    return "Data generated successfully."

def validate_data():
    print("Validating data quality and schema...")
    # Simulating a validation check (True = Pass, False = Fail)
    data_is_valid = True 
    if data_is_valid:
        return "data_processing_group.DataPreprocessing"
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


# Default arguments for the DAG (including retry policies)
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
}

# Define the DAG
with DAG(
    dag_id='data_pipeline_ml_workflow',
    default_args=default_args,
    description='An advanced data pipeline with TaskGroups, Branching, and Parallelism',
    schedule_interval='*/5 * * * *',  # Scheduled to execute every 5 minutes
    catchup=False,
    tags=['machine_learning', 'analytics'],
) as dag:

    # 1. Data Generation Task (High priority to ensure data is ready quickly)
    data_generation = PythonOperator(
        task_id='DataGeneration',
        python_callable=generate_data,
        priority_weight=10,
    )

    # 2. Data Validation / Branching Task
    data_validation = BranchPythonOperator(
        task_id='DataValidation',
        python_callable=validate_data,
    )

    # 4. TaskGroup for Data Preparation (Organizing Preprocessing & Feature Engineering)
    with TaskGroup(group_id='data_processing_group') as data_processing_group:
        data_preprocessing = PythonOperator(
            task_id='DataPreprocessing',
            python_callable=preprocess_data,
        )

        feature_engineering = PythonOperator(
            task_id='FeatureEngineering',
            python_callable=feature_engineer,
            priority_weight=5, # Higher priority than standard analytics
        )

        # Dependency within the TaskGroup
        data_preprocessing >> feature_engineering

    # 5. Analytics Task (Will run in parallel with the data processing group)
    analytics = PythonOperator(
        task_id='Analytics',
        python_callable=run_analytics,
    )

    # 6. Report Generation Task
    # trigger_rule='none_failed_min_one_success' ensures this runs whether it 
    # comes from the validation failure branch OR the successful processing pipeline.
    report_generation = PythonOperator(
        task_id='ReportGeneration',
        python_callable=generate_report,
        trigger_rule='none_failed_min_one_success', 
    )

    # --- Task Dependencies & Parallelism ---
    
    # Step 1: Generate data then validate it
    data_generation >> data_validation

    # Step 2: Branching routes
    # Route A (Success): Branch into both the processing group and parallel Analytics
    data_validation >> [data_processing_group, analytics]
    
    # Route B (Failure): Branch directly to Report Generation (skipping processing/analytics)
    data_validation >> report_generation

    # Step 3: Reconverge successful parallel paths into the final report
    [data_processing_group, analytics] >> report_generation