Lab link: https://lab.samsai.io/student-ui/

Templates of simple Spark code are copied over from above dashboard to this folder.

Shared environment info of the tools used in this platform:

```
Spark platform — running component versions
============================================
Last verified: 2026-06-02 (after Airflow 3 upgrade attempt + rollback)

Orchestration & workflow
------------------------
Airflow              2.10.5  (Python 3.11, custom image spark-platform/airflow:2.10.5)
Airflow Postgres     15      (postgres:15, dedicated volume airflow_airflow_postgres_data)
Airflow Redis        7       (redis:7-alpine, Celery broker)

Spark cluster
-------------
Spark master/workers 3.4.0   (Scala 2.12.17, OpenJDK 1.8.0_452)
Worker count         3       (spark-worker-1, -2, -3)
Submit pattern       BashOperator -> docker exec spark-master spark-submit
Kafka connector      org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0  (resolved via --packages, cached in /tmp/.ivy2)

ML tracking
-----------
MLflow server        2.8.1   (custom image spark-platform-mlflow-server)
MLflow Postgres      13      (postgres:13)
Object store         RustFS  (rustfs/rustfs:latest, S3-compatible at rustfs:9000)

Streaming
---------
Kafka broker         Confluent CP 7.5.0    (confluentinc/cp-kafka:7.5.0)
Zookeeper            Confluent CP 7.5.0    (confluentinc/cp-zookeeper:7.5.0)
Kafka init           Confluent CP 7.4.0    (one-off topic creator)
Kafka UI             provectuslabs/kafka-ui:latest (served at /kafka-ui, context path /kafka-ui)
Kafka exporter       danielqsj/kafka-exporter:latest
```