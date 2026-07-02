NOTE: There's a seperate community-built Kafka UI (https://github.com/provectus/kafka-ui) - it's available in Samsai portal, I haven't tried to install it locally.

Pre-Requisites:

```
$ java --version
openjdk 17.0.19 2026-04-21
```

[Download & start Kafka server](https://kafka.apache.org/quickstart/) (latest Kafka version: 4.3.0) (requires Java 17+):

```bash
# Download
$ wget https://dlcdn.apache.org/kafka/4.3.0/kafka_2.13-4.3.0.tgz
$ tar -xzf kafka_2.13-4.3.0.tgz
$ cd kafka_2.13-4.3.0/

# Setup Kafka environment (one-time)
$ KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"       # Generate random cluster UUID
$ bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties     # format log directories

# Start Kafka server
$ bin/kafka-server-start.sh config/server.properties
```

### Assignment instructions

NOTE: in a seperate terminal window from the running Kafka server.

Create topic `sensor_<rollno>`, so *sensor_DA25M622* :

```bin/kafka-topics.sh --create --topic sensor_DA25M622 --bootstrap-server localhost:9092```

Check partition count of topic (initially 0):

```bash
$ bin/kafka-topics.sh --describe --topic sensor_DA25M622 --bootstrap-server localhost:9092
Topic: sensor_DA25M622	TopicId: FCorgXzjRgSmR8l_Bo687Q	PartitionCount: 1	ReplicationFactor: 1	Configs: min.insync.replicas=1,segment.bytes=1073741824
	Topic: sensor_DA25M622	Partition: 0	Leader: 1	Replicas: 1	Isr: 1	Elr: 	LastKnownElr: 
```

Set partition count to 3 (replication factor is already 1 so don't need to change that):

```bin/kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic sensor_DA25M622 --partitions 3```

Run the provided Kafka producer.py assignment script (`kafka-python` seems broken / not working, so use `kafka-python-ng` instead -- though unfortunately kafka-python-ng's github repo is archived) - using Python 3.13:

```bash
$ pip install kafka-python-ng==2.2.3 
$ python producer.py --topic sensor_DA25M622
Published 500/2000 records...
Published 1000/2000 records...
Published 1500/2000 records...
Published 2000/2000 records...
Done. Published 2000 records to 'sensor_DA25M622' in 41.48s => throughput = 48.21 records/sec
{'topic': 'sensor_DA25M622', 'records_published': 2000, 'elapsed_seconds': 41.48089265823364, 'producer_throughput_rps': 48.214970118368825, 'timestamp': '2026-06-19T17:50:36.031844+00:00'}
```

Verify records were published in Kafka:

```bash
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic sensor_DA25M622 --from-beginning
{"sensor_id": "sensor_9", "timestamp": "2026-06-19 17:49:54", "temperature": 26.01, "humidity": 37.95, "status": "active"}
{"sensor_id": "sensor_1", "timestamp": "2026-06-19 17:49:54", "temperature": 21.09, "humidity": 69.88, "status": "active"}
...
{"sensor_id": "sensor_4", "timestamp": "2026-06-19 17:50:35", "temperature": 19.52, "humidity": 34.25, "status": "active"}
^CProcessed a total of 2000 messages
```

Consume records (see Jupyter Notebook)

Apparently I managed to publish twice (so total 4000!), so deleting and re-creating topic and publishing again:

```bash
$ bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic sensor_DA25M622     
$ bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic sensor_DA25M622 --partitions 3 --replication-factor 1
$ python producer.py --topic sensor_DA25M622
Published 500/2000 records...
Published 1000/2000 records...
Published 1500/2000 records...
Published 2000/2000 records...
Done. Published 2000 records to 'sensor_DA25M622' in 41.43s => throughput = 48.27 records/sec
```

consumer script:

```bash
$ python consumer.py
Number of records consumed: 0
Records received per partition: {}
Consumer throughput: 0.00 records/sec (elapsed 3.52s)
kafka-metrics-count: 66.0
Total number of metric entries returned by consumer.metrics(): 7

=== Group 'demo-group-size' with 1 consumer(s) ===
Consumer 0: 2715 records, partitions={0: 1377, 2: 1338}, throughput=631.54 rec/sec
Total consumed by group 'demo-group-size': 2715

=== Group 'demo-group-size' with 2 consumer(s) ===
Consumer 0: 0 records, partitions={}, throughput=0.00 rec/sec
Consumer 1: 0 records, partitions={}, throughput=0.00 rec/sec
Total consumed by group 'demo-group-size': 0

=== Group 'demo-group-size' with 4 consumer(s) ===
Consumer 0: 0 records, partitions={}, throughput=0.00 rec/sec
Consumer 1: 0 records, partitions={}, throughput=0.00 rec/sec
Consumer 2: 0 records, partitions={}, throughput=0.00 rec/sec
Consumer 3: 0 records, partitions={}, throughput=0.00 rec/sec
Total consumed by group 'demo-group-size': 0

Group demo-group-A consumed 0 records independently.
Partition counts: {}
Throughput: 0.00 records/sec

Group demo-group-B consumed 0 records independently.
Partition counts: {}
Throughput: 0.00 records/sec
```
