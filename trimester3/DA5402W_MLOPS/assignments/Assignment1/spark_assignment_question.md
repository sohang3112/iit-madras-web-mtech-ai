Part B: Stream Processing using Spark Structured Streaming
(20 Marks)

Using Spark Structured Streaming, implement a real-time preprocessing and analytics pipeline
for the sensor stream obtained from Kafka.

Data Preprocessing
1. Define an appropriate schema for the incoming records.
2. Print the schema .
3. Handle missing values:
• Replace missing temperature values using the average temperature of the same sensor
over the previous 5-minute window, OR report and drop records if insufficient history
exists.
4. Remove duplicate records using:
sensor id + timestamp
5. Identify and remove invalid records:
• Temperature < −20
• Temperature > 100
• Invalid timestamps
6. Convert timestamp strings into Spark Timestamp format.
7. Create the following features:
• Hour of day
• Day of week
• Weekend indicator

Streaming Analytics
8. Compute the average temperature per sensor.
9. Compute the maximum temperature per sensor.
10. Compute the number of active sensors as sensors that have transmitted at least one record
within the last 5 minutes.
11. Compute the distribution of sensor status values.
Event-Time Processing
12. Implement a 5-minute tumbling window and compute the average temperature for each
window.
13. Apply watermarking with a delay threshold of 5 minutes.
14. Inject late events and demonstrate: (i) accepted records (ii) discarded records

Reporting
Generate a summary table containing:
  Metric
  Missing Values Corrected
  Duplicate Records Removed
  Invalid Records Removed
  Late Records Accepted
  Records Discarded by Watermarking
  Performance Analysis
  Collect and report:
    • Input rate (rows/sec)
    • Processing rate (rows/sec)
    • Batch duration
    • State store size (if applicable)
