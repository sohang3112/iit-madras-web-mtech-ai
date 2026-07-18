Email title: "Assignment 2 Released - DA5402W"
Mlops Assignment Deadline: 22 July

```bash
pip install -U "ray[data,train,tune,serve]"
pip install mlflow
pip install seaborn      # for confusion matrix heatmap
```

Part A done, Part B todo

Ray is also lazy. You can actually load multiple datasets at once -- `ray.data.read_parquet(["path1", "path2"])`

<!--
Started Ray instance in seperate terminal before running main Ray script:

```python
>>> import ray
>>> context = ray.init() ; print(context.dashboard_url)
2026-07-18 14:10:59,244	INFO worker.py:2015 -- Started a local Ray instance. View the dashboard at http://127.0.0.1:8265 
http://127.0.0.1:8265
```
-->

Ray script finally ran successfully!
```bash
$ /home/sohang/.local/bin/miniconda3/bin/python train_DA25M622.py
2026-07-18 15:38:24,565 INFO worker.py:2015 -- Started a local Ray instance. View the dashboard at http://127.0.0.1:8266 
╭──────────────────────────────────────────────────────────────────╮
│ Configuration for experiment     trainable_2026-07-18_15-38-26   │
├──────────────────────────────────────────────────────────────────┤
│ Search algorithm                 BasicVariantGenerator           │
│ Scheduler                        AsyncHyperBandScheduler         │
│ Number of trials                 1                               │
╰──────────────────────────────────────────────────────────────────╯

View detailed results here: /home/sohang/ray_results/trainable_2026-07-18_15-38-26
To visualize your results with TensorBoard, run: `tensorboard --logdir /tmp/ray/session_2026-07-18_15-38-10_617960_531994/artifacts/2026-07-18_15-38-26/trainable_2026-07-18_15-38-26/driver_artifacts`

Trial status: 1 PENDING
Current time: 2026-07-18 15:38:26. Total running time: 0s
Logical resource usage: 1.0/1 CPUs, 0/1 GPUs (0.0/1.0 accelerator_type:GeForce-MX130)
╭─────────────────────────────────────────────────────╮
│ Trial name              status       C     max_iter │
├─────────────────────────────────────────────────────┤
│ trainable_9e0d4_00000   PENDING      1          100 │
╰─────────────────────────────────────────────────────╯

Trial trainable_9e0d4_00000 started with configuration:
╭────────────────────────────────────────────╮
│ Trial trainable_9e0d4_00000 config         │
├────────────────────────────────────────────┤
│ C                                        1 │
│ max_iter                               100 │
╰────────────────────────────────────────────╯
(trainable pid=532900) 2026/07/18 15:38:34 INFO mlflow.store.db.utils: Creating initial MLflow database tables...
(trainable pid=532900) 2026/07/18 15:38:34 INFO mlflow.store.db.utils: Updating database tables
(trainable pid=532900) WARNING: Using incubator modules: jdk.incubator.vector
(trainable pid=532900) Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
(trainable pid=532900) Setting default log level to "WARN".
(trainable pid=532900) To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
(trainable pid=532900) 26/07/18 15:38:37 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
[Stage 0:>                                                          (0 + 1) / 1]
                                                                                
[Stage 1:>                                                          (0 + 1) / 1]
                                                                                
[Stage 2:>                                                          (0 + 1) / 1]

Trial status: 1 RUNNING
Current time: 2026-07-18 15:38:56. Total running time: 30s
Logical resource usage: 1.0/1 CPUs, 0/1 GPUs (0.0/1.0 accelerator_type:GeForce-MX130)
╭─────────────────────────────────────────────────────╮
│ Trial name              status       C     max_iter │
├─────────────────────────────────────────────────────┤
│ trainable_9e0d4_00000   RUNNING      1          100 │
╰─────────────────────────────────────────────────────╯
                                                                                
[Stage 13:>                                                         (0 + 1) / 1]
                                                                                
[Stage 15:>                                                         (0 + 1) / 1]
                                                                                
[Stage 17:>                                                         (0 + 1) / 1]
                                                                                
[Stage 19:>                                                         (0 + 1) / 1]
                                                                                
[Stage 21:>                                                         (0 + 1) / 1]
                                                                                
[Stage 30:>                                                         (0 + 1) / 1]
                                                                                
(trainable pid=532900) /home/sohang/Projects/iit-madras-web-mtech-ai/trimester3/DA5402W_MLOPS/assignments/Assignment2/train_DA25M622.py:120: UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
(trainable pid=532900)   fig, ax = plt.subplots(figsize=(6, 5))
Trial status: 1 RUNNING
Current time: 2026-07-18 15:39:26. Total running time: 1min 0s
Logical resource usage: 1.0/1 CPUs, 0/1 GPUs (0.0/1.0 accelerator_type:GeForce-MX130)
╭─────────────────────────────────────────────────────╮
│ Trial name              status       C     max_iter │
├─────────────────────────────────────────────────────┤
│ trainable_9e0d4_00000   RUNNING      1          100 │
╰─────────────────────────────────────────────────────╯

Trial trainable_9e0d4_00000 completed after 1 iterations at 2026-07-18 15:39:44. Total running time: 1min 18s
╭────────────────────────────────────────────────╮
│ Trial trainable_9e0d4_00000 result             │
├────────────────────────────────────────────────┤
│ checkpoint_dir_name                            │
│ time_this_iter_s                       71.4696 │
│ time_total_s                           71.4696 │
│ training_iteration                           1 │
│ accuracy                               0.87978 │
│ f1                                     0.82358 │
╰────────────────────────────────────────────────╯
2026-07-18 15:39:44,988 INFO tune.py:1007 -- Wrote the latest version of all result files and experiment state to '/home/sohang/ray_results/trainable_2026-07-18_15-38-26' in 0.0066s.

Trial status: 1 TERMINATED
Current time: 2026-07-18 15:39:44. Total running time: 1min 18s
Logical resource usage: 0/1 CPUs, 0/1 GPUs (0.0/1.0 accelerator_type:GeForce-MX130)
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Trial name              status         C     max_iter     iter     total time (s)         f1     accuracy │
├───────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ trainable_9e0d4_00000   TERMINATED     1          100        1            71.4696   0.823575     0.879783 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Best config: {'C': 1.0, 'max_iter': 100}
Best F1 score recorded: 0.8235750733889323
```

