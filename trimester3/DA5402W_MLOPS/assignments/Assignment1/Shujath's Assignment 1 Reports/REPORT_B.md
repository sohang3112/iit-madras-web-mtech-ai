# Part B Report: Spark Structured Streaming

## Configuration

| Item | Value |
|---|---|
| Kafka topic | `sensor_da25m590` |
| Partitions | 3 |
| Replication factor | 1 |
| Records produced | 3000 |
| Spark application | `DA5402W-Part-B-Spark-Structured-Streaming` |
| Watermark threshold | 5 minutes |
| Tumbling window | 5 minutes |
| Spark UI | `http://localhost:4040` |
| Kafka UI | `http://localhost:8080` |

## Schema

```text
sensor_id: string
timestamp: string
temperature: double
humidity: double
status: string
event_timestamp: timestamp
```

## Summary Table

| Metric | Value |
|---|---:|
| Raw Records | 3000 |
| Clean Records | 656 |
| Missing Values Corrected | 23 |
| Missing Values Dropped | 0 |
| Duplicate Records Removed | 2239 |
| Invalid Records Removed | 21 |
| Late Records Accepted | 658 |
| Records Discarded by Watermarking | 84 |
| Active Sensors in Last 5 Minutes | 10 |

## Analytics Results

### Average Temperature Per Sensor

| Sensor | Average Temperature |
|---|---:|
| sensor_1 | 24.03 |
| sensor_10 | 25.24 |
| sensor_2 | 24.94 |
| sensor_3 | 24.75 |
| sensor_4 | 25.99 |
| sensor_5 | 25.63 |
| sensor_6 | 26.46 |
| sensor_7 | 24.95 |
| sensor_8 | 24.33 |
| sensor_9 | 24.81 |

### Maximum Temperature Per Sensor

| Sensor | Maximum Temperature |
|---|---:|
| sensor_1 | 34.87 |
| sensor_10 | 34.99 |
| sensor_2 | 34.14 |
| sensor_3 | 34.85 |
| sensor_4 | 34.62 |
| sensor_5 | 34.97 |
| sensor_6 | 34.95 |
| sensor_7 | 34.33 |
| sensor_8 | 34.79 |
| sensor_9 | 34.94 |

### Status Distribution

| Status | Count |
|---|---:|
| active | 463 |
| error | 60 |
| idle | 95 |
| maintenance | 38 |

### Five-Minute Tumbling Window

| Window Start | Window End | Average Temperature |
|---|---|---:|
| 2026-06-23 21:35:00 | 2026-06-23 21:40:00 | 25.12 |

## Event-Time Processing

Timestamp strings were converted to Spark timestamp values using tolerant parsing, so invalid timestamp strings were converted to null and removed as invalid records. A 5-minute event-time threshold was used to distinguish accepted late events from records discarded by watermarking.

Results:

| Event-Time Metric | Value |
|---|---:|
| Late Records Accepted | 658 |
| Records Discarded by Watermarking | 84 |
| 5-Minute Window Average Temperature | 25.12 |

## Performance Metrics

| Metric | Value |
|---|---:|
| Input rate (rows/sec) | 109.85 |
| Processing rate (rows/sec) | 24.02 |
| Batch duration (seconds) | 27.31 |
| State store size | 656 |

## Execution Evidence

Generated artefacts:

| Artefact | Purpose |
|---|---|
| `reports/summary_table.json` | Data-quality and performance metrics |
| `reports/analytics_results.json` | Analytics outputs |
| `reports/spark_query_progress.json` | Spark run metadata |
| `reports/raw_kafka_records.jsonl` | Kafka input records consumed for this run |
| `reports/clean_records_csv/part-00000.csv` | Cleaned output records |

Dashboard evidence:

| Dashboard | Observation |
|---|---|
| Kafbat UI | Topic `sensor_da25m590` contains the produced Kafka messages |
| Spark UI | Jobs, stages, and SQL/DataFrame operations were visible at `http://localhost:4040` during execution |

## Discussion

Spark Structured Streaming treats the incoming Kafka sensor stream as an unbounded table. The implementation parses each record into a defined schema, converts the timestamp string to event time, removes invalid records, handles missing temperatures using recent same-sensor history, removes duplicates based on `sensor_id + timestamp`, and derives time-based features.

Event-time processing is needed because sensor events may arrive out of order. Watermarking provides a bounded lateness policy. records within the 5-minute threshold are still accepted, while records older than that threshold are counted as discarded by watermarking. The active sensor metric uses the same event-time idea by counting sensors that transmitted at least one valid record within the latest 5-minute event-time window.
