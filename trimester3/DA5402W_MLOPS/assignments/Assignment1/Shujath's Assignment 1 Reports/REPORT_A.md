# Part A Report - Kafka-Based Data Ingestion

**Roll number:** `DA25M590`  
**Topic:** `sensor_da25m590`  
**Execution environment:** MLDL  
**Bootstrap server:** `localhost:9092` (replace if different)

## Configuration

The experiment uses one Kafka broker in KRaft mode. The topic has three partitions and a
replication factor of one, as required. Records are JSON encoded and keyed by `sensor_id`.
Acknowledgment mode is `all`, automatic topic creation is disabled in the included local setup,
and consumers use unique group IDs with automatic commits disabled.

Configuration was verified with:

```bash
kafka-topics.sh --bootstrap-server "$BOOTSTRAP_SERVERS" \
  --describe --topic sensor_da25m590
```

The broker reported `PartitionCount: 3` and `ReplicationFactor: 1`. Partitions 0, 1, and 2
were led by broker 1, and each partition had its replica present in the in-sync replica set.

## Results

The experiment ran at `2026-06-22T19:53:06Z`. Metrics were read from
`reports/part_a_metrics.json`.

| Metric | Measured value |
|---|---:|
| Total records produced | 2,000 |
| Producer throughput (records/sec) | 48.05 |
| 1-consumer: total consumed | 2,000 |
| 1-consumer throughput (records/sec) | 602.09 |
| 2-consumer: total consumed | 2,000 |
| 2-consumer throughput (records/sec) | 293.15 |
| 4-consumer: total consumed | 2,000 |
| 4-consumer throughput (records/sec) | 296.21 |
| Analytics group: total consumed | 2,000 |
| Monitoring group: total consumed | 2,000 |

### Partition Distribution

| Scenario | Partition 0 | Partition 1 | Partition 2 | Total |
|---|---:|---:|---:|---:|
| 1 consumer | 404 | 1,016 | 580 | 2,000 |
| 2 consumers | 404 | 1,016 | 580 | 2,000 |
| 4 consumers | 404 | 1,016 | 580 | 2,000 |

In the four-consumer experiment, consumer 3 had an empty assignment and processed zero records.
The other three consumers were assigned one partition each. The two-consumer run assigned
partitions 0 and 1 to one consumer and partition 2 to the other.

The one-consumer throughput was higher for this finite replay. The multi-consumer measurements
include consumer-group joining and rebalance overhead, which is significant relative to the short
processing time. The result demonstrates available parallelism and assignment behavior; it does
not imply that adding consumers must improve throughput for every small workload.

## Independent Consumer Groups

The `analytics-*` and `monitoring-*` groups ran concurrently. Both started with new group IDs and
independent offset state. Each consumed 2,000 records, equal to the 2,000 records produced. This
shows that records are load-balanced within a group but broadcast logically across different
groups.

Kafka's consumer-group description reported committed offsets of 404, 1,016, and 580 for
partitions 0, 1, and 2. These matched the corresponding log-end offsets, giving zero lag on every
partition after processing.

## Discussion

### Role of Partitions

Partitions divide a topic into ordered logs. They distribute storage and processing across Kafka
brokers and allow records to be consumed in parallel. Ordering is guaranteed within one partition,
not across the entire topic. Using `sensor_id` as the key keeps all records for a sensor ordered in
the same partition.

### Partitions and Consumer Parallelism

Within a consumer group, each partition is assigned to at most one consumer at a time. With three
partitions, one consumer reads all three, two consumers divide the three partitions, and three
consumers can each read one partition. Actual throughput also depends on record distribution,
broker capacity, network overhead, and rebalance time, so more active consumers do not guarantee
perfectly linear speedup.

### More Consumers Than Partitions

When four consumers join a group reading a three-partition topic, Kafka can assign work to only
three of them. The fourth remains idle until a partition becomes available, for example after
another consumer leaves. It adds group-management overhead without increasing steady-state
parallelism. Increasing useful parallelism therefore requires increasing the partition count,
subject to the ordering and operational trade-offs of doing so.
