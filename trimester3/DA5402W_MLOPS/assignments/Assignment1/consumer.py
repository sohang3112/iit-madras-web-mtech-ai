import time
import threading
from collections import Counter
from kafka import KafkaConsumer

def consume_to_end(consumer, timeout_ms=1000, print_messages=False):
    start = time.time()
    consumed_messages = 0
    partition_counts = Counter()

    while True:
        msg_pack = consumer.poll(timeout_ms=timeout_ms)
        if not msg_pack:
            break

        for tp, messages in msg_pack.items():
            partition_counts[tp.partition] += len(messages)
            for msg in messages:
                if print_messages:
                    print(msg)
                consumed_messages += 1

    elapsed = time.time() - start
    throughput = consumed_messages / elapsed if elapsed > 0 else 0.0
    return consumed_messages, partition_counts, elapsed, throughput

# --- single consumer run ---
consumer = KafkaConsumer(
    'sensor_DA25M622',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='demo-single-consumer'
)

consumed_messages, partition_counts, elapsed, throughput = consume_to_end(consumer, timeout_ms=1000)

print("Number of records consumed:", consumed_messages)
print("Records received per partition:", dict(partition_counts))
print(f"Consumer throughput: {throughput:.2f} records/sec (elapsed {elapsed:.2f}s)")

metrics = consumer.metrics()
print("kafka-metrics-count:", metrics.get('kafka-metrics-count', {}).get('count'))
print("Total number of metric entries returned by consumer.metrics():", len(metrics))

consumer.close()

# --- consumer-group size demonstration ---
def run_consumer_group(num_consumers, group_id):
    consumers = [
        KafkaConsumer(
            'sensor_DA25M622',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=group_id
        )
        for _ in range(num_consumers)
    ]

    results = [None] * num_consumers

    def worker(index, consumer_instance):
        results[index] = consume_to_end(consumer_instance, timeout_ms=1000)
        consumer_instance.close()

    threads = []
    for idx, c in enumerate(consumers):
        t = threading.Thread(target=worker, args=(idx, c))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"\n=== Group '{group_id}' with {num_consumers} consumer(s) ===")
    total = 0
    for idx, (count, partition_counts, elapsed, throughput) in enumerate(results):
        print(f"Consumer {idx}: {count} records, partitions={dict(partition_counts)}, throughput={throughput:.2f} rec/sec")
        total += count
    print(f"Total consumed by group '{group_id}': {total}")

for n in [1, 2, 4]:
    run_consumer_group(n, group_id='demo-group-size')

# --- independent consumer group demonstration ---
for group_id in ['demo-group-A', 'demo-group-B']:
    consumer = KafkaConsumer(
        'sensor_DA25M622',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=group_id
    )
    consumed_messages, partition_counts, elapsed, throughput = consume_to_end(consumer, timeout_ms=1000)
    print(f"\nGroup {group_id} consumed {consumed_messages} records independently.")
    print(f"Partition counts: {dict(partition_counts)}")
    print(f"Throughput: {throughput:.2f} records/sec")
    consumer.close()
