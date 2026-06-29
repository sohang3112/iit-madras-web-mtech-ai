# Part C Report: Workflow Orchestration Using Apache Airflow

## DAG Design

| Item | Value |
|---|---|
| DAG ID | `da5402w_part_c_workflow_orchestration` |
| Schedule | Every 5 minutes |
| Retries | 3 |
| Retry delay | 1 minute |
| Executor | LocalExecutor |
| Airflow UI | `http://localhost:8081` |

## Task List

| Task | Operator | Purpose |
|---|---|---|
| DataGeneration | PythonOperator | Generate sample sensor records |
| DataValidation | BranchPythonOperator | Validate generated records and choose execution branch |
| DataPreprocessing | PythonOperator | Remove invalid records |
| FeatureEngineering | PythonOperator | Create time and threshold features |
| Analytics | PythonOperator | Compute average temperature and status counts |
| ReportGeneration | PythonOperator | Generate the final workflow report |

## Dependency Analysis

```text
DataGeneration
  -> DataValidation
      -> processing.DataPreprocessing
      -> processing.FeatureEngineering
      -> analytics.Analytics
      -> analytics.ReportGeneration
      -> workflow_complete

DataValidation
  -> validation_failed
  -> workflow_complete
```

## Parallel Execution Opportunities

The DAG uses TaskGroups to organize related tasks. The validation branch separates the valid processing path from the failure path. In larger workflows, independent validation checks, independent feature engineering steps, and multiple analytics tasks could run in parallel after `DataValidation`.

## Branching Behavior

`DataValidation` is implemented as a `BranchPythonOperator`. If the generated dataset is valid, it routes execution to `processing.DataPreprocessing`. If validation fails, it routes execution to `validation_failed`.

## Retry Policy

All tasks inherit:

| Setting | Value |
|---|---|
| Retries | 3 |
| Retry delay | 1 minute |

Retry execution evidence was captured using the controlled retry demo variable `part_c_retry_demo=true`, which causes `DataGeneration` to fail on its first attempt and succeed on retry.

## Priority Weights

| Task | Priority Weight |
|---|---:|
| DataGeneration | 10 |
| DataValidation | 9 |
| DataPreprocessing | 8 |
| FeatureEngineering | 7 |
| Analytics | 6 |
| ReportGeneration | 5 |

## Screenshot Checklist

| Required Screenshot | Captured |
|---|---|
| DAG graph screenshot | `DAG_Graph_Screenshot` |
| TaskGroup screenshot | `Task_Group_Screenshot` |
| Branching behavior screenshot | `Branching_Behavior_Screenshot` |
| Retry configuration screenshot | `Retry_Config_Code_Screenshot` |
| Retry execution screenshot | `Retry_Execution_Screenshot` |
| Task duration summary screenshot | `Task_Duration_Screenshot` |
| Run duration screenshot | `Run_Duration_Screenshot` |

## Task Duration Summary

Task durations were captured in `Task_Duration_Screenshot`. The Airflow UI showed successful completed runs for all required tasks, with the scheduled run duration chart also captured in `Run_Duration_Screenshot`.

| Task | Duration |
|---|---:|
| DataGeneration | See `Task_Duration_Screenshot` |
| DataValidation | See `Task_Duration_Screenshot` |
| DataPreprocessing | See `Task_Duration_Screenshot` |
| FeatureEngineering | See `Task_Duration_Screenshot` |
| Analytics | See `Task_Duration_Screenshot` |
| ReportGeneration | See `Task_Duration_Screenshot` |

## Execution Results

Latest successful workflow report:

| Item | Value |
|---|---|
| Run ID | `scheduled__2026-06-24T21:00:00+00:00` |
| Status | `success` |
| Records processed | 50 |

Average temperature per sensor:

| Sensor | Average Temperature |
|---|---:|
| sensor_1 | 26.78 |
| sensor_2 | 27.64 |
| sensor_3 | 27.64 |
| sensor_4 | 22.01 |
| sensor_5 | 25.71 |

Status counts:

| Status | Count |
|---|---:|
| active | 11 |
| error | 15 |
| idle | 18 |
| maintenance | 6 |

## Generated Artefacts

The DAG writes files under `reports/`:

| Artefact | Purpose |
|---|---|
| `generated_<run_id>.json` | Generated sensor data |
| `validation_summary.json` | Validation result |
| `preprocessed_data.json` | Cleaned records |
| `features.json` | Feature engineered records |
| `analytics.json` | Analytics output |
| `workflow_report.json` | Final workflow report |

## Discussion

Workflow orchestration coordinates tasks that must run in a specific order, handles dependencies, and provides observability through logs, status, retries, and duration tracking.

Retries improve reliability because transient failures can be handled without manual reruns. Parallel execution reduces total workflow time when tasks are independent. Branching allows the workflow to choose different paths based on runtime conditions, such as whether validation succeeds or fails.
