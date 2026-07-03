Kafka-Based Data Ingestion (20 Marks)

A Kafka producer script is provided to run to get the data stream.

Tasks

1. Create a Kafka topic named:
sensor <rollno>
2. Configure the topic with:
• 3 partitions
• Replication factor = 1
3. Execute the provided producer and verify that records are being published successfully.
4. Consume the records from the topic and verify correct delivery.
5. Collect and report the following metrics:
• Total number of records produced
• Total number of records consumed
• Number of records received from each partition
• Producer throughput (records/sec)
• Consumer throughput (records/sec)
6. Demonstrate the effect of varying the number of consumers:
• One consumer
• Two consumers
• Four consumers
7. Create two different consumer groups and demonstrate that each group consumes the
stream independently.
