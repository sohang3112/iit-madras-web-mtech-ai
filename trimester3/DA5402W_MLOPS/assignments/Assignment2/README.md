Email title: "Assignment 2 Released - DA5402W"
Mlops Assignment Deadline: 22 July

```bash
pip install -U "ray[data,train,tune,serve]"
pip install mlflow
pip install seaborn      # for confusion matrix heatmap
```

`mlflow ui` starts http://localhost:5000 (in the folder where started, saves *mlflow.db* sqlite file)
IMPORTANT: clicking experiments in mlflow ui now by default shows a *GenAI* tab -- have to switch away to *Model Training* tab to view anything actual!

Part A done, Part B done, Part C mlflow pending

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
$ python train_DA25M622.py
Using MLflow tracking URI: http://localhost:5000
2026-07-18 18:12:47,747 INFO worker.py:2015 -- Started a local Ray instance. View the dashboard at http://127.0.0.1:8265 
Mlflow experiment id: 1
╭──────────────────────────────────────────────────────────────────╮
│ Configuration for experiment     trainable_2026-07-18_18-12-49   │
├──────────────────────────────────────────────────────────────────┤
│ Search algorithm                 BasicVariantGenerator           │
│ Scheduler                        AsyncHyperBandScheduler         │
│ Number of trials                 1                               │
╰──────────────────────────────────────────────────────────────────╯

View detailed results here: /home/sohang/ray_results/trainable_2026-07-18_18-12-49
To visualize your results with TensorBoard, run: `tensorboard --logdir /tmp/ray/session_2026-07-18_18-12-39_177327_69038/artifacts/2026-07-18_18-12-49/trainable_2026-07-18_18-12-49/driver_artifacts`

Trial status: 1 PENDING
Current time: 2026-07-18 18:12:49. Total running time: 0s
Logical resource usage: 1.0/1 CPUs, 0/1 GPUs (0.0/1.0 accelerator_type:GeForce-MX130)
╭─────────────────────────────────────────────────────╮
│ Trial name              status       C     max_iter │
├─────────────────────────────────────────────────────┤
│ trainable_2f436_00000   PENDING      1          100 │
╰─────────────────────────────────────────────────────╯

Trial trainable_2f436_00000 started with configuration:
╭────────────────────────────────────────────╮
│ Trial trainable_2f436_00000 config         │
├────────────────────────────────────────────┤
│ C                                        1 │
│ max_iter                               100 │
╰────────────────────────────────────────────╯
(trainable pid=69806) WARNING: Using incubator modules: jdk.incubator.vector
(trainable pid=69806) Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
(trainable pid=69806) Setting default log level to "WARN".
(trainable pid=69806) To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
(trainable pid=69806) 26/07/18 18:12:57 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
[Stage 1:>                                                          (0 + 1) / 1]
                                                                                
[Stage 2:>                                                          (0 + 1) / 1]
                                                                                
[Stage 13:>                                                         (0 + 1) / 1]

Trial status: 1 RUNNING
Current time: 2026-07-18 18:13:19. Total running time: 30s
Logical resource usage: 1.0/1 CPUs, 0/1 GPUs (0.0/1.0 accelerator_type:GeForce-MX130)
╭─────────────────────────────────────────────────────╮
│ Trial name              status       C     max_iter │
├─────────────────────────────────────────────────────┤
│ trainable_2f436_00000   RUNNING      1          100 │
╰─────────────────────────────────────────────────────╯
                                                                                
[Stage 15:>                                                         (0 + 1) / 1]
                                                                                
[Stage 17:>                                                         (0 + 1) / 1]
                                                                                
[Stage 19:>                                                         (0 + 1) / 1]
                                                                                
[Stage 21:>                                                         (0 + 1) / 1]
[Stage 22:>                                                         (0 + 1) / 1]
                                                                                
[Stage 26:>                                                         (0 + 1) / 1]
                                                                                
[Stage 30:>                                                         (0 + 1) / 1]
/home/sohang/Projects/iit-madras-web-mtech-ai/trimester3/DA5402W_MLOPS/assignments/Assignment2/train_DA25M622.py:159: UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
(trainable pid=69806)   fig, ax = plt.subplots(figsize=(6, 5))
Trial status: 1 RUNNING
Current time: 2026-07-18 18:13:49. Total running time: 1min 0s
Logical resource usage: 1.0/1 CPUs, 0/1 GPUs (0.0/1.0 accelerator_type:GeForce-MX130)
╭─────────────────────────────────────────────────────╮
│ Trial name              status       C     max_iter │
├─────────────────────────────────────────────────────┤
│ trainable_2f436_00000   RUNNING      1          100 │
╰─────────────────────────────────────────────────────╯
(trainable pid=69806) 🏃 View run trial-2f436_00000 at: http://localhost:5000/#/experiments/1/runs/fb2fbd13b5c946b2b2323b53fde2f005
(trainable pid=69806) 🧪 View experiment at: http://localhost:5000/#/experiments/1

Trial trainable_2f436_00000 completed after 1 iterations at 2026-07-18 18:13:57. Total running time: 1min 7s
╭────────────────────────────────────────────────╮
│ Trial trainable_2f436_00000 result             │
├────────────────────────────────────────────────┤
│ checkpoint_dir_name                            │
│ time_this_iter_s                       61.5558 │
│ time_total_s                           61.5558 │
│ training_iteration                           1 │
│ accuracy                               0.87978 │
│ f1                                     0.82358 │
╰────────────────────────────────────────────────╯
2026-07-18 18:13:57,113 INFO tune.py:1007 -- Wrote the latest version of all result files and experiment state to '/home/sohang/ray_results/trainable_2026-07-18_18-12-49' in 0.0064s.

Trial status: 1 TERMINATED
Current time: 2026-07-18 18:13:57. Total running time: 1min 7s
Logical resource usage: 0/1 CPUs, 0/1 GPUs (0.0/1.0 accelerator_type:GeForce-MX130)
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Trial name              status         C     max_iter     iter     total time (s)         f1     accuracy │
├───────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ trainable_2f436_00000   TERMINATED     1          100        1            61.5558   0.823575     0.879783 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Best config: {'C': 1.0, 'max_iter': 100}
Best F1 score recorded: 0.8235750733889323
🏃 View run unequaled-hare-281 at: http://localhost:5000/#/experiments/1/runs/5c8580bddf0a4cff8da0a3350113074f
🧪 View experiment at: http://localhost:5000/#/experiments/1
```

Results are in this Ray folder (and mlflow folder `mlruns` got created in current folder -- can start mlflow ui at http://localhost:5000 `MLFLOW_ALLOW_FILE_STORE=true mflow ui` which will auto use ./mlruns folder):

```bash
$ tree /home/sohang/ray_results/trainable_2026-07-18_15-38-26 
/home/sohang/ray_results/trainable_2026-07-18_15-38-26
├── basic-variant-state-2026-07-18_15-38-26.json
├── experiment_state-2026-07-18_15-38-26.json
├── trainable_9e0d4_00000_0_C=1.0000,max_iter=100_2026-07-18_15-38-26
│   ├── events.out.tfevents.1784369313.sohang-VivoBook-ASUS-Laptop-X510UFO
│   ├── params.json
│   ├── params.pkl
│   ├── progress.csv
│   └── result.json
└── tuner.pkl

2 directories, 8 files
```

