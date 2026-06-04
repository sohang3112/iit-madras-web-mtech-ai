# DA5402W - ML Ops

Professors:
* Dr. Alka Bhushan &lt;ic39149@imail.iitm.ac.in&gt;: will cover first 3 modules of syllabus
* Dr. Priyanka Naik
* Dr. Aishwarya Chakraborty

Teaching Assistants (TAs):
* Jashaswaimalya -- software & tools-related issues
* Shuvrajeet -- assignment & quiz-related issues

Focus on open source tools that can be deployed anywhere, not cloud-based tools. Some are:

* Apache Kafka: messaging queue
* Apache Spark: in-memory distributed computing --> MOST IMPORTANT
* Apache Atlas: data compliance (eg. we have to report where sensitive data is stored to govt), manage metadata

**PySpark Lab Link**: https://lab.samsai.io/student-ui/ (need to sign in with google via IIT smail (student email))

Theory lecture notes are here, code lecture notes seperately.

Datasets for Modules 1-3 :
* [Intel Image Classification dataset](https://www.kaggle.com/datasets/puneet6060/intel-image-classification/data)
* [New York Taxi records dataset](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## WIP Lecture 2 - Apache Spark, Data Engineering

### Course Overview

* ML Ops is intersection of Machine Learning, Dev Ops, Data Engineering.
* ML Ops end-to-end pipeline: Data -> Training -> Deployment -> Monitoring
* Tasks:
    * Experiment Tracking: model & dataset versions, hyperparameters, eval metrics, train configs, logs.
    * Model Deployment: APIs, web services, edge devices, cloud platforms
    * Model Monitoring: prediction metrics, response latency, resource utilization, failure rates, data quality, drift detection
    * Model Retraining: scheduled, trigger-based, continous
  
MLOps Workflow:

![MLOps Workflow](images/mlops_workflow.png)

* Tools:
  * *Apache Airflow*: automate & schedule piping tasks
  * *Apache Kafka*: real-time streaming data
  * *Apache Spark*: process & analyze large-scale data, distributed ML
  * *MLFlow*: manage experiment tracking, model lifecycle & development
  * *AutoML*: automate model selection, training & tuning
  * *Git & DVC*: version control for data, code & model pipelines
  * *Prometheus & Kibana*: data visualization, monitoring of logs & metrics

### Apache Spark

It's a distributed computing platform, with a wide range of workloads it can handle like batch algos, iterative, streaming, etc.

Apache Spark connectors ecosystem with a wide variety of tools like Kafka, MySQL, etc. :

![Apache Spark Connectors](images/apache_spark_connectors.png)

Spark Components:
* Spark Core dataframes & Spark SQL Engine: Java/Python/etc., RDBMS table, CSV, Parquet, JSON, etc.
* MLLib: machine learning algorithms, linear algebra, gradient descent optimization, feature extraction, transformation, pipeline, model tuning
* Spark Structured Real-time Streaming
* Graph X: graph algos - page rank, connected components, triangle counting etc.

Spark Distributed Execution:

![Spark Distributed Execution](images/spark_distributed_execution.png)

Spark Driver:
* creates Spark Session object
* Accesses cluster manager and executes in session
* transforms Spark operations into DAG computations, schedules them and distributes as tasks across Spark executors
* After resource alloc, directly communicate with executors

Spark Session:
* single unified entry to all Spark operations
* Can create JVM runtime parameters, define DataFrame and Datasets, read from data sources, access catalog metadata, issue Spark SQL queries

Cluster Manager:
* manage & alloc resources for cluster of nodes
* Local / standalone / Yarn / Kubernetes

Spark Executors:
* execute tasks
* communicate with drivers
* run on worker nodes

Distributed Data & Partitions: 
* Each executor gets number of partitions = Min(2, Number of Executor Cores + 1)

![Spark Distributed Data & Partitions](images/spark_distributed_partitions.png)

* Driver creates a DAG for each job via `count()`, `show()`, `collect()` (brings all data into memory, use with caution), etc.
* Stages are created for each Shuffle operation (usually more expensive than action operations) via `groupByKey()`, `reduceByKey()`
* Task (set of steps) is assigned to a partition. All tasks in a stage run in parallel.

![Spark Driver, Stages & Tasks](images/spark_driver_stage_task.png)

Spark Operations:
* Transformations (lazy): Narrow or Wide (wide causes shuffling of data across executors): `orderBy()`, `groupBy()`, `filter()`, `select()`, `join()`
* Actions: cause data to be materialized (return to driver, save to file): `show()`, `take()`, `count()`, `collect()`, `save()`

Spark Structured APIS: Spark DataFrame, and Spark SQL

Data Collection Strategies:
* Batch (files, database, cloud)
* Streaming (kafka)
* Batch + Streaming (hybrid)

### WIP Data Engineering

* Data infra (on-prem / cloud / hybrid-cloud / multi-cloud), databases and pipelines to extract, transform & load data
* Data Characterstics: Volume (how many records?), Velocity (how many users?), Variety (how many data formats?)

Data Engineering Architecture:
* Applications
* Relational Database
* Batch / Streaming pipeline
* Data Lake (store huge raw structured or unstructured data)
* ETL (Extract, Transform, Load)
  * Extract from: logs, databases, APIs, etc.
  * Transform: clean & process data: Remove duplicates, standardize formats, aggregate, validate
  * Load: store processed data
* Data Warehouse: convert data from data lake into clean, structured, aggregated and optimized data for fast analytical queries
* BI dashboards / ML

TODO


## TODO Lecture 4 (week 2) - Apache Airflow

TODO


## TODO Lecture 5 - Apache Kafka - SLIDES NOT UPLOADED YET (BUT VIDEO AVAILABLE)

TODO


## TODO Lecture 6 - MLFlow

TODO

