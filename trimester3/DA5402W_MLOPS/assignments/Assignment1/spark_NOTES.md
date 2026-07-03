```
$ spark-submit spark_streaming.py
WARNING: Using incubator modules: jdk.incubator.vector
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
26/07/02 18:05:25 WARN Utils: Your hostname, sohang-VivoBook-ASUS-Laptop-X510UFO, resolves to a loopback address: 127.0.1.1; using 192.168.1.31 instead (on interface wlp2s0)
26/07/02 18:05:25 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
26/07/02 18:05:27 INFO SparkContext: Running Spark version 4.1.2
26/07/02 18:05:27 INFO SparkContext: OS info Linux, 7.0.0-27-generic, amd64
26/07/02 18:05:27 INFO SparkContext: Java version 17.0.19+10-1-26.04.2-Ubuntu
26/07/02 18:05:27 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
26/07/02 18:05:27 INFO ResourceUtils: ==============================================================
26/07/02 18:05:27 INFO ResourceUtils: No custom resources configured for spark.driver.
26/07/02 18:05:27 INFO ResourceUtils: ==============================================================
26/07/02 18:05:27 INFO SparkContext: Submitted application: SensorStreamingPipeline
26/07/02 18:05:27 INFO SecurityManager: Changing view acls to: sohang
26/07/02 18:05:27 INFO SecurityManager: Changing modify acls to: sohang
26/07/02 18:05:27 INFO SecurityManager: Changing view acls groups to: sohang
26/07/02 18:05:27 INFO SecurityManager: Changing modify acls groups to: sohang
26/07/02 18:05:27 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: sohang groups with view permissions: EMPTY; users with modify permissions: sohang; groups with modify permissions: EMPTY; RPC SSL disabled
26/07/02 18:05:28 INFO Utils: Successfully started service 'sparkDriver' on port 33475.
26/07/02 18:05:28 INFO SparkEnv: Registering MapOutputTracker
26/07/02 18:05:28 INFO SparkEnv: Registering BlockManagerMaster
26/07/02 18:05:28 INFO BlockManagerMasterEndpoint: Using org.apache.spark.storage.DefaultTopologyMapper for getting topology information
26/07/02 18:05:28 INFO BlockManagerMasterEndpoint: BlockManagerMasterEndpoint up
26/07/02 18:05:28 INFO SparkEnv: Registering BlockManagerMasterHeartbeat
26/07/02 18:05:28 INFO DiskBlockManager: Created local directory at /tmp/blockmgr-05dbefdb-7e1e-4133-b721-4592dd7bfe8e
26/07/02 18:05:28 INFO SparkEnv: Registering OutputCommitCoordinator
26/07/02 18:05:28 INFO JettyUtils: Start Jetty 0.0.0.0:4040 for SparkUI
26/07/02 18:05:28 INFO Utils: Successfully started service 'SparkUI' on port 4040.
26/07/02 18:05:28 INFO ResourceProfile: Default ResourceProfile created, executor resources: Map(cores -> name: cores, amount: 1, script: , vendor: , memory -> name: memory, amount: 1024, script: , vendor: , offHeap -> name: offHeap, amount: 0, script: , vendor: ), task resources: Map(cpus -> name: cpus, amount: 1.0)
26/07/02 18:05:28 INFO ResourceProfile: Limiting resource is cpu
26/07/02 18:05:28 INFO ResourceProfileManager: Added ResourceProfile id: 0
26/07/02 18:05:28 INFO SecurityManager: Changing view acls to: sohang
26/07/02 18:05:28 INFO SecurityManager: Changing modify acls to: sohang
26/07/02 18:05:28 INFO SecurityManager: Changing view acls groups to: sohang
26/07/02 18:05:28 INFO SecurityManager: Changing modify acls groups to: sohang
26/07/02 18:05:28 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: sohang groups with view permissions: EMPTY; users with modify permissions: sohang; groups with modify permissions: EMPTY; RPC SSL disabled
26/07/02 18:05:28 INFO Executor: Starting executor ID driver on host 192.168.1.31
26/07/02 18:05:28 INFO Executor: OS info Linux, 7.0.0-27-generic, amd64
26/07/02 18:05:28 INFO Executor: Java version 17.0.19+10-1-26.04.2-Ubuntu
26/07/02 18:05:28 INFO Executor: Starting executor with user classpath (userClassPathFirst = false): ''
26/07/02 18:05:28 INFO Executor: Created or updated repl class loader org.apache.spark.util.MutableURLClassLoader@3c11392d for default.
26/07/02 18:05:28 INFO Utils: Successfully started service 'org.apache.spark.network.netty.NettyBlockTransferService' on port 38009.
26/07/02 18:05:28 INFO NettyBlockTransferService: Server created on 192.168.1.31:38009
26/07/02 18:05:28 INFO BlockManager: Using org.apache.spark.storage.RandomBlockReplicationPolicy for block replication policy
26/07/02 18:05:28 INFO BlockManagerMaster: Registering BlockManager BlockManagerId(driver, 192.168.1.31, 38009, None)
26/07/02 18:05:28 INFO BlockManagerMasterEndpoint: Registering block manager 192.168.1.31:38009 with 434.4 MiB RAM, BlockManagerId(driver, 192.168.1.31, 38009, None)
26/07/02 18:05:28 INFO BlockManagerMaster: Registered BlockManager BlockManagerId(driver, 192.168.1.31, 38009, None)
26/07/02 18:05:28 INFO BlockManager: Initialized BlockManager: BlockManagerId(driver, 192.168.1.31, 38009, None)
INFO:__main__:Reading from Kafka topic: sensor_DA25M622
26/07/02 18:05:31 INFO SharedState: Setting hive.metastore.warehouse.dir ('null') to the value of spark.sql.warehouse.dir.
26/07/02 18:05:31 INFO SharedState: Warehouse path is 'file:/home/sohang/Projects/iit-madras-web-mtech-ai/trimester3/DA5402W_MLOPS/assignments/Assignment1/spark-warehouse'.
ERROR:__main__:Error in main: Failed to find data source: kafka. Please deploy the application as per the deployment section of Structured Streaming + Kafka Integration Guide.
Traceback (most recent call last):
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/trimester3/DA5402W_MLOPS/assignments/Assignment1/spark_streaming.py", line 241, in main
    df = read_from_kafka(
        spark, kafka_brokers="localhost:9092", topic="sensor_DA25M622"
    )
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/trimester3/DA5402W_MLOPS/assignments/Assignment1/spark_streaming.py", line 66, in read_from_kafka
    .load()
     ~~~~^^
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/.venv/lib/python3.14/site-packages/pyspark/python/lib/pyspark.zip/pyspark/sql/streaming/readwriter.py", line 307, in load
    return self._df(self._jreader.load())
                    ~~~~~~~~~~~~~~~~~~^^
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/.venv/lib/python3.14/site-packages/pyspark/python/lib/py4j-0.10.9.9-src.zip/py4j/java_gateway.py", line 1362, in __call__
    return_value = get_return_value(
        answer, self.gateway_client, self.target_id, self.name)
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/.venv/lib/python3.14/site-packages/pyspark/python/lib/pyspark.zip/pyspark/errors/exceptions/captured.py", line 269, in deco
    raise converted from None
pyspark.errors.exceptions.captured.AnalysisException: Failed to find data source: kafka. Please deploy the application as per the deployment section of Structured Streaming + Kafka Integration Guide.
26/07/02 18:05:32 INFO SparkContext: SparkContext is stopping with exitCode 0 from stop at NativeMethodAccessorImpl.java:0.
26/07/02 18:05:32 INFO SparkUI: Stopped Spark web UI at http://192.168.1.31:4040
26/07/02 18:05:32 INFO MapOutputTrackerMasterEndpoint: MapOutputTrackerMasterEndpoint stopped!
26/07/02 18:05:32 INFO MemoryStore: MemoryStore started with capacity 434.4 MiB
26/07/02 18:05:32 INFO MemoryStore: MemoryStore cleared
26/07/02 18:05:32 INFO BlockManager: BlockManager stopped
26/07/02 18:05:32 INFO BlockManagerMaster: BlockManagerMaster stopped
26/07/02 18:05:32 INFO OutputCommitCoordinator$OutputCommitCoordinatorEndpoint: OutputCommitCoordinator stopped!
26/07/02 18:05:32 INFO SparkContext: Successfully stopped SparkContext (Uptime: 4511 ms)
INFO:__main__:Spark session stopped.
INFO:py4j.clientserver:Closing down clientserver connection
```

spark connection seems to work i think, script error in pyspark :

```bash
$ spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 spark_streaming.py
WARNING: Using incubator modules: jdk.incubator.vector
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
26/07/03 18:31:35 WARN Utils: Your hostname, sohang-VivoBook-ASUS-Laptop-X510UFO, resolves to a loopback address: 127.0.1.1; using 192.168.1.31 instead (on interface wlp2s0)
26/07/03 18:31:35 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
:: loading settings :: url = jar:file:/home/sohang/Projects/iit-madras-web-mtech-ai/.venv/lib/python3.14/site-packages/pyspark/jars/ivy-2.5.3.jar!/org/apache/ivy/core/settings/ivysettings.xml
Ivy Default Cache set to: /home/sohang/.ivy2.5.2/cache
The jars for the packages stored in: /home/sohang/.ivy2.5.2/jars
org.apache.spark#spark-sql-kafka-0-10_2.12 added as a dependency
:: resolving dependencies :: org.apache.spark#spark-submit-parent-cd0bca9d-8efd-46af-a224-b796520fbab5;1.0
	confs: [default]
	found org.apache.spark#spark-sql-kafka-0-10_2.12;3.5.0 in central
	found org.apache.spark#spark-token-provider-kafka-0-10_2.12;3.5.0 in central
	found org.apache.kafka#kafka-clients;3.4.1 in central
	found org.lz4#lz4-java;1.8.0 in central
	found org.xerial.snappy#snappy-java;1.1.10.3 in central
	found org.slf4j#slf4j-api;2.0.7 in central
	found org.apache.hadoop#hadoop-client-runtime;3.3.4 in central
	found org.apache.hadoop#hadoop-client-api;3.3.4 in central
	found commons-logging#commons-logging;1.1.3 in central
	found com.google.code.findbugs#jsr305;3.0.0 in central
	found org.apache.commons#commons-pool2;2.11.1 in central
:: resolution report :: resolve 630ms :: artifacts dl 20ms
	:: modules in use:
	com.google.code.findbugs#jsr305;3.0.0 from central in [default]
	commons-logging#commons-logging;1.1.3 from central in [default]
	org.apache.commons#commons-pool2;2.11.1 from central in [default]
	org.apache.hadoop#hadoop-client-api;3.3.4 from central in [default]
	org.apache.hadoop#hadoop-client-runtime;3.3.4 from central in [default]
	org.apache.kafka#kafka-clients;3.4.1 from central in [default]
	org.apache.spark#spark-sql-kafka-0-10_2.12;3.5.0 from central in [default]
	org.apache.spark#spark-token-provider-kafka-0-10_2.12;3.5.0 from central in [default]
	org.lz4#lz4-java;1.8.0 from central in [default]
	org.slf4j#slf4j-api;2.0.7 from central in [default]
	org.xerial.snappy#snappy-java;1.1.10.3 from central in [default]
	---------------------------------------------------------------------
	|                  |            modules            ||   artifacts   |
	|       conf       | number| search|dwnlded|evicted|| number|dwnlded|
	---------------------------------------------------------------------
	|      default     |   11  |   0   |   0   |   0   ||   11  |   0   |
	---------------------------------------------------------------------
:: retrieving :: org.apache.spark#spark-submit-parent-cd0bca9d-8efd-46af-a224-b796520fbab5
	confs: [default]
	0 artifacts copied, 11 already retrieved (0kB/11ms)
26/07/03 18:31:36 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
26/07/03 18:31:38 INFO SparkContext: Running Spark version 4.1.2
26/07/03 18:31:38 INFO SparkContext: OS info Linux, 7.0.0-27-generic, amd64
26/07/03 18:31:38 INFO SparkContext: Java version 17.0.19+10-1-26.04.2-Ubuntu
26/07/03 18:31:38 INFO ResourceUtils: ==============================================================
26/07/03 18:31:38 INFO ResourceUtils: No custom resources configured for spark.driver.
26/07/03 18:31:38 INFO ResourceUtils: ==============================================================
26/07/03 18:31:38 INFO SparkContext: Submitted application: SensorStreamingPipeline
26/07/03 18:31:38 INFO SecurityManager: Changing view acls to: sohang
26/07/03 18:31:38 INFO SecurityManager: Changing modify acls to: sohang
26/07/03 18:31:38 INFO SecurityManager: Changing view acls groups to: sohang
26/07/03 18:31:38 INFO SecurityManager: Changing modify acls groups to: sohang
26/07/03 18:31:38 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: sohang groups with view permissions: EMPTY; users with modify permissions: sohang; groups with modify permissions: EMPTY; RPC SSL disabled
26/07/03 18:31:38 INFO Utils: Successfully started service 'sparkDriver' on port 45933.
26/07/03 18:31:38 INFO SparkEnv: Registering MapOutputTracker
26/07/03 18:31:38 INFO SparkEnv: Registering BlockManagerMaster
26/07/03 18:31:38 INFO BlockManagerMasterEndpoint: Using org.apache.spark.storage.DefaultTopologyMapper for getting topology information
26/07/03 18:31:38 INFO BlockManagerMasterEndpoint: BlockManagerMasterEndpoint up
26/07/03 18:31:38 INFO SparkEnv: Registering BlockManagerMasterHeartbeat
26/07/03 18:31:38 INFO DiskBlockManager: Created local directory at /tmp/blockmgr-b1d47923-d948-4f60-adb9-d64f6a694c39
26/07/03 18:31:38 INFO SparkEnv: Registering OutputCommitCoordinator
26/07/03 18:31:39 INFO JettyUtils: Start Jetty 0.0.0.0:4040 for SparkUI
26/07/03 18:31:39 INFO Utils: Successfully started service 'SparkUI' on port 4040.
26/07/03 18:31:39 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.0.jar at spark://192.168.1.31:45933/jars/org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.0.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.5.0.jar at spark://192.168.1.31:45933/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.5.0.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.4.1.jar at spark://192.168.1.31:45933/jars/org.apache.kafka_kafka-clients-3.4.1.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar at spark://192.168.1.31:45933/jars/com.google.code.findbugs_jsr305-3.0.0.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.11.1.jar at spark://192.168.1.31:45933/jars/org.apache.commons_commons-pool2-2.11.1.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.3.4.jar at spark://192.168.1.31:45933/jars/org.apache.hadoop_hadoop-client-runtime-3.3.4.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar at spark://192.168.1.31:45933/jars/org.lz4_lz4-java-1.8.0.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.3.jar at spark://192.168.1.31:45933/jars/org.xerial.snappy_snappy-java-1.1.10.3.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.7.jar at spark://192.168.1.31:45933/jars/org.slf4j_slf4j-api-2.0.7.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.3.4.jar at spark://192.168.1.31:45933/jars/org.apache.hadoop_hadoop-client-api-3.3.4.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/commons-logging_commons-logging-1.1.3.jar at spark://192.168.1.31:45933/jars/commons-logging_commons-logging-1.1.3.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.0.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.0.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.0.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.0.jar
26/07/03 18:31:39 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.5.0.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.5.0.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.5.0.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.5.0.jar
26/07/03 18:31:39 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.4.1.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.4.1.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.4.1.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.kafka_kafka-clients-3.4.1.jar
26/07/03 18:31:39 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar at file:///home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/com.google.code.findbugs_jsr305-3.0.0.jar
26/07/03 18:31:39 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.11.1.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.11.1.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.11.1.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.commons_commons-pool2-2.11.1.jar
26/07/03 18:31:39 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.3.4.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.3.4.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.3.4.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.hadoop_hadoop-client-runtime-3.3.4.jar
26/07/03 18:31:39 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar at file:///home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.lz4_lz4-java-1.8.0.jar
26/07/03 18:31:39 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.3.jar at file:///home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.3.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.3.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.xerial.snappy_snappy-java-1.1.10.3.jar
26/07/03 18:31:39 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.7.jar at file:///home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.7.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.7.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.slf4j_slf4j-api-2.0.7.jar
26/07/03 18:31:39 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.3.4.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.3.4.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.3.4.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.hadoop_hadoop-client-api-3.3.4.jar
26/07/03 18:31:39 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/commons-logging_commons-logging-1.1.3.jar at file:///home/sohang/.ivy2.5.2/jars/commons-logging_commons-logging-1.1.3.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/commons-logging_commons-logging-1.1.3.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/commons-logging_commons-logging-1.1.3.jar
26/07/03 18:31:39 INFO ResourceProfile: Default ResourceProfile created, executor resources: Map(cores -> name: cores, amount: 1, script: , vendor: , memory -> name: memory, amount: 1024, script: , vendor: , offHeap -> name: offHeap, amount: 0, script: , vendor: ), task resources: Map(cpus -> name: cpus, amount: 1.0)
26/07/03 18:31:39 INFO ResourceProfile: Limiting resource is cpu
26/07/03 18:31:39 INFO ResourceProfileManager: Added ResourceProfile id: 0
26/07/03 18:31:39 INFO SecurityManager: Changing view acls to: sohang
26/07/03 18:31:39 INFO SecurityManager: Changing modify acls to: sohang
26/07/03 18:31:39 INFO SecurityManager: Changing view acls groups to: sohang
26/07/03 18:31:39 INFO SecurityManager: Changing modify acls groups to: sohang
26/07/03 18:31:39 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: sohang groups with view permissions: EMPTY; users with modify permissions: sohang; groups with modify permissions: EMPTY; RPC SSL disabled
26/07/03 18:31:39 INFO Executor: Starting executor ID driver on host 192.168.1.31
26/07/03 18:31:39 INFO Executor: OS info Linux, 7.0.0-27-generic, amd64
26/07/03 18:31:39 INFO Executor: Java version 17.0.19+10-1-26.04.2-Ubuntu
26/07/03 18:31:39 INFO Executor: Starting executor with user classpath (userClassPathFirst = false): ''
26/07/03 18:31:39 INFO Executor: Created or updated repl class loader org.apache.spark.util.MutableURLClassLoader@5dc88b55 for default.
26/07/03 18:31:39 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.3.4.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.3.4.jar has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.hadoop_hadoop-client-api-3.3.4.jar
26/07/03 18:31:39 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.0.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.0.jar has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.0.jar
26/07/03 18:31:39 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.7.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.7.jar has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.slf4j_slf4j-api-2.0.7.jar
26/07/03 18:31:39 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.4.1.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.4.1.jar has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.kafka_kafka-clients-3.4.1.jar
26/07/03 18:31:39 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.3.4.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.3.4.jar has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.hadoop_hadoop-client-runtime-3.3.4.jar
26/07/03 18:31:39 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.lz4_lz4-java-1.8.0.jar
26/07/03 18:31:39 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/commons-logging_commons-logging-1.1.3.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: /home/sohang/.ivy2.5.2/jars/commons-logging_commons-logging-1.1.3.jar has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/commons-logging_commons-logging-1.1.3.jar
26/07/03 18:31:39 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: /home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/com.google.code.findbugs_jsr305-3.0.0.jar
26/07/03 18:31:39 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.11.1.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.11.1.jar has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.commons_commons-pool2-2.11.1.jar
26/07/03 18:31:39 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.5.0.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.5.0.jar has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.5.0.jar
26/07/03 18:31:39 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.3.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.3.jar has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.xerial.snappy_snappy-java-1.1.10.3.jar
26/07/03 18:31:39 INFO Executor: Fetching spark://192.168.1.31:45933/jars/org.apache.hadoop_hadoop-client-api-3.3.4.jar with timestamp 1783083698376
26/07/03 18:31:39 INFO TransportClientFactory: Successfully created connection to /192.168.1.31:45933 after 36 ms (0 ms spent in bootstraps)
26/07/03 18:31:39 INFO Utils: Fetching spark://192.168.1.31:45933/jars/org.apache.hadoop_hadoop-client-api-3.3.4.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp8766433921583860622.tmp
26/07/03 18:31:40 INFO Utils: /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp8766433921583860622.tmp has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.hadoop_hadoop-client-api-3.3.4.jar
26/07/03 18:31:40 INFO Executor: Adding file:/tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.hadoop_hadoop-client-api-3.3.4.jar to class loader default
26/07/03 18:31:40 INFO Executor: Fetching spark://192.168.1.31:45933/jars/com.google.code.findbugs_jsr305-3.0.0.jar with timestamp 1783083698376
26/07/03 18:31:40 INFO Utils: Fetching spark://192.168.1.31:45933/jars/com.google.code.findbugs_jsr305-3.0.0.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp4657485589745262370.tmp
26/07/03 18:31:40 INFO Utils: /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp4657485589745262370.tmp has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/com.google.code.findbugs_jsr305-3.0.0.jar
26/07/03 18:31:40 INFO Executor: Adding file:/tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/com.google.code.findbugs_jsr305-3.0.0.jar to class loader default
26/07/03 18:31:40 INFO Executor: Fetching spark://192.168.1.31:45933/jars/commons-logging_commons-logging-1.1.3.jar with timestamp 1783083698376
26/07/03 18:31:40 INFO Utils: Fetching spark://192.168.1.31:45933/jars/commons-logging_commons-logging-1.1.3.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp7418253701298262177.tmp
26/07/03 18:31:40 INFO Utils: /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp7418253701298262177.tmp has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/commons-logging_commons-logging-1.1.3.jar
26/07/03 18:31:40 INFO Executor: Adding file:/tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/commons-logging_commons-logging-1.1.3.jar to class loader default
26/07/03 18:31:40 INFO Executor: Fetching spark://192.168.1.31:45933/jars/org.lz4_lz4-java-1.8.0.jar with timestamp 1783083698376
26/07/03 18:31:40 INFO Utils: Fetching spark://192.168.1.31:45933/jars/org.lz4_lz4-java-1.8.0.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp1385273656919957589.tmp
26/07/03 18:31:40 INFO Utils: /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp1385273656919957589.tmp has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.lz4_lz4-java-1.8.0.jar
26/07/03 18:31:40 INFO Executor: Adding file:/tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.lz4_lz4-java-1.8.0.jar to class loader default
26/07/03 18:31:40 INFO Executor: Fetching spark://192.168.1.31:45933/jars/org.apache.hadoop_hadoop-client-runtime-3.3.4.jar with timestamp 1783083698376
26/07/03 18:31:40 INFO Utils: Fetching spark://192.168.1.31:45933/jars/org.apache.hadoop_hadoop-client-runtime-3.3.4.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp8582326178397227633.tmp
26/07/03 18:31:40 INFO Utils: /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp8582326178397227633.tmp has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.hadoop_hadoop-client-runtime-3.3.4.jar
26/07/03 18:31:40 INFO Executor: Adding file:/tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.hadoop_hadoop-client-runtime-3.3.4.jar to class loader default
26/07/03 18:31:40 INFO Executor: Fetching spark://192.168.1.31:45933/jars/org.apache.commons_commons-pool2-2.11.1.jar with timestamp 1783083698376
26/07/03 18:31:40 INFO Utils: Fetching spark://192.168.1.31:45933/jars/org.apache.commons_commons-pool2-2.11.1.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp16276644883788196119.tmp
26/07/03 18:31:40 INFO Utils: /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp16276644883788196119.tmp has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.commons_commons-pool2-2.11.1.jar
26/07/03 18:31:40 INFO Executor: Adding file:/tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.commons_commons-pool2-2.11.1.jar to class loader default
26/07/03 18:31:40 INFO Executor: Fetching spark://192.168.1.31:45933/jars/org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.0.jar with timestamp 1783083698376
26/07/03 18:31:40 INFO Utils: Fetching spark://192.168.1.31:45933/jars/org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.0.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp13608990841320843703.tmp
26/07/03 18:31:40 INFO Utils: /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp13608990841320843703.tmp has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.0.jar
26/07/03 18:31:40 INFO Executor: Adding file:/tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.0.jar to class loader default
26/07/03 18:31:40 INFO Executor: Fetching spark://192.168.1.31:45933/jars/org.xerial.snappy_snappy-java-1.1.10.3.jar with timestamp 1783083698376
26/07/03 18:31:40 INFO Utils: Fetching spark://192.168.1.31:45933/jars/org.xerial.snappy_snappy-java-1.1.10.3.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp16185125374034601864.tmp
26/07/03 18:31:40 INFO Utils: /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp16185125374034601864.tmp has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.xerial.snappy_snappy-java-1.1.10.3.jar
26/07/03 18:31:40 INFO Executor: Adding file:/tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.xerial.snappy_snappy-java-1.1.10.3.jar to class loader default
26/07/03 18:31:40 INFO Executor: Fetching spark://192.168.1.31:45933/jars/org.slf4j_slf4j-api-2.0.7.jar with timestamp 1783083698376
26/07/03 18:31:40 INFO Utils: Fetching spark://192.168.1.31:45933/jars/org.slf4j_slf4j-api-2.0.7.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp10934963532842149746.tmp
26/07/03 18:31:40 INFO Utils: /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp10934963532842149746.tmp has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.slf4j_slf4j-api-2.0.7.jar
26/07/03 18:31:40 INFO Executor: Adding file:/tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.slf4j_slf4j-api-2.0.7.jar to class loader default
26/07/03 18:31:40 INFO Executor: Fetching spark://192.168.1.31:45933/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.5.0.jar with timestamp 1783083698376
26/07/03 18:31:40 INFO Utils: Fetching spark://192.168.1.31:45933/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.5.0.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp13551121568036299231.tmp
26/07/03 18:31:40 INFO Utils: /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp13551121568036299231.tmp has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.5.0.jar
26/07/03 18:31:40 INFO Executor: Adding file:/tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.5.0.jar to class loader default
26/07/03 18:31:40 INFO Executor: Fetching spark://192.168.1.31:45933/jars/org.apache.kafka_kafka-clients-3.4.1.jar with timestamp 1783083698376
26/07/03 18:31:40 INFO Utils: Fetching spark://192.168.1.31:45933/jars/org.apache.kafka_kafka-clients-3.4.1.jar to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp12924214141203237367.tmp
26/07/03 18:31:40 INFO Utils: /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/fetchFileTemp12924214141203237367.tmp has been previously copied to /tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.kafka_kafka-clients-3.4.1.jar
26/07/03 18:31:40 INFO Executor: Adding file:/tmp/spark-9e4b3785-211a-4e76-96d6-ceb270edcb41/userFiles-34390cc2-99cf-43ca-8859-ba8f9860018f/org.apache.kafka_kafka-clients-3.4.1.jar to class loader default
26/07/03 18:31:40 INFO Utils: Successfully started service 'org.apache.spark.network.netty.NettyBlockTransferService' on port 39771.
26/07/03 18:31:40 INFO NettyBlockTransferService: Server created on 192.168.1.31:39771
26/07/03 18:31:40 INFO BlockManager: Using org.apache.spark.storage.RandomBlockReplicationPolicy for block replication policy
26/07/03 18:31:40 INFO BlockManagerMaster: Registering BlockManager BlockManagerId(driver, 192.168.1.31, 39771, None)
26/07/03 18:31:40 INFO BlockManagerMasterEndpoint: Registering block manager 192.168.1.31:39771 with 434.4 MiB RAM, BlockManagerId(driver, 192.168.1.31, 39771, None)
26/07/03 18:31:40 INFO BlockManagerMaster: Registered BlockManager BlockManagerId(driver, 192.168.1.31, 39771, None)
26/07/03 18:31:40 INFO BlockManager: Initialized BlockManager: BlockManagerId(driver, 192.168.1.31, 39771, None)
INFO:__main__:Reading from Kafka topic: sensor_DA25M622
26/07/03 18:31:42 INFO SharedState: Setting hive.metastore.warehouse.dir ('null') to the value of spark.sql.warehouse.dir.
26/07/03 18:31:42 INFO SharedState: Warehouse path is 'file:/home/sohang/Projects/iit-madras-web-mtech-ai/trimester3/DA5402W_MLOPS/assignments/Assignment1/spark-warehouse'.
ERROR:__main__:Error in main: An error occurred while calling o40.load.
: java.lang.NoSuchMethodError: 'scala.collection.mutable.WrappedArray scala.Predef$.wrapRefArray(java.lang.Object[])'
	at org.apache.spark.sql.kafka010.KafkaSourceProvider$.<init>(KafkaSourceProvider.scala:545)
	at org.apache.spark.sql.kafka010.KafkaSourceProvider$.<clinit>(KafkaSourceProvider.scala)
	at org.apache.spark.sql.kafka010.KafkaSourceProvider.org$apache$spark$sql$kafka010$KafkaSourceProvider$$validateStreamOptions(KafkaSourceProvider.scala:338)
	at org.apache.spark.sql.kafka010.KafkaSourceProvider.sourceSchema(KafkaSourceProvider.scala:71)
	at org.apache.spark.sql.execution.datasources.DataSource.sourceSchema(DataSource.scala:247)
	at org.apache.spark.sql.execution.datasources.DataSource.sourceInfo$lzycompute(DataSource.scala:132)
	at org.apache.spark.sql.execution.datasources.DataSource.sourceInfo(DataSource.scala:132)
	at org.apache.spark.sql.execution.streaming.runtime.StreamingRelation$.apply(StreamingRelation.scala:38)
	at org.apache.spark.sql.catalyst.analysis.ResolveDataSource$$anonfun$apply$1.applyOrElse(ResolveDataSource.scala:86)
	at org.apache.spark.sql.catalyst.analysis.ResolveDataSource$$anonfun$apply$1.applyOrElse(ResolveDataSource.scala:45)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper.$anonfun$resolveOperatorsUpWithPruning$3(AnalysisHelper.scala:139)
	at org.apache.spark.sql.catalyst.trees.CurrentOrigin$.withOrigin(origin.scala:107)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper.$anonfun$resolveOperatorsUpWithPruning$1(AnalysisHelper.scala:139)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper$.allowInvokingTransformsInAnalyzer(AnalysisHelper.scala:416)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper.resolveOperatorsUpWithPruning(AnalysisHelper.scala:135)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper.resolveOperatorsUpWithPruning$(AnalysisHelper.scala:131)
	at org.apache.spark.sql.catalyst.plans.logical.LogicalPlan.resolveOperatorsUpWithPruning(LogicalPlan.scala:37)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper.resolveOperatorsUp(AnalysisHelper.scala:112)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper.resolveOperatorsUp$(AnalysisHelper.scala:111)
	at org.apache.spark.sql.catalyst.plans.logical.LogicalPlan.resolveOperatorsUp(LogicalPlan.scala:37)
	at org.apache.spark.sql.catalyst.analysis.ResolveDataSource.apply(ResolveDataSource.scala:45)
	at org.apache.spark.sql.catalyst.analysis.ResolveDataSource.apply(ResolveDataSource.scala:43)
	at org.apache.spark.sql.catalyst.rules.RuleExecutor.$anonfun$execute$2(RuleExecutor.scala:248)
	at scala.collection.LinearSeqOps.foldLeft(LinearSeq.scala:183)
	at scala.collection.LinearSeqOps.foldLeft$(LinearSeq.scala:179)
	at scala.collection.immutable.List.foldLeft(List.scala:79)
	at org.apache.spark.sql.catalyst.rules.RuleExecutor.$anonfun$execute$1(RuleExecutor.scala:245)
	at org.apache.spark.sql.catalyst.rules.RuleExecutor.$anonfun$execute$1$adapted(RuleExecutor.scala:237)
	at scala.collection.immutable.List.foreach(List.scala:323)
	at org.apache.spark.sql.catalyst.rules.RuleExecutor.execute(RuleExecutor.scala:237)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.org$apache$spark$sql$catalyst$analysis$Analyzer$$executeSameContext(Analyzer.scala:343)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.$anonfun$execute$1(Analyzer.scala:339)
	at org.apache.spark.sql.catalyst.analysis.AnalysisContext$.withNewAnalysisContext(Analyzer.scala:224)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.execute(Analyzer.scala:339)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.execute(Analyzer.scala:289)
	at org.apache.spark.sql.catalyst.rules.RuleExecutor.$anonfun$executeAndTrack$1(RuleExecutor.scala:207)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker$.withTracker(QueryPlanningTracker.scala:89)
	at org.apache.spark.sql.catalyst.rules.RuleExecutor.executeAndTrack(RuleExecutor.scala:207)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.resolveInFixedPoint(HybridAnalyzer.scala:236)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.$anonfun$apply$1(HybridAnalyzer.scala:91)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.withTrackedAnalyzerBridgeState(HybridAnalyzer.scala:122)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.apply(HybridAnalyzer.scala:84)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.$anonfun$executeAndCheck$1(Analyzer.scala:322)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper$.markInAnalyzer(AnalysisHelper.scala:423)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.executeAndCheck(Analyzer.scala:322)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$2(QueryExecution.scala:139)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker.measurePhase(QueryPlanningTracker.scala:148)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$2(QueryExecution.scala:330)
	at org.apache.spark.sql.execution.QueryExecution$.withInternalError(QueryExecution.scala:717)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$1(QueryExecution.scala:330)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:804)
	at org.apache.spark.sql.execution.QueryExecution.executePhase(QueryExecution.scala:329)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$1(QueryExecution.scala:139)
	at scala.util.Try$.apply(Try.scala:217)
	at org.apache.spark.util.Utils$.doTryWithCallerStacktrace(Utils.scala:1392)
	at org.apache.spark.util.LazyTry.tryT$lzycompute(LazyTry.scala:46)
	at org.apache.spark.util.LazyTry.tryT(LazyTry.scala:46)
	at org.apache.spark.util.LazyTry.get(LazyTry.scala:58)
	at org.apache.spark.sql.execution.QueryExecution.analyzed(QueryExecution.scala:150)
	at org.apache.spark.sql.execution.QueryExecution.assertAnalyzed(QueryExecution.scala:90)
	at org.apache.spark.sql.classic.Dataset$.$anonfun$ofRows$1(Dataset.scala:114)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:804)
	at org.apache.spark.sql.classic.Dataset$.ofRows(Dataset.scala:112)
	at org.apache.spark.sql.classic.DataStreamReader.loadInternal(DataStreamReader.scala:81)
	at org.apache.spark.sql.classic.DataStreamReader.load(DataStreamReader.scala:71)
	at org.apache.spark.sql.classic.DataStreamReader.load(DataStreamReader.scala:41)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.base/java.lang.reflect.Method.invoke(Method.java:569)
	at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
	at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)
	at py4j.Gateway.invoke(Gateway.java:282)
	at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
	at py4j.commands.CallCommand.execute(CallCommand.java:79)
	at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:184)
	at py4j.ClientServerConnection.run(ClientServerConnection.java:108)
	at java.base/java.lang.Thread.run(Thread.java:840)
Traceback (most recent call last):
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/trimester3/DA5402W_MLOPS/assignments/Assignment1/spark_streaming.py", line 243, in main
    df = read_from_kafka(
        spark, kafka_brokers="localhost:9092", topic="sensor_DA25M622"
    )
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/trimester3/DA5402W_MLOPS/assignments/Assignment1/spark_streaming.py", line 68, in read_from_kafka
    .load()
     ~~~~^^
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/.venv/lib/python3.14/site-packages/pyspark/python/lib/pyspark.zip/pyspark/sql/streaming/readwriter.py", line 307, in load
    return self._df(self._jreader.load())
                    ~~~~~~~~~~~~~~~~~~^^
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/.venv/lib/python3.14/site-packages/pyspark/python/lib/py4j-0.10.9.9-src.zip/py4j/java_gateway.py", line 1362, in __call__
    return_value = get_return_value(
        answer, self.gateway_client, self.target_id, self.name)
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/.venv/lib/python3.14/site-packages/pyspark/python/lib/pyspark.zip/pyspark/errors/exceptions/captured.py", line 263, in deco
    return f(*a, **kw)
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/.venv/lib/python3.14/site-packages/pyspark/python/lib/py4j-0.10.9.9-src.zip/py4j/protocol.py", line 327, in get_return_value
    raise Py4JJavaError(
        "An error occurred while calling {0}{1}{2}.\n".
        format(target_id, ".", name), value)
py4j.protocol.Py4JJavaError: An error occurred while calling o40.load.
: java.lang.NoSuchMethodError: 'scala.collection.mutable.WrappedArray scala.Predef$.wrapRefArray(java.lang.Object[])'
	at org.apache.spark.sql.kafka010.KafkaSourceProvider$.<init>(KafkaSourceProvider.scala:545)
	at org.apache.spark.sql.kafka010.KafkaSourceProvider$.<clinit>(KafkaSourceProvider.scala)
	at org.apache.spark.sql.kafka010.KafkaSourceProvider.org$apache$spark$sql$kafka010$KafkaSourceProvider$$validateStreamOptions(KafkaSourceProvider.scala:338)
	at org.apache.spark.sql.kafka010.KafkaSourceProvider.sourceSchema(KafkaSourceProvider.scala:71)
	at org.apache.spark.sql.execution.datasources.DataSource.sourceSchema(DataSource.scala:247)
	at org.apache.spark.sql.execution.datasources.DataSource.sourceInfo$lzycompute(DataSource.scala:132)
	at org.apache.spark.sql.execution.datasources.DataSource.sourceInfo(DataSource.scala:132)
	at org.apache.spark.sql.execution.streaming.runtime.StreamingRelation$.apply(StreamingRelation.scala:38)
	at org.apache.spark.sql.catalyst.analysis.ResolveDataSource$$anonfun$apply$1.applyOrElse(ResolveDataSource.scala:86)
	at org.apache.spark.sql.catalyst.analysis.ResolveDataSource$$anonfun$apply$1.applyOrElse(ResolveDataSource.scala:45)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper.$anonfun$resolveOperatorsUpWithPruning$3(AnalysisHelper.scala:139)
	at org.apache.spark.sql.catalyst.trees.CurrentOrigin$.withOrigin(origin.scala:107)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper.$anonfun$resolveOperatorsUpWithPruning$1(AnalysisHelper.scala:139)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper$.allowInvokingTransformsInAnalyzer(AnalysisHelper.scala:416)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper.resolveOperatorsUpWithPruning(AnalysisHelper.scala:135)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper.resolveOperatorsUpWithPruning$(AnalysisHelper.scala:131)
	at org.apache.spark.sql.catalyst.plans.logical.LogicalPlan.resolveOperatorsUpWithPruning(LogicalPlan.scala:37)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper.resolveOperatorsUp(AnalysisHelper.scala:112)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper.resolveOperatorsUp$(AnalysisHelper.scala:111)
	at org.apache.spark.sql.catalyst.plans.logical.LogicalPlan.resolveOperatorsUp(LogicalPlan.scala:37)
	at org.apache.spark.sql.catalyst.analysis.ResolveDataSource.apply(ResolveDataSource.scala:45)
	at org.apache.spark.sql.catalyst.analysis.ResolveDataSource.apply(ResolveDataSource.scala:43)
	at org.apache.spark.sql.catalyst.rules.RuleExecutor.$anonfun$execute$2(RuleExecutor.scala:248)
	at scala.collection.LinearSeqOps.foldLeft(LinearSeq.scala:183)
	at scala.collection.LinearSeqOps.foldLeft$(LinearSeq.scala:179)
	at scala.collection.immutable.List.foldLeft(List.scala:79)
	at org.apache.spark.sql.catalyst.rules.RuleExecutor.$anonfun$execute$1(RuleExecutor.scala:245)
	at org.apache.spark.sql.catalyst.rules.RuleExecutor.$anonfun$execute$1$adapted(RuleExecutor.scala:237)
	at scala.collection.immutable.List.foreach(List.scala:323)
	at org.apache.spark.sql.catalyst.rules.RuleExecutor.execute(RuleExecutor.scala:237)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.org$apache$spark$sql$catalyst$analysis$Analyzer$$executeSameContext(Analyzer.scala:343)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.$anonfun$execute$1(Analyzer.scala:339)
	at org.apache.spark.sql.catalyst.analysis.AnalysisContext$.withNewAnalysisContext(Analyzer.scala:224)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.execute(Analyzer.scala:339)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.execute(Analyzer.scala:289)
	at org.apache.spark.sql.catalyst.rules.RuleExecutor.$anonfun$executeAndTrack$1(RuleExecutor.scala:207)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker$.withTracker(QueryPlanningTracker.scala:89)
	at org.apache.spark.sql.catalyst.rules.RuleExecutor.executeAndTrack(RuleExecutor.scala:207)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.resolveInFixedPoint(HybridAnalyzer.scala:236)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.$anonfun$apply$1(HybridAnalyzer.scala:91)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.withTrackedAnalyzerBridgeState(HybridAnalyzer.scala:122)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.apply(HybridAnalyzer.scala:84)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.$anonfun$executeAndCheck$1(Analyzer.scala:322)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper$.markInAnalyzer(AnalysisHelper.scala:423)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.executeAndCheck(Analyzer.scala:322)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$2(QueryExecution.scala:139)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker.measurePhase(QueryPlanningTracker.scala:148)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$2(QueryExecution.scala:330)
	at org.apache.spark.sql.execution.QueryExecution$.withInternalError(QueryExecution.scala:717)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$1(QueryExecution.scala:330)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:804)
	at org.apache.spark.sql.execution.QueryExecution.executePhase(QueryExecution.scala:329)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$1(QueryExecution.scala:139)
	at scala.util.Try$.apply(Try.scala:217)
	at org.apache.spark.util.Utils$.doTryWithCallerStacktrace(Utils.scala:1392)
	at org.apache.spark.util.LazyTry.tryT$lzycompute(LazyTry.scala:46)
	at org.apache.spark.util.LazyTry.tryT(LazyTry.scala:46)
	at org.apache.spark.util.LazyTry.get(LazyTry.scala:58)
	at org.apache.spark.sql.execution.QueryExecution.analyzed(QueryExecution.scala:150)
	at org.apache.spark.sql.execution.QueryExecution.assertAnalyzed(QueryExecution.scala:90)
	at org.apache.spark.sql.classic.Dataset$.$anonfun$ofRows$1(Dataset.scala:114)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:804)
	at org.apache.spark.sql.classic.Dataset$.ofRows(Dataset.scala:112)
	at org.apache.spark.sql.classic.DataStreamReader.loadInternal(DataStreamReader.scala:81)
	at org.apache.spark.sql.classic.DataStreamReader.load(DataStreamReader.scala:71)
	at org.apache.spark.sql.classic.DataStreamReader.load(DataStreamReader.scala:41)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.base/java.lang.reflect.Method.invoke(Method.java:569)
	at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
	at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)
	at py4j.Gateway.invoke(Gateway.java:282)
	at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
	at py4j.commands.CallCommand.execute(CallCommand.java:79)
	at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:184)
	at py4j.ClientServerConnection.run(ClientServerConnection.java:108)
	at java.base/java.lang.Thread.run(Thread.java:840)

26/07/03 18:31:43 INFO SparkContext: SparkContext is stopping with exitCode 0 from stop at NativeMethodAccessorImpl.java:0.
26/07/03 18:31:43 INFO SparkUI: Stopped Spark web UI at http://192.168.1.31:4040
26/07/03 18:31:43 INFO MapOutputTrackerMasterEndpoint: MapOutputTrackerMasterEndpoint stopped!
26/07/03 18:31:43 INFO MemoryStore: MemoryStore started with capacity 434.4 MiB
26/07/03 18:31:43 INFO MemoryStore: MemoryStore cleared
26/07/03 18:31:43 INFO BlockManager: BlockManager stopped
26/07/03 18:31:43 INFO BlockManagerMaster: BlockManagerMaster stopped
26/07/03 18:31:43 INFO OutputCommitCoordinator$OutputCommitCoordinatorEndpoint: OutputCommitCoordinator stopped!
26/07/03 18:31:43 INFO SparkContext: Successfully stopped SparkContext (Uptime: 4925 ms)
INFO:__main__:Spark session stopped.
INFO:py4j.clientserver:Closing down clientserver connection
```

now spark connection to kafka seems spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.2 spark_streaming.py
WARNING: Using incubator modules: jdk.incubator.vector
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
26/07/03 18:41:33 WARN Utils: Your hostname, sohang-VivoBook-ASUS-Laptop-X510UFO, resolves to a loopback address: 127.0.1.1; using 192.168.1.31 instead (on interface wlp2s0)
26/07/03 18:41:33 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
:: loading settings :: url = jar:file:/home/sohang/Projects/iit-madras-web-mtech-ai/.venv/lib/python3.14/site-packages/pyspark/jars/ivy-2.5.3.jar!/org/apache/ivy/core/settings/ivysettings.xml
Ivy Default Cache set to: /home/sohang/.ivy2.5.2/cache
The jars for the packages stored in: /home/sohang/.ivy2.5.2/jars
org.apache.spark#spark-sql-kafka-0-10_2.13 added as a dependency
:: resolving dependencies :: org.apache.spark#spark-submit-parent-7915b52e-bcc5-480f-ba31-1c9884a03473;1.0
	confs: [default]
	found org.apache.spark#spark-sql-kafka-0-10_2.13;4.1.2 in central
	found org.apache.spark#spark-token-provider-kafka-0-10_2.13;4.1.2 in central
	found org.apache.kafka#kafka-clients;3.9.1 in central
	found org.lz4#lz4-java;1.8.0 in central
	found org.xerial.snappy#snappy-java;1.1.10.8 in central
	found org.slf4j#slf4j-api;2.0.17 in central
	found org.apache.hadoop#hadoop-client-runtime;3.4.2 in central
	found org.apache.hadoop#hadoop-client-api;3.4.2 in central
	found com.google.code.findbugs#jsr305;3.0.0 in central
	found org.scala-lang.modules#scala-parallel-collections_2.13;1.2.0 in central
	found org.apache.commons#commons-pool2;2.12.1 in central
downloading https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.13/4.1.2/spark-sql-kafka-0-10_2.13-4.1.2.jar ...
	[SUCCESSFUL ] org.apache.spark#spark-sql-kafka-0-10_2.13;4.1.2!spark-sql-kafka-0-10_2.13.jar (202ms)
downloading https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.13/4.1.2/spark-token-provider-kafka-0-10_2.13-4.1.2.jar ...
	[SUCCESSFUL ] org.apache.spark#spark-token-provider-kafka-0-10_2.13;4.1.2!spark-token-provider-kafka-0-10_2.13.jar (229ms)
downloading https://repo1.maven.org/maven2/org/scala-lang/modules/scala-parallel-collections_2.13/1.2.0/scala-parallel-collections_2.13-1.2.0.jar ...
	[SUCCESSFUL ] org.scala-lang.modules#scala-parallel-collections_2.13;1.2.0!scala-parallel-collections_2.13.jar (153ms)
downloading https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.9.1/kafka-clients-3.9.1.jar ...
	[SUCCESSFUL ] org.apache.kafka#kafka-clients;3.9.1!kafka-clients.jar (1448ms)
downloading https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.12.1/commons-pool2-2.12.1.jar ...
	[SUCCESSFUL ] org.apache.commons#commons-pool2;2.12.1!commons-pool2.jar (83ms)
downloading https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-client-runtime/3.4.2/hadoop-client-runtime-3.4.2.jar ...
	[SUCCESSFUL ] org.apache.hadoop#hadoop-client-runtime;3.4.2!hadoop-client-runtime.jar (6433ms)
downloading https://repo1.maven.org/maven2/org/xerial/snappy/snappy-java/1.1.10.8/snappy-java-1.1.10.8.jar ...
	[SUCCESSFUL ] org.xerial.snappy#snappy-java;1.1.10.8!snappy-java.jar(bundle) (480ms)
downloading https://repo1.maven.org/maven2/org/slf4j/slf4j-api/2.0.17/slf4j-api-2.0.17.jar ...
	[SUCCESSFUL ] org.slf4j#slf4j-api;2.0.17!slf4j-api.jar (71ms)
downloading https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-client-api/3.4.2/hadoop-client-api-3.4.2.jar ...
	[SUCCESSFUL ] org.apache.hadoop#hadoop-client-api;3.4.2!hadoop-client-api.jar (3952ms)
:: resolution report :: resolve 15564ms :: artifacts dl 13069ms
	:: modules in use:
	com.google.code.findbugs#jsr305;3.0.0 from central in [default]
	org.apache.commons#commons-pool2;2.12.1 from central in [default]
	org.apache.hadoop#hadoop-client-api;3.4.2 from central in [default]
	org.apache.hadoop#hadoop-client-runtime;3.4.2 from central in [default]
	org.apache.kafka#kafka-clients;3.9.1 from central in [default]
	org.apache.spark#spark-sql-kafka-0-10_2.13;4.1.2 from central in [default]
	org.apache.spark#spark-token-provider-kafka-0-10_2.13;4.1.2 from central in [default]
	org.lz4#lz4-java;1.8.0 from central in [default]
	org.scala-lang.modules#scala-parallel-collections_2.13;1.2.0 from central in [default]
	org.slf4j#slf4j-api;2.0.17 from central in [default]
	org.xerial.snappy#snappy-java;1.1.10.8 from central in [default]
	---------------------------------------------------------------------
	|                  |            modules            ||   artifacts   |
	|       conf       | number| search|dwnlded|evicted|| number|dwnlded|
	---------------------------------------------------------------------
	|      default     |   11  |   9   |   9   |   0   ||   11  |   9   |
	---------------------------------------------------------------------
:: retrieving :: org.apache.spark#spark-submit-parent-7915b52e-bcc5-480f-ba31-1c9884a03473
	confs: [default]
	9 artifacts copied, 2 already retrieved (62237kB/64ms)
26/07/03 18:42:02 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
26/07/03 18:42:04 INFO SparkContext: Running Spark version 4.1.2
26/07/03 18:42:04 INFO SparkContext: OS info Linux, 7.0.0-27-generic, amd64
26/07/03 18:42:04 INFO SparkContext: Java version 17.0.19+10-1-26.04.2-Ubuntu
26/07/03 18:42:04 INFO ResourceUtils: ==============================================================
26/07/03 18:42:04 INFO ResourceUtils: No custom resources configured for spark.driver.
26/07/03 18:42:04 INFO ResourceUtils: ==============================================================
26/07/03 18:42:04 INFO SparkContext: Submitted application: SensorStreamingPipeline
26/07/03 18:42:04 INFO SecurityManager: Changing view acls to: sohang
26/07/03 18:42:04 INFO SecurityManager: Changing modify acls to: sohang
26/07/03 18:42:04 INFO SecurityManager: Changing view acls groups to: sohang
26/07/03 18:42:04 INFO SecurityManager: Changing modify acls groups to: sohang
26/07/03 18:42:04 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: sohang groups with view permissions: EMPTY; users with modify permissions: sohang; groups with modify permissions: EMPTY; RPC SSL disabled
26/07/03 18:42:04 INFO Utils: Successfully started service 'sparkDriver' on port 36241.
26/07/03 18:42:04 INFO SparkEnv: Registering MapOutputTracker
26/07/03 18:42:04 INFO SparkEnv: Registering BlockManagerMaster
26/07/03 18:42:04 INFO BlockManagerMasterEndpoint: Using org.apache.spark.storage.DefaultTopologyMapper for getting topology information
26/07/03 18:42:04 INFO BlockManagerMasterEndpoint: BlockManagerMasterEndpoint up
26/07/03 18:42:04 INFO SparkEnv: Registering BlockManagerMasterHeartbeat
26/07/03 18:42:04 INFO DiskBlockManager: Created local directory at /tmp/blockmgr-31b38d1a-29fe-4d70-a851-eebb791f2b27
26/07/03 18:42:04 INFO SparkEnv: Registering OutputCommitCoordinator
26/07/03 18:42:05 INFO JettyUtils: Start Jetty 0.0.0.0:4040 for SparkUI
26/07/03 18:42:05 INFO Utils: Successfully started service 'SparkUI' on port 4040.
26/07/03 18:42:05 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar at spark://192.168.1.31:36241/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar at spark://192.168.1.31:36241/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar at spark://192.168.1.31:36241/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.9.1.jar at spark://192.168.1.31:36241/jars/org.apache.kafka_kafka-clients-3.9.1.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar at spark://192.168.1.31:36241/jars/com.google.code.findbugs_jsr305-3.0.0.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.12.1.jar at spark://192.168.1.31:36241/jars/org.apache.commons_commons-pool2-2.12.1.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar at spark://192.168.1.31:36241/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar at spark://192.168.1.31:36241/jars/org.lz4_lz4-java-1.8.0.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar at spark://192.168.1.31:36241/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.17.jar at spark://192.168.1.31:36241/jars/org.slf4j_slf4j-api-2.0.17.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar at spark://192.168.1.31:36241/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar
26/07/03 18:42:05 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar
26/07/03 18:42:05 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar at file:///home/sohang/.ivy2.5.2/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar
26/07/03 18:42:05 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.9.1.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.9.1.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.9.1.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.kafka_kafka-clients-3.9.1.jar
26/07/03 18:42:05 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar at file:///home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/com.google.code.findbugs_jsr305-3.0.0.jar
26/07/03 18:42:05 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.12.1.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.12.1.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.12.1.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.commons_commons-pool2-2.12.1.jar
26/07/03 18:42:05 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar
26/07/03 18:42:05 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar at file:///home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.lz4_lz4-java-1.8.0.jar
26/07/03 18:42:05 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar at file:///home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.xerial.snappy_snappy-java-1.1.10.8.jar
26/07/03 18:42:05 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.17.jar at file:///home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.17.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.17.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.slf4j_slf4j-api-2.0.17.jar
26/07/03 18:42:05 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.hadoop_hadoop-client-api-3.4.2.jar
26/07/03 18:42:05 INFO ResourceProfile: Default ResourceProfile created, executor resources: Map(cores -> name: cores, amount: 1, script: , vendor: , memory -> name: memory, amount: 1024, script: , vendor: , offHeap -> name: offHeap, amount: 0, script: , vendor: ), task resources: Map(cpus -> name: cpus, amount: 1.0)
26/07/03 18:42:05 INFO ResourceProfile: Limiting resource is cpu
26/07/03 18:42:05 INFO ResourceProfileManager: Added ResourceProfile id: 0
26/07/03 18:42:05 INFO SecurityManager: Changing view acls to: sohang
26/07/03 18:42:05 INFO SecurityManager: Changing modify acls to: sohang
26/07/03 18:42:05 INFO SecurityManager: Changing view acls groups to: sohang
26/07/03 18:42:05 INFO SecurityManager: Changing modify acls groups to: sohang
26/07/03 18:42:05 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: sohang groups with view permissions: EMPTY; users with modify permissions: sohang; groups with modify permissions: EMPTY; RPC SSL disabled
26/07/03 18:42:05 INFO Executor: Starting executor ID driver on host 192.168.1.31
26/07/03 18:42:05 INFO Executor: OS info Linux, 7.0.0-27-generic, amd64
26/07/03 18:42:05 INFO Executor: Java version 17.0.19+10-1-26.04.2-Ubuntu
26/07/03 18:42:05 INFO Executor: Starting executor with user classpath (userClassPathFirst = false): ''
26/07/03 18:42:05 INFO Executor: Created or updated repl class loader org.apache.spark.util.MutableURLClassLoader@2610493c for default.
26/07/03 18:42:05 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar
26/07/03 18:42:05 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.17.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.17.jar has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.slf4j_slf4j-api-2.0.17.jar
26/07/03 18:42:05 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar
26/07/03 18:42:05 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.12.1.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.12.1.jar has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.commons_commons-pool2-2.12.1.jar
26/07/03 18:42:05 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar
26/07/03 18:42:05 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.lz4_lz4-java-1.8.0.jar
26/07/03 18:42:05 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.xerial.snappy_snappy-java-1.1.10.8.jar
26/07/03 18:42:05 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: /home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/com.google.code.findbugs_jsr305-3.0.0.jar
26/07/03 18:42:05 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar
26/07/03 18:42:05 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.9.1.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.9.1.jar has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.kafka_kafka-clients-3.9.1.jar
26/07/03 18:42:05 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.hadoop_hadoop-client-api-3.4.2.jar
26/07/03 18:42:05 INFO Executor: Fetching spark://192.168.1.31:36241/jars/org.slf4j_slf4j-api-2.0.17.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO TransportClientFactory: Successfully created connection to /192.168.1.31:36241 after 25 ms (0 ms spent in bootstraps)
26/07/03 18:42:05 INFO Utils: Fetching spark://192.168.1.31:36241/jars/org.slf4j_slf4j-api-2.0.17.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp9933980758755597880.tmp
26/07/03 18:42:05 INFO Utils: /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp9933980758755597880.tmp has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.slf4j_slf4j-api-2.0.17.jar
26/07/03 18:42:05 INFO Executor: Adding file:/tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.slf4j_slf4j-api-2.0.17.jar to class loader default
26/07/03 18:42:05 INFO Executor: Fetching spark://192.168.1.31:36241/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Fetching spark://192.168.1.31:36241/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp13729946833083084832.tmp
26/07/03 18:42:05 INFO Utils: /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp13729946833083084832.tmp has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar
26/07/03 18:42:05 INFO Executor: Adding file:/tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar to class loader default
26/07/03 18:42:05 INFO Executor: Fetching spark://192.168.1.31:36241/jars/org.apache.kafka_kafka-clients-3.9.1.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Fetching spark://192.168.1.31:36241/jars/org.apache.kafka_kafka-clients-3.9.1.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp15939142686444608850.tmp
26/07/03 18:42:05 INFO Utils: /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp15939142686444608850.tmp has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.kafka_kafka-clients-3.9.1.jar
26/07/03 18:42:05 INFO Executor: Adding file:/tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.kafka_kafka-clients-3.9.1.jar to class loader default
26/07/03 18:42:05 INFO Executor: Fetching spark://192.168.1.31:36241/jars/org.apache.commons_commons-pool2-2.12.1.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Fetching spark://192.168.1.31:36241/jars/org.apache.commons_commons-pool2-2.12.1.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp7785610186872243162.tmp
26/07/03 18:42:05 INFO Utils: /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp7785610186872243162.tmp has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.commons_commons-pool2-2.12.1.jar
26/07/03 18:42:05 INFO Executor: Adding file:/tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.commons_commons-pool2-2.12.1.jar to class loader default
26/07/03 18:42:05 INFO Executor: Fetching spark://192.168.1.31:36241/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Fetching spark://192.168.1.31:36241/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp7507059557451733453.tmp
26/07/03 18:42:05 INFO Utils: /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp7507059557451733453.tmp has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar
26/07/03 18:42:05 INFO Executor: Adding file:/tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar to class loader default
26/07/03 18:42:05 INFO Executor: Fetching spark://192.168.1.31:36241/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar with timestamp 1783084324446
26/07/03 18:42:05 INFO Utils: Fetching spark://192.168.1.31:36241/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp5340574888738971557.tmp
26/07/03 18:42:06 INFO Utils: /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp5340574888738971557.tmp has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.hadoop_hadoop-client-api-3.4.2.jar
26/07/03 18:42:06 INFO Executor: Adding file:/tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.hadoop_hadoop-client-api-3.4.2.jar to class loader default
26/07/03 18:42:06 INFO Executor: Fetching spark://192.168.1.31:36241/jars/org.lz4_lz4-java-1.8.0.jar with timestamp 1783084324446
26/07/03 18:42:06 INFO Utils: Fetching spark://192.168.1.31:36241/jars/org.lz4_lz4-java-1.8.0.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp8040520470659239729.tmp
26/07/03 18:42:06 INFO Utils: /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp8040520470659239729.tmp has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.lz4_lz4-java-1.8.0.jar
26/07/03 18:42:06 INFO Executor: Adding file:/tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.lz4_lz4-java-1.8.0.jar to class loader default
26/07/03 18:42:06 INFO Executor: Fetching spark://192.168.1.31:36241/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084324446
26/07/03 18:42:06 INFO Utils: Fetching spark://192.168.1.31:36241/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp17037191835440022812.tmp
26/07/03 18:42:06 INFO Utils: /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp17037191835440022812.tmp has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar
26/07/03 18:42:06 INFO Executor: Adding file:/tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar to class loader default
26/07/03 18:42:06 INFO Executor: Fetching spark://192.168.1.31:36241/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar with timestamp 1783084324446
26/07/03 18:42:06 INFO Utils: Fetching spark://192.168.1.31:36241/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp3357119598409106264.tmp
26/07/03 18:42:06 INFO Utils: /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp3357119598409106264.tmp has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.xerial.snappy_snappy-java-1.1.10.8.jar
26/07/03 18:42:06 INFO Executor: Adding file:/tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.xerial.snappy_snappy-java-1.1.10.8.jar to class loader default
26/07/03 18:42:06 INFO Executor: Fetching spark://192.168.1.31:36241/jars/com.google.code.findbugs_jsr305-3.0.0.jar with timestamp 1783084324446
26/07/03 18:42:06 INFO Utils: Fetching spark://192.168.1.31:36241/jars/com.google.code.findbugs_jsr305-3.0.0.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp8767752114729254070.tmp
26/07/03 18:42:06 INFO Utils: /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp8767752114729254070.tmp has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/com.google.code.findbugs_jsr305-3.0.0.jar
26/07/03 18:42:06 INFO Executor: Adding file:/tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/com.google.code.findbugs_jsr305-3.0.0.jar to class loader default
26/07/03 18:42:06 INFO Executor: Fetching spark://192.168.1.31:36241/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084324446
26/07/03 18:42:06 INFO Utils: Fetching spark://192.168.1.31:36241/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp8037880650910272244.tmp
26/07/03 18:42:06 INFO Utils: /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/fetchFileTemp8037880650910272244.tmp has been previously copied to /tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar
26/07/03 18:42:06 INFO Executor: Adding file:/tmp/spark-4a574fe7-ab50-40e5-99cd-28997f435b70/userFiles-55734433-d9e8-4cd4-b6ab-27472b70f824/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar to class loader default
26/07/03 18:42:06 INFO Utils: Successfully started service 'org.apache.spark.network.netty.NettyBlockTransferService' on port 41103.
26/07/03 18:42:06 INFO NettyBlockTransferService: Server created on 192.168.1.31:41103
26/07/03 18:42:06 INFO BlockManager: Using org.apache.spark.storage.RandomBlockReplicationPolicy for block replication policy
26/07/03 18:42:06 INFO BlockManagerMaster: Registering BlockManager BlockManagerId(driver, 192.168.1.31, 41103, None)
26/07/03 18:42:06 INFO BlockManagerMasterEndpoint: Registering block manager 192.168.1.31:41103 with 434.4 MiB RAM, BlockManagerId(driver, 192.168.1.31, 41103, None)
26/07/03 18:42:06 INFO BlockManagerMaster: Registered BlockManager BlockManagerId(driver, 192.168.1.31, 41103, None)
26/07/03 18:42:06 INFO BlockManager: Initialized BlockManager: BlockManagerId(driver, 192.168.1.31, 41103, None)
INFO:__main__:Reading from Kafka topic: sensor_DA25M622
26/07/03 18:42:08 INFO SharedState: Setting hive.metastore.warehouse.dir ('null') to the value of spark.sql.warehouse.dir.
26/07/03 18:42:08 INFO SharedState: Warehouse path is 'file:/home/sohang/Projects/iit-madras-web-mtech-ai/trimester3/DA5402W_MLOPS/assignments/Assignment1/spark-warehouse'.
INFO:__main__:Starting data preprocessing...
INFO:__main__:================================================================================
INFO:__main__:SCHEMA:
root
 |-- sensor_id: string (nullable = true)
 |-- temperature: double (nullable = true)
 |-- timestamp: string (nullable = true)
 |-- status: string (nullable = true)

INFO:__main__:================================================================================
INFO:__main__:Data preprocessing completed.
INFO:__main__:Starting streaming queries...
26/07/03 18:42:11 INFO StateStoreCoordinatorRef: Registered StateStoreCoordinator endpoint
26/07/03 18:42:11 WARN ResolveWriteToStream: Temporary checkpoint location created which is deleted normally when the query didn't fail: /tmp/temporary-514ba7e2-cefe-4139-805f-5075778969c6. If it's required to delete it under any circumstances, please set spark.sql.streaming.forceDeleteTempCheckpointLocation to true. Important to know deleting temp checkpoint folder is best effort.
26/07/03 18:42:11 INFO ResolveWriteToStream: Checkpoint root file:///tmp/temporary-514ba7e2-cefe-4139-805f-5075778969c6 resolved to file:/tmp/temporary-514ba7e2-cefe-4139-805f-5075778969c6.
26/07/03 18:42:11 WARN ResolveWriteToStream: spark.sql.adaptive.enabled is not supported in streaming DataFrames/Datasets and will be disabled.
ERROR:__main__:Error in main: [NON_TIME_WINDOW_NOT_SUPPORTED_IN_STREAMING] Window function is not supported in ROW_NUMBER() (as column `row_num`) on streaming DataFrames/Datasets.
Structured Streaming only supports time-window aggregation using the WINDOW function. (window specification: (PARTITION BY SENSOR_ID, TIMESTAMP ORDER BY TIMESTAMP ASC NULLS FIRST ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)) SQLSTATE: 42KDE
Traceback (most recent call last):
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/trimester3/DA5402W_MLOPS/assignments/Assignment1/spark_streaming.py", line 266, in main
    .start()
     ~~~~~^^
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/.venv/lib/python3.14/site-packages/pyspark/python/lib/pyspark.zip/pyspark/sql/streaming/readwriter.py", line 1704, in start
    return self._sq(self._jwrite.start())
                    ~~~~~~~~~~~~~~~~~~^^
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/.venv/lib/python3.14/site-packages/pyspark/python/lib/py4j-0.10.9.9-src.zip/py4j/java_gateway.py", line 1362, in __call__
    return_value = get_return_value(
        answer, self.gateway_client, self.target_id, self.name)
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/.venv/lib/python3.14/site-packages/pyspark/python/lib/pyspark.zip/pyspark/errors/exceptions/captured.py", line 269, in deco
    raise converted from None
pyspark.errors.exceptions.captured.AnalysisException: [NON_TIME_WINDOW_NOT_SUPPORTED_IN_STREAMING] Window function is not supported in ROW_NUMBER() (as column `row_num`) on streaming DataFrames/Datasets.
Structured Streaming only supports time-window aggregation using the WINDOW function. (window specification: (PARTITION BY SENSOR_ID, TIMESTAMP ORDER BY TIMESTAMP ASC NULLS FIRST ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)) SQLSTATE: 42KDE
26/07/03 18:42:11 INFO SparkContext: SparkContext is stopping with exitCode 0 from stop at NativeMethodAccessorImpl.java:0.
26/07/03 18:42:12 INFO SparkUI: Stopped Spark web UI at http://192.168.1.31:4040
26/07/03 18:42:12 INFO MapOutputTrackerMasterEndpoint: MapOutputTrackerMasterEndpoint stopped!
26/07/03 18:42:12 INFO MemoryStore: MemoryStore started with capacity 434.4 MiB
26/07/03 18:42:12 INFO MemoryStore: MemoryStore cleared
26/07/03 18:42:12 INFO BlockManager: BlockManager stopped
26/07/03 18:42:12 INFO BlockManagerMaster: BlockManagerMaster stopped
26/07/03 18:42:12 INFO OutputCommitCoordinator$OutputCommitCoordinatorEndpoint: OutputCommitCoordinator stopped!
26/07/03 18:42:12 INFO SparkContext: Successfully stopped SparkContext (Uptime: 7611 ms)
INFO:__main__:Spark session stopped.
INFO:py4j.clientserver:Closing down clientserver connection
```
