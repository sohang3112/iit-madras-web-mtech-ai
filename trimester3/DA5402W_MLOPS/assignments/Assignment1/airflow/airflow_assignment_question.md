# Part C: Workflow Orchestration using Apache Airflow (20 Marks)
Design and implement an Apache Airflow DAG to automate a data processing workflow.

## Workflow Tasks

The DAG must contain the following tasks:
1. DataGeneration
2. DataValidation
3. DataPreprocessing
4. FeatureEngineering
5. Analytics
6. ReportGeneration

## Requirements
1. Design an Airflow DAG using the tasks listed above.
2. Determine appropriate dependencies between tasks.
3. Identify tasks that can execute in parallel and implement parallel execution wherever
appropriate.
4. Organize related tasks using at least one TaskGroup.
5. Configure retry policies:
 * Retries = 3
 * Retry delay = 1 minute
6. Use a BranchPythonOperator to implement conditional execution.
7. Assign suitable priority weights to selected tasks.
8. Schedule the DAG to execute every 5 minutes.
9. Monitor DAG execution using the Airflow UI.

## Airflow Report Requirements

Include:
1. DAG graph screenshot.
2. Description of task dependencies.
3. Explanation of parallel execution opportunities.
4. Branching behavior screenshot.
5. Retry execution screenshot.
6. Task duration summary.
