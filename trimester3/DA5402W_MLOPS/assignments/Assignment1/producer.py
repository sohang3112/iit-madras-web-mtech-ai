"""
Kafka Producer - DA5402W Assignment 1

Generates synthetic sensor readings (temperature, humidity, status) and
publishes them to a Kafka topic. Intentionally injects:
  - missing temperature values            
  - duplicate records (sensor_id+timestamp) 
  - out-of-range temperatures              
  - invalid/garbled timestamps             
  - late-arriving records                  

Run:
    python producer.py --topic sensor_roll_no --records 5000 --rate 50
"""

import argparse
import json
import random
import time
from datetime import datetime, timedelta, timezone

from kafka import KafkaProducer

NUM_SENSORS = 10
STATUSES = ["active", "idle", "error", "maintenance"]


def build_record(sensor_id: int, ts: datetime, last_record: dict | None):
    """Build one sensor reading, occasionally injecting an anomaly."""
    record = {
        "sensor_id": f"sensor_{sensor_id}",
        "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": round(random.uniform(15.0, 35.0), 2),
        "humidity": round(random.uniform(30.0, 90.0), 2),
        "status": random.choices(STATUSES, weights=[0.7, 0.15, 0.1, 0.05])[0],
    }

    roll = random.random()
    if roll < 0.03:
        record["temperature"] = None                       # missing value
    elif roll < 0.05:
        record["temperature"] = random.choice([-50.0, 150.0, -25.5, 120.0])  # invalid range
    elif roll < 0.07:
        record["timestamp"] = "NOT_A_TIMESTAMP"             # invalid timestamp
    elif roll < 0.10:
        late_ts = ts - timedelta(minutes=random.randint(6, 15))
        record["timestamp"] = late_ts.strftime("%Y-%m-%d %H:%M:%S")  # late record
    elif roll < 0.12 and last_record is not None:
        return dict(last_record)                            # exact duplicate

    return record


def main():
    parser = argparse.ArgumentParser(description="Kafka sensor data producer")
    parser.add_argument("--topic", required=True, help="Kafka topic, e.g. sensor_21f1234567")
    parser.add_argument("--bootstrap-servers", default="localhost:9092")
    parser.add_argument("--records", type=int, default=2000, help="Total records to publish")
    parser.add_argument("--rate", type=float, default=50.0, help="Target records/sec")
    parser.add_argument("--metrics-out", default="reports/producer_metrics.json")
    args = parser.parse_args()

    producer = KafkaProducer(
        bootstrap_servers=args.bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if k else None,
        api_version=(3, 5, 0),
    )

    sleep_interval = 1.0 / args.rate if args.rate > 0 else 0
    start_time = time.time()
    last_record = None

    for i in range(args.records):
        ts = datetime.now(timezone.utc)
        sensor_id = random.randint(1, NUM_SENSORS)
        record = build_record(sensor_id, ts, last_record)

        producer.send(args.topic, key=record["sensor_id"], value=record)
        last_record = record

        if sleep_interval:
            time.sleep(sleep_interval)

        if (i + 1) % 500 == 0:
            print(f"Published {i + 1}/{args.records} records...")

    producer.flush()
    elapsed = time.time() - start_time
    throughput = args.records / elapsed if elapsed > 0 else 0

    print(f"Done. Published {args.records} records to '{args.topic}' in {elapsed:.2f}s "
          f"=> throughput = {throughput:.2f} records/sec")

    metrics = {
        "topic": args.topic,
        "records_published": args.records,
        "elapsed_seconds": elapsed,
        "producer_throughput_rps": throughput,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    
    print(metrics)


if __name__ == "__main__":
    main()
