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


## Lecture 4 (week 2) - Apache Airflow for Data Engineering pipelines

* programmatic authoring, scheduling & monitoring of workflows as DAGs
* contains a web server, meta store, queuing system, executors
* can run single instance or on a cluster with many executor nodes
* Uses DAGs where each node is a task

When to Use:
* When workflow has clear start & end and runs on a schedule
* Prefers python coding to build workflow
  * Provides version control, team collaboration, testing & extensibility
* When pipeline is complex and recurring
* Process historical data, rerun failed tasks
* Designed for batched workflows

Airflow Architecture:
* Web Server (UI)
* Scheduler: monitors DAGs and triggers tasks based on time or events
* Executor: distributes tasks to workers. eg. `SequentialExecutor`, `CeleryExecutor`, `KubernetesExecutor`
* Workers: execute tasks
* Metadata database: store DAGs, task states and other metadata

DAGs' key attributes:
* Schedule: when workflows should run
* Tasks: discrete units of tasks that are run on workers
* Task Dependencies: order and conditions under which tasks execute
* Callbacks: actions to take when entire workflow completes
* Additional Parameters

Usecases:
* ETL (Extract / Data Ingestion, Transform, Load)
* ML Workflows (train, eval, deploy)
* Data Warehousing (pipelines for data lakes, warehouses)
* Ad-hoc Job Scheduling> more flexible than cron
* Code reusability, Fault tolerant, Visibility & control over data pipelines


## TODO Lecture 5 - Apache Kafka - SLIDES NOT UPLOADED YET (BUT VIDEO AVAILABLE)

TODO


## WIP Lecture 7 - [Apache Beam](https://beam.apache.org) - SLIDES NOT UPLOADED YET (BUT VIDEO AVAILABLE)

* Unified api for Batch & Streaming Data Processing
* Execute locally for development, testing, debugging using small datasets
* Same pipeline run on multiple engines/runners - Apache Flink, Apache Spark, Google Cloud DataFlow, Samza

*Pipeline as a Directed Acyclic Graph (DAG)*
* complete data workflow: read data, apply transforms (`PTransform`), write outputs. Data flows between them as `PCollection`.
* handle both bounded (batch) and unbounded (streaming) data with same pipeline

`PCollection`: core data structure in Beam
* unordered, potentially distributed collection of data elements from dataset/stream processed in parallel by Beam transforms.
* bounded (batch) or unbounded (streaming) data
* Time-aware: every elem has timestamp, belongs to a window, and is tracked using watermarks to handle event-time processing & late-arriving data
* Portable: Coder (serialization format) and Windowing Strategy (grouping, triggering, aggregation)

`PTransform` (data processing operation)
* It's a processing step in a pipeline: input & output are one or more `PCollection`
* Parallel execution (each element) via multiple workers using user-defined code
* Built-in transforms (`ParDo`, `GroupByKey`, `Combine`, `Count`), custom transforms
* Types: Source (`Read`, `Create`), Processing (`ParDo`, `GroupByKey`, `Combine`), Output (`Write`), User-Defined Composite

Aggregation:
* group data with same key & window and apply operations like `Count`, `Sum`, `Max`, `Average`
* Aggregation Transforms:
  * `GroupByKey`: output no smaller than input
  * `CombinePerKey`: group & apply combine function (sum, count) to produce smaller result set
* (for streaming data) relies on Windowing, Watermarks & Triggers to determine when results are complete and should be emitted.
* Parallel Scalability across millions of keys; when keys are few, they can be split into sub-keys and later recombined.

Advanced:
* Windowing: unbounded data streams are chunked into finite windows of types: Fixed, Sliding, Session, Global
* Watermarks: estimate how complete incoming event-time data is
* Triggers: control when window results are emitted. Supports early, on-time and late result generation.

Beam Workflow example from https://beam.apache.org/documentation/ml/about-ml/ (TODO: go through rest of that docs page):

![Beam Workflow Example](images/beam_workflow_example.png)

### [Spark ML](https://spark.apache.org)

TODO: go through https://spark.apache.org/docs/latest/ml-statistics.html , https://spark.apache.org/docs/latest/ml-datasource.html , https://spark.apache.org/docs/latest/ml-pipeline.html

* Common ML agos: classification, regression, clustering, collaborative filtering
* Featurization: feature extraction, reduction, dimensionality reduction, selection
* Pipelines: construct, evaluate & tune ML pipeline
* save & load model, algorithm, pipeline
* linear algebra, statistics, data learning

Basic statistics: Pearson & Spearman's correlation, hypothesis testing (`ChiSquareTest`), summarizer (available metrics are column-wise max, min, mean, sum, variance, std, number of non-zeros, total count)

Data Sources: Parquet, CSV, JSON, JDBC, image, libsvm etc.

Spark ML Pipelines (high level apis on top of DataFrames):
* DataFrame (from SparkSQL): supports text, feature vectors, true labels, predictions
* Transformer: DataFrame -> DataFrame
* Estimator: fit on a DataFrame to get a Transformer

Pipeline Components:
* Transformers (DataFrame -> DataFrame by append one or more columns): uses feature transform methods or trained models. eg. text -> feature vectors, trained model -> predicted labels
* Estimators: learns from input data and produces a trained model
* `Transformer.transform()` and `estimator.fit()` are stateless, and each transformer, estimator has unique id

Spark Pipeline (sequence of Stages) can be linear on non-linear DAG (like sequential or functional in keras):
* Run-time checking of DataFrame schema
* Unique pipeline stage objects (as each has unique id so cannot be reused, but can make different stage of same type)
* Uniform parameter api (for `fit`, `transform`): eg. `lr.setMaxIter(10)` sets for one instance, while `ParamMap(lr1.maxIter -> 10, lr2.maxIter -> 20)` sets for different instances
* ML Persistence: save & load models & pipelines using Scala, Java, Python; model saved in Spark 3.x can usually be loaded in later minor patch releases

![Spark Pipeline Example](images/spark_pipeline_example.png)

Model Selection & Tuning:
* Tuning for single estimator (elem in pipeline) or full pipeline
* Cross Validator (similar to `GridSearchCV`): 
  * for each hyper-parameter combination:
    * do k-fold (using average metric) & retrain on full data
  * Parallel hyper-param eval: `cv.setParallelism(4)`
