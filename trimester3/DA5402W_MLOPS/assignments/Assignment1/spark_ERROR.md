$ spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.2 spark_streaming.py
WARNING: Using incubator modules: jdk.incubator.vector
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
26/07/03 18:51:29 WARN Utils: Your hostname, sohang-VivoBook-ASUS-Laptop-X510UFO, resolves to a loopback address: 127.0.1.1; using 192.168.1.31 instead (on interface wlp2s0)
26/07/03 18:51:29 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
:: loading settings :: url = jar:file:/home/sohang/Projects/iit-madras-web-mtech-ai/.venv/lib/python3.14/site-packages/pyspark/jars/ivy-2.5.3.jar!/org/apache/ivy/core/settings/ivysettings.xml
Ivy Default Cache set to: /home/sohang/.ivy2.5.2/cache
The jars for the packages stored in: /home/sohang/.ivy2.5.2/jars
org.apache.spark#spark-sql-kafka-0-10_2.13 added as a dependency
:: resolving dependencies :: org.apache.spark#spark-submit-parent-9989ef17-2414-4a6e-a85e-3a3ea55ab362;1.0
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
:: resolution report :: resolve 523ms :: artifacts dl 19ms
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
	|      default     |   11  |   0   |   0   |   0   ||   11  |   0   |
	---------------------------------------------------------------------
:: retrieving :: org.apache.spark#spark-submit-parent-9989ef17-2414-4a6e-a85e-3a3ea55ab362
	confs: [default]
	0 artifacts copied, 11 already retrieved (0kB/11ms)
26/07/03 18:51:30 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
26/07/03 18:51:32 INFO SparkContext: Running Spark version 4.1.2
26/07/03 18:51:32 INFO SparkContext: OS info Linux, 7.0.0-27-generic, amd64
26/07/03 18:51:32 INFO SparkContext: Java version 17.0.19+10-1-26.04.2-Ubuntu
26/07/03 18:51:32 INFO ResourceUtils: ==============================================================
26/07/03 18:51:32 INFO ResourceUtils: No custom resources configured for spark.driver.
26/07/03 18:51:32 INFO ResourceUtils: ==============================================================
26/07/03 18:51:32 INFO SparkContext: Submitted application: SensorStreamingPipeline
26/07/03 18:51:32 INFO SecurityManager: Changing view acls to: sohang
26/07/03 18:51:32 INFO SecurityManager: Changing modify acls to: sohang
26/07/03 18:51:32 INFO SecurityManager: Changing view acls groups to: sohang
26/07/03 18:51:32 INFO SecurityManager: Changing modify acls groups to: sohang
26/07/03 18:51:32 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: sohang groups with view permissions: EMPTY; users with modify permissions: sohang; groups with modify permissions: EMPTY; RPC SSL disabled
26/07/03 18:51:32 INFO Utils: Successfully started service 'sparkDriver' on port 35689.
26/07/03 18:51:32 INFO SparkEnv: Registering MapOutputTracker
26/07/03 18:51:32 INFO SparkEnv: Registering BlockManagerMaster
26/07/03 18:51:32 INFO BlockManagerMasterEndpoint: Using org.apache.spark.storage.DefaultTopologyMapper for getting topology information
26/07/03 18:51:32 INFO BlockManagerMasterEndpoint: BlockManagerMasterEndpoint up
26/07/03 18:51:32 INFO SparkEnv: Registering BlockManagerMasterHeartbeat
26/07/03 18:51:32 INFO DiskBlockManager: Created local directory at /tmp/blockmgr-fffc8d19-e639-4889-a254-8a8596ee7de4
26/07/03 18:51:32 INFO SparkEnv: Registering OutputCommitCoordinator
26/07/03 18:51:32 INFO JettyUtils: Start Jetty 0.0.0.0:4040 for SparkUI
26/07/03 18:51:33 INFO Utils: Successfully started service 'SparkUI' on port 4040.
26/07/03 18:51:33 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar at spark://192.168.1.31:35689/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar at spark://192.168.1.31:35689/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar at spark://192.168.1.31:35689/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.9.1.jar at spark://192.168.1.31:35689/jars/org.apache.kafka_kafka-clients-3.9.1.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar at spark://192.168.1.31:35689/jars/com.google.code.findbugs_jsr305-3.0.0.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.12.1.jar at spark://192.168.1.31:35689/jars/org.apache.commons_commons-pool2-2.12.1.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar at spark://192.168.1.31:35689/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar at spark://192.168.1.31:35689/jars/org.lz4_lz4-java-1.8.0.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar at spark://192.168.1.31:35689/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.17.jar at spark://192.168.1.31:35689/jars/org.slf4j_slf4j-api-2.0.17.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO SparkContext: Added JAR file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar at spark://192.168.1.31:35689/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar
26/07/03 18:51:33 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar
26/07/03 18:51:33 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar at file:///home/sohang/.ivy2.5.2/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar
26/07/03 18:51:33 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.9.1.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.9.1.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.9.1.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.kafka_kafka-clients-3.9.1.jar
26/07/03 18:51:33 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar at file:///home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/com.google.code.findbugs_jsr305-3.0.0.jar
26/07/03 18:51:33 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.12.1.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.12.1.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.12.1.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.commons_commons-pool2-2.12.1.jar
26/07/03 18:51:33 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar
26/07/03 18:51:33 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar at file:///home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.lz4_lz4-java-1.8.0.jar
26/07/03 18:51:33 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar at file:///home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.xerial.snappy_snappy-java-1.1.10.8.jar
26/07/03 18:51:33 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.17.jar at file:///home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.17.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.17.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.slf4j_slf4j-api-2.0.17.jar
26/07/03 18:51:33 INFO SparkContext: Added file file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar at file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Copying /home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.hadoop_hadoop-client-api-3.4.2.jar
26/07/03 18:51:33 INFO ResourceProfile: Default ResourceProfile created, executor resources: Map(cores -> name: cores, amount: 1, script: , vendor: , memory -> name: memory, amount: 1024, script: , vendor: , offHeap -> name: offHeap, amount: 0, script: , vendor: ), task resources: Map(cpus -> name: cpus, amount: 1.0)
26/07/03 18:51:33 INFO ResourceProfile: Limiting resource is cpu
26/07/03 18:51:33 INFO ResourceProfileManager: Added ResourceProfile id: 0
26/07/03 18:51:33 INFO SecurityManager: Changing view acls to: sohang
26/07/03 18:51:33 INFO SecurityManager: Changing modify acls to: sohang
26/07/03 18:51:33 INFO SecurityManager: Changing view acls groups to: sohang
26/07/03 18:51:33 INFO SecurityManager: Changing modify acls groups to: sohang
26/07/03 18:51:33 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: sohang groups with view permissions: EMPTY; users with modify permissions: sohang; groups with modify permissions: EMPTY; RPC SSL disabled
26/07/03 18:51:33 INFO Executor: Starting executor ID driver on host 192.168.1.31
26/07/03 18:51:33 INFO Executor: OS info Linux, 7.0.0-27-generic, amd64
26/07/03 18:51:33 INFO Executor: Java version 17.0.19+10-1-26.04.2-Ubuntu
26/07/03 18:51:33 INFO Executor: Starting executor with user classpath (userClassPathFirst = false): ''
26/07/03 18:51:33 INFO Executor: Created or updated repl class loader org.apache.spark.util.MutableURLClassLoader@5dc88b55 for default.
26/07/03 18:51:33 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar
26/07/03 18:51:33 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.17.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.slf4j_slf4j-api-2.0.17.jar has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.slf4j_slf4j-api-2.0.17.jar
26/07/03 18:51:33 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar
26/07/03 18:51:33 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.12.1.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.commons_commons-pool2-2.12.1.jar has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.commons_commons-pool2-2.12.1.jar
26/07/03 18:51:33 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar
26/07/03 18:51:33 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.lz4_lz4-java-1.8.0.jar has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.lz4_lz4-java-1.8.0.jar
26/07/03 18:51:33 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.xerial.snappy_snappy-java-1.1.10.8.jar
26/07/03 18:51:33 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: /home/sohang/.ivy2.5.2/jars/com.google.code.findbugs_jsr305-3.0.0.jar has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/com.google.code.findbugs_jsr305-3.0.0.jar
26/07/03 18:51:33 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar
26/07/03 18:51:33 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.9.1.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.kafka_kafka-clients-3.9.1.jar has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.kafka_kafka-clients-3.9.1.jar
26/07/03 18:51:33 INFO Executor: Fetching file:///home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: /home/sohang/.ivy2.5.2/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.hadoop_hadoop-client-api-3.4.2.jar
26/07/03 18:51:33 INFO Executor: Fetching spark://192.168.1.31:35689/jars/org.slf4j_slf4j-api-2.0.17.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO TransportClientFactory: Successfully created connection to /192.168.1.31:35689 after 35 ms (0 ms spent in bootstraps)
26/07/03 18:51:33 INFO Utils: Fetching spark://192.168.1.31:35689/jars/org.slf4j_slf4j-api-2.0.17.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp9680399025653342411.tmp
26/07/03 18:51:33 INFO Utils: /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp9680399025653342411.tmp has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.slf4j_slf4j-api-2.0.17.jar
26/07/03 18:51:33 INFO Executor: Adding file:/tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.slf4j_slf4j-api-2.0.17.jar to class loader default
26/07/03 18:51:33 INFO Executor: Fetching spark://192.168.1.31:35689/jars/org.apache.kafka_kafka-clients-3.9.1.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Fetching spark://192.168.1.31:35689/jars/org.apache.kafka_kafka-clients-3.9.1.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp12613255289248433982.tmp
26/07/03 18:51:33 INFO Utils: /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp12613255289248433982.tmp has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.kafka_kafka-clients-3.9.1.jar
26/07/03 18:51:33 INFO Executor: Adding file:/tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.kafka_kafka-clients-3.9.1.jar to class loader default
26/07/03 18:51:33 INFO Executor: Fetching spark://192.168.1.31:35689/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Fetching spark://192.168.1.31:35689/jars/org.xerial.snappy_snappy-java-1.1.10.8.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp12123597983069818772.tmp
26/07/03 18:51:33 INFO Utils: /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp12123597983069818772.tmp has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.xerial.snappy_snappy-java-1.1.10.8.jar
26/07/03 18:51:33 INFO Executor: Adding file:/tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.xerial.snappy_snappy-java-1.1.10.8.jar to class loader default
26/07/03 18:51:33 INFO Executor: Fetching spark://192.168.1.31:35689/jars/com.google.code.findbugs_jsr305-3.0.0.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Fetching spark://192.168.1.31:35689/jars/com.google.code.findbugs_jsr305-3.0.0.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp59855774580179367.tmp
26/07/03 18:51:33 INFO Utils: /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp59855774580179367.tmp has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/com.google.code.findbugs_jsr305-3.0.0.jar
26/07/03 18:51:33 INFO Executor: Adding file:/tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/com.google.code.findbugs_jsr305-3.0.0.jar to class loader default
26/07/03 18:51:33 INFO Executor: Fetching spark://192.168.1.31:35689/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Fetching spark://192.168.1.31:35689/jars/org.apache.hadoop_hadoop-client-api-3.4.2.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp16382640203205553091.tmp
26/07/03 18:51:33 INFO Utils: /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp16382640203205553091.tmp has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.hadoop_hadoop-client-api-3.4.2.jar
26/07/03 18:51:33 INFO Executor: Adding file:/tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.hadoop_hadoop-client-api-3.4.2.jar to class loader default
26/07/03 18:51:33 INFO Executor: Fetching spark://192.168.1.31:35689/jars/org.apache.commons_commons-pool2-2.12.1.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Fetching spark://192.168.1.31:35689/jars/org.apache.commons_commons-pool2-2.12.1.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp13769762647541511404.tmp
26/07/03 18:51:33 INFO Utils: /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp13769762647541511404.tmp has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.commons_commons-pool2-2.12.1.jar
26/07/03 18:51:33 INFO Executor: Adding file:/tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.commons_commons-pool2-2.12.1.jar to class loader default
26/07/03 18:51:33 INFO Executor: Fetching spark://192.168.1.31:35689/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Fetching spark://192.168.1.31:35689/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp5950296861064031343.tmp
26/07/03 18:51:33 INFO Utils: /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp5950296861064031343.tmp has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar
26/07/03 18:51:33 INFO Executor: Adding file:/tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.spark_spark-token-provider-kafka-0-10_2.13-4.1.2.jar to class loader default
26/07/03 18:51:33 INFO Executor: Fetching spark://192.168.1.31:35689/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Fetching spark://192.168.1.31:35689/jars/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp16113706564786499921.tmp
26/07/03 18:51:33 INFO Utils: /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp16113706564786499921.tmp has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar
26/07/03 18:51:33 INFO Executor: Adding file:/tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.hadoop_hadoop-client-runtime-3.4.2.jar to class loader default
26/07/03 18:51:33 INFO Executor: Fetching spark://192.168.1.31:35689/jars/org.lz4_lz4-java-1.8.0.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Fetching spark://192.168.1.31:35689/jars/org.lz4_lz4-java-1.8.0.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp601588892539623484.tmp
26/07/03 18:51:33 INFO Utils: /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp601588892539623484.tmp has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.lz4_lz4-java-1.8.0.jar
26/07/03 18:51:33 INFO Executor: Adding file:/tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.lz4_lz4-java-1.8.0.jar to class loader default
26/07/03 18:51:33 INFO Executor: Fetching spark://192.168.1.31:35689/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Fetching spark://192.168.1.31:35689/jars/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp13962878209627925689.tmp
26/07/03 18:51:33 INFO Utils: /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp13962878209627925689.tmp has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar
26/07/03 18:51:33 INFO Executor: Adding file:/tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.scala-lang.modules_scala-parallel-collections_2.13-1.2.0.jar to class loader default
26/07/03 18:51:33 INFO Executor: Fetching spark://192.168.1.31:35689/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar with timestamp 1783084892305
26/07/03 18:51:33 INFO Utils: Fetching spark://192.168.1.31:35689/jars/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp4206514835775980060.tmp
26/07/03 18:51:33 INFO Utils: /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/fetchFileTemp4206514835775980060.tmp has been previously copied to /tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar
26/07/03 18:51:33 INFO Executor: Adding file:/tmp/spark-ffb9ab31-eed2-4130-9b5f-087c44e996f5/userFiles-2d6ace78-bee0-4094-bfca-7473044c78a5/org.apache.spark_spark-sql-kafka-0-10_2.13-4.1.2.jar to class loader default
26/07/03 18:51:33 INFO Utils: Successfully started service 'org.apache.spark.network.netty.NettyBlockTransferService' on port 44041.
26/07/03 18:51:33 INFO NettyBlockTransferService: Server created on 192.168.1.31:44041
26/07/03 18:51:33 INFO BlockManager: Using org.apache.spark.storage.RandomBlockReplicationPolicy for block replication policy
26/07/03 18:51:33 INFO BlockManagerMaster: Registering BlockManager BlockManagerId(driver, 192.168.1.31, 44041, None)
26/07/03 18:51:33 INFO BlockManagerMasterEndpoint: Registering block manager 192.168.1.31:44041 with 434.4 MiB RAM, BlockManagerId(driver, 192.168.1.31, 44041, None)
26/07/03 18:51:34 INFO BlockManagerMaster: Registered BlockManager BlockManagerId(driver, 192.168.1.31, 44041, None)
26/07/03 18:51:34 INFO BlockManager: Initialized BlockManager: BlockManagerId(driver, 192.168.1.31, 44041, None)
INFO:__main__:Reading from Kafka topic: sensor_DA25M622
26/07/03 18:51:36 INFO SharedState: Setting hive.metastore.warehouse.dir ('null') to the value of spark.sql.warehouse.dir.
26/07/03 18:51:36 INFO SharedState: Warehouse path is 'file:/home/sohang/Projects/iit-madras-web-mtech-ai/trimester3/DA5402W_MLOPS/assignments/Assignment1/spark-warehouse'.
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
26/07/03 18:51:39 INFO StateStoreCoordinatorRef: Registered StateStoreCoordinator endpoint
26/07/03 18:51:39 WARN ResolveWriteToStream: Temporary checkpoint location created which is deleted normally when the query didn't fail: /tmp/temporary-9191374e-47d8-4903-a2fe-81db2ec0abe8. If it's required to delete it under any circumstances, please set spark.sql.streaming.forceDeleteTempCheckpointLocation to true. Important to know deleting temp checkpoint folder is best effort.
26/07/03 18:51:39 INFO ResolveWriteToStream: Checkpoint root file:///tmp/temporary-9191374e-47d8-4903-a2fe-81db2ec0abe8 resolved to file:/tmp/temporary-9191374e-47d8-4903-a2fe-81db2ec0abe8.
26/07/03 18:51:39 WARN ResolveWriteToStream: spark.sql.adaptive.enabled is not supported in streaming DataFrames/Datasets and will be disabled.
26/07/03 18:51:39 INFO CheckpointFileManager: Writing atomically to file:/tmp/temporary-9191374e-47d8-4903-a2fe-81db2ec0abe8/metadata using temp file file:/tmp/temporary-9191374e-47d8-4903-a2fe-81db2ec0abe8/.metadata.3dd1dabc-f61c-494e-b28e-66c1035e4e57.tmp
26/07/03 18:51:40 INFO CheckpointFileManager: Renamed temp file file:/tmp/temporary-9191374e-47d8-4903-a2fe-81db2ec0abe8/.metadata.3dd1dabc-f61c-494e-b28e-66c1035e4e57.tmp to file:/tmp/temporary-9191374e-47d8-4903-a2fe-81db2ec0abe8/metadata
26/07/03 18:51:40 INFO MicroBatchExecution: Starting [id = 0c2fa0d9-5f00-420f-8c6b-99797136bf26, runId = 99bc2a8b-5b58-4d83-8bb3-b2507b0c00d2]. Use file:/tmp/temporary-9191374e-47d8-4903-a2fe-81db2ec0abe8 to store the query checkpoint.
26/07/03 18:51:40 INFO MicroBatchExecution: Reading table [org.apache.spark.sql.kafka010.KafkaSourceProvider$KafkaTable@52443ff9] from DataSourceV2 named 'kafka' [org.apache.spark.sql.kafka010.KafkaSourceProvider@22d899d4]
26/07/03 18:51:40 WARN ResolveWriteToStream: Temporary checkpoint location created which is deleted normally when the query didn't fail: /tmp/temporary-19bbec0f-06a4-433c-bd8d-c9242a6d9cfe. If it's required to delete it under any circumstances, please set spark.sql.streaming.forceDeleteTempCheckpointLocation to true. Important to know deleting temp checkpoint folder is best effort.
26/07/03 18:51:40 INFO ResolveWriteToStream: Checkpoint root file:///tmp/temporary-19bbec0f-06a4-433c-bd8d-c9242a6d9cfe resolved to file:/tmp/temporary-19bbec0f-06a4-433c-bd8d-c9242a6d9cfe.
26/07/03 18:51:40 WARN ResolveWriteToStream: spark.sql.adaptive.enabled is not supported in streaming DataFrames/Datasets and will be disabled.
26/07/03 18:51:40 INFO MicroBatchExecution: Finish initializing with logical plan:
~WriteToMicroBatchDataSource org.apache.spark.sql.execution.streaming.ConsoleTable$@24e1d6bf, 0c2fa0d9-5f00-420f-8c6b-99797136bf26, [numRows=20, truncate=false], Append
+- ~Project [sensor_id#15, temperature#20, timestamp#19-T600000ms, status#18, hour_of_day#21, day_of_week#22, CASE WHEN ((day_of_week#22 = 1) OR (day_of_week#22 = 7)) THEN 1 ELSE 0 END AS is_weekend#23]
   +- ~Project [sensor_id#15, temperature#20, timestamp#19-T600000ms, status#18, hour_of_day#21, dayofweek(cast(timestamp#19-T600000ms as date)) AS day_of_week#22]
      +- ~Project [sensor_id#15, temperature#20, timestamp#19-T600000ms, status#18, hour(timestamp#19-T600000ms, Some(Asia/Kolkata)) AS hour_of_day#21]
         +- ~Filter isnotnull(temperature#20)
            +- ~Project [sensor_id#15, CASE WHEN isnull(temperature#16) THEN 25.0 ELSE temperature#16 END AS temperature#20, timestamp#19-T600000ms, status#18]
               +- ~Deduplicate [sensor_id#15, timestamp#19-T600000ms]
                  +- ~EventTimeWatermark e4e21be9-4e7e-457c-a1ef-a0a4e18bae63, timestamp#19: timestamp, 10 minutes
                     +- ~Filter (((temperature#16 >= cast(-20 as double)) AND (temperature#16 <= cast(100 as double))) AND NOT isnull(timestamp#19))
                        +- ~Project [sensor_id#15, temperature#16, to_timestamp(timestamp#17, Some(yyyy-MM-dd HH:mm:ss), TimestampType, Some(Asia/Kolkata), true) AS timestamp#19, status#18]
                           +- ~Project [data#14.sensor_id AS sensor_id#15, data#14.temperature AS temperature#16, data#14.timestamp AS timestamp#17, data#14.status AS status#18]
                              +- ~Project [from_json(StructField(sensor_id,StringType,false), StructField(temperature,DoubleType,true), StructField(timestamp,StringType,false), StructField(status,StringType,false), cast(value#8 as string), Some(Asia/Kolkata), false) AS data#14]
                                 +- ~StreamingDataSourceV2ScanRelation[key#7, value#8, topic#9, partition#10, offset#11L, timestamp#12, timestampType#13] KafkaTable

26/07/03 18:51:40 INFO OffsetSeqLog: BatchIds found from listing:
26/07/03 18:51:40 INFO CommitLog: BatchIds found from listing:
26/07/03 18:51:40 INFO OffsetSeqLog: BatchIds found from listing:
26/07/03 18:51:40 INFO OffsetSeqLog: BatchIds found from listing:
26/07/03 18:51:40 INFO MicroBatchExecution: Starting new streaming query.
26/07/03 18:51:40 WARN MicroBatchExecution: Disabling AQE since AQE is not supported in stateful workloads.
26/07/03 18:51:40 INFO MicroBatchExecution: Stream started from {}
ERROR:__main__:Error in main: [STREAMING_OUTPUT_MODE.UNSUPPORTED_OPERATION] Invalid streaming output mode: append. This output mode is not supported for streaming aggregations without watermark on streaming DataFrames/DataSets. SQLSTATE: 42KDE
Traceback (most recent call last):
  File "/home/sohang/Projects/iit-madras-web-mtech-ai/trimester3/DA5402W_MLOPS/assignments/Assignment1/spark_streaming.py", line 321, in main
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
pyspark.errors.exceptions.captured.AnalysisException: [STREAMING_OUTPUT_MODE.UNSUPPORTED_OPERATION] Invalid streaming output mode: append. This output mode is not supported for streaming aggregations without watermark on streaming DataFrames/DataSets. SQLSTATE: 42KDE
26/07/03 18:51:40 INFO SparkContext: SparkContext is stopping with exitCode 0 from stop at NativeMethodAccessorImpl.java:0.
26/07/03 18:51:40 ERROR MicroBatchExecution: Query [id = 0c2fa0d9-5f00-420f-8c6b-99797136bf26, runId = 99bc2a8b-5b58-4d83-8bb3-b2507b0c00d2] terminated with error
java.lang.AssertionError: assertion failed
	at scala.Predef$.assert(Predef.scala:264)
	at org.apache.spark.sql.kafka010.KafkaMicroBatchStream.getOrCreateInitialPartitionOffsets(KafkaMicroBatchStream.scala:372)
	at org.apache.spark.sql.kafka010.KafkaMicroBatchStream.initialOffset(KafkaMicroBatchStream.scala:111)
	at org.apache.spark.sql.execution.streaming.runtime.MicroBatchExecution.$anonfun$getStartOffset$2(MicroBatchExecution.scala:737)
	at scala.Option.getOrElse(Option.scala:201)
	at org.apache.spark.sql.execution.streaming.runtime.MicroBatchExecution.getStartOffset(MicroBatchExecution.scala:737)
	at org.apache.spark.sql.execution.streaming.runtime.MicroBatchExecution.$anonfun$constructNextBatch$4(MicroBatchExecution.scala:773)
	at org.apache.spark.sql.execution.streaming.runtime.ProgressContext.reportTimeTaken(ProgressReporter.scala:200)
	at org.apache.spark.sql.execution.streaming.runtime.MicroBatchExecution.$anonfun$constructNextBatch$2(MicroBatchExecution.scala:772)
	at scala.collection.immutable.List.map(List.scala:236)
	at scala.collection.immutable.List.map(List.scala:79)
	at org.apache.spark.sql.execution.streaming.runtime.MicroBatchExecution.$anonfun$constructNextBatch$1(MicroBatchExecution.scala:761)
	at scala.runtime.java8.JFunction0$mcZ$sp.apply(JFunction0$mcZ$sp.scala:17)
	at org.apache.spark.sql.execution.streaming.runtime.MicroBatchExecution.withProgressLocked(MicroBatchExecution.scala:1335)
	at org.apache.spark.sql.execution.streaming.runtime.MicroBatchExecution.constructNextBatch(MicroBatchExecution.scala:757)
	at org.apache.spark.sql.execution.streaming.runtime.MicroBatchExecution.$anonfun$executeOneBatch$2(MicroBatchExecution.scala:492)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at org.apache.spark.sql.execution.streaming.runtime.ProgressContext.reportTimeTaken(ProgressReporter.scala:200)
	at org.apache.spark.sql.execution.streaming.runtime.MicroBatchExecution.executeOneBatch(MicroBatchExecution.scala:481)
	at org.apache.spark.sql.execution.streaming.runtime.MicroBatchExecution.$anonfun$runActivatedStream$1(MicroBatchExecution.scala:461)
	at org.apache.spark.sql.execution.streaming.runtime.MicroBatchExecution.$anonfun$runActivatedStream$1$adapted(MicroBatchExecution.scala:461)
	at org.apache.spark.sql.execution.streaming.runtime.TriggerExecutor.runOneBatch(TriggerExecutor.scala:40)
	at org.apache.spark.sql.execution.streaming.runtime.TriggerExecutor.runOneBatch$(TriggerExecutor.scala:38)
	at org.apache.spark.sql.execution.streaming.runtime.ProcessingTimeExecutor.runOneBatch(TriggerExecutor.scala:71)
	at org.apache.spark.sql.execution.streaming.runtime.ProcessingTimeExecutor.execute(TriggerExecutor.scala:83)
	at org.apache.spark.sql.execution.streaming.runtime.MicroBatchExecution.runActivatedStream(MicroBatchExecution.scala:461)
	at org.apache.spark.sql.execution.streaming.runtime.StreamExecution.$anonfun$runStream$1(StreamExecution.scala:347)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:804)
	at org.apache.spark.sql.execution.streaming.runtime.StreamExecution.org$apache$spark$sql$execution$streaming$runtime$StreamExecution$$runStream(StreamExecution.scala:307)
	at org.apache.spark.sql.execution.streaming.runtime.StreamExecution$$anon$1.run(StreamExecution.scala:230)
26/07/03 18:51:40 INFO MicroBatchExecution: Async log purge executor pool for query [id = 0c2fa0d9-5f00-420f-8c6b-99797136bf26, runId = 99bc2a8b-5b58-4d83-8bb3-b2507b0c00d2] has been shutdown
26/07/03 18:51:40 INFO MicroBatchExecution: Deleting checkpoint file:/tmp/temporary-9191374e-47d8-4903-a2fe-81db2ec0abe8.
26/07/03 18:51:40 INFO SparkUI: Stopped Spark web UI at http://192.168.1.31:4040
26/07/03 18:51:40 INFO MapOutputTrackerMasterEndpoint: MapOutputTrackerMasterEndpoint stopped!
26/07/03 18:51:40 INFO MemoryStore: MemoryStore started with capacity 434.4 MiB
26/07/03 18:51:40 INFO MemoryStore: MemoryStore cleared
26/07/03 18:51:40 INFO BlockManager: BlockManager stopped
26/07/03 18:51:40 INFO BlockManagerMaster: BlockManagerMaster stopped
26/07/03 18:51:40 INFO OutputCommitCoordinator$OutputCommitCoordinatorEndpoint: OutputCommitCoordinator stopped!
26/07/03 18:51:40 INFO SparkContext: Successfully stopped SparkContext (Uptime: 7984 ms)
INFO:__main__:Spark session stopped.
INFO:py4j.clientserver:Closing down clientserver connection
