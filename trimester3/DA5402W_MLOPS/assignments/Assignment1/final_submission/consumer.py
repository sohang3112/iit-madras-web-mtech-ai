import threading
import time
from collections import Counter

from kafka import KafkaConsumer
from kafka.structs import TopicPartition


def consume_to_end(
    consumer,
    timeout_ms=1000,
    print_messages=False,
    max_idle_seconds=3,
    max_total_seconds=60,
):
    """Consume until the topic appears idle.

    Instead of breaking on the first empty poll (which often happens during
    group rebalances when multiple consumers join), keep polling until either:
    - we've consumed some messages and been idle for max_idle_seconds, or
    - we've waited more than max_total_seconds with no messages at all.
    """
    start = time.time()
    consumed_messages = 0
    partition_counts = Counter()
    last_message_time = start

    # Trigger initial join/assignment
    consumer.poll(timeout_ms=timeout_ms)

    while True:
        msg_pack = consumer.poll(timeout_ms=timeout_ms)
        now = time.time()

        if msg_pack:
            for tp, messages in msg_pack.items():
                partition_counts[tp.partition] += len(messages)
                for msg in messages:
                    if print_messages:
                        print(msg)
                    consumed_messages += 1
            last_message_time = now
            continue

        # No messages this poll
        # If we've seen messages and been idle for long enough, stop
        if consumed_messages > 0 and (now - last_message_time) >= max_idle_seconds:
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


def print_topic_offsets(consumer, topic):
    """Print beginning/end offsets per partition for topic using this consumer.

    This helps detect if a partition has no data, or if it's offline/unavailable.
    """
    partitions = consumer.partitions_for_topic(topic)
    if not partitions:
        print(f"Topic '{topic}' has no partitions (consumer couldn't find the topic).")
        return

    tps = [TopicPartition(topic, p) for p in sorted(partitions)]
    try:
        begins = consumer.beginning_offsets(tps)
        ends = consumer.end_offsets(tps)
    except Exception as e:
        print(f"Failed to fetch offsets: {e}")
        return

    total = 0
    print(f"Partitions for topic '{topic}': {sorted(partitions)}")
    for tp in tps:
        b = begins.get(tp)
        e = ends.get(tp)
        if b is None or e is None:
            print(f"  Partition {tp.partition}: no offset info (might be offline)")
            continue
        cnt = e - b
        print(f"  Partition {tp.partition}: beginning={b}, end={e}, messages={cnt}")
        total += cnt
    print(f"Total messages available across partitions: {total}")


# --- single consumer run ---
consumer = KafkaConsumer(
    "sensor_DA25M622",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="demo-single-consumer",
)

print_topic_offsets(consumer, "sensor_DA25M622")
consumed_messages, partition_counts, elapsed, throughput = consume_to_end(
    consumer, timeout_ms=1000
)

print("Number of records consumed:", consumed_messages)
print("Records received per partition:", dict(partition_counts))
print(f"Consumer throughput: {throughput:.2f} records/sec (elapsed {elapsed:.2f}s)")

metrics = consumer.metrics()
print("kafka-metrics-count:", metrics.get("kafka-metrics-count", {}).get("count"))
print("Total number of metric entries returned by consumer.metrics():", len(metrics))

consumer.close()


# --- consumer-group size demonstration ---
def run_consumer_group(num_consumers, group_id):
    # Print offsets once before launching consumers
    temp_consumer = KafkaConsumer(
        "sensor_DA25M622",
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=f"{group_id}-probe",
    )
    print_topic_offsets(temp_consumer, "sensor_DA25M622")
    temp_consumer.close()

    consumers = [
        KafkaConsumer(
            "sensor_DA25M622",
            bootstrap_servers=["localhost:9092"],
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id=group_id,
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
        print(
            f"Consumer {idx}: {count} records, partitions={dict(partition_counts)}, throughput={throughput:.2f} rec/sec"
        )
        total += count
    print(f"Total consumed by group '{group_id}': {total}")


for n in [2, 4]:
    run_consumer_group(n, group_id=f"demo-group-of-size-{n}")

# --- independent consumer group demonstration ---
for group_id in ["demo-group-A", "demo-group-B"]:
    consumer = KafkaConsumer(
        "sensor_DA25M622",
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=group_id,
    )
    print_topic_offsets(consumer, "sensor_DA25M622")
    consumed_messages, partition_counts, elapsed, throughput = consume_to_end(
        consumer, timeout_ms=1000
    )
    print(f"\nGroup {group_id} consumed {consumed_messages} records independently.")
    print(f"Partition counts: {dict(partition_counts)}")
    print(f"Throughput: {throughput:.2f} records/sec")
    consumer.close()
