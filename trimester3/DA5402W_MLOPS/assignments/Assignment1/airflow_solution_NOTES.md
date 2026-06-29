[Airflow Quick Start](https://airflow.apache.org/docs/apache-airflow/stable/start.html) :

```bash
$ pip install "apache-airflow[celery]==3.2.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.2.2/constraints-3.10.txt"
$ mkdir -p ~/airflow
$ airflow version
3.2.2
$ airflow standalone         # init database, scheduler, start airflow server at port 8080
```

Open Airflow web UI at http://localhost:8080 