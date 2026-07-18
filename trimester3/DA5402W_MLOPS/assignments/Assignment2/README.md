Email title: "Assignment 2 Released - DA5402W"
Mlops Assignment Deadline: 22 July

```bash
pip install -U "ray[data,train,tune,serve]"
pip install mlflow
pip install seaborn      # for confusion matrix heatmap
```

Part A done, Part B todo

Ray is also lazy. You can actually load multiple datasets at once -- `ray.data.read_parquet(["path1", "path2"])`

Started Ray instance in seperate terminal before running main Ray script:

```python
>>> import ray
>>> context = ray.init() ; print(context.dashboard_url)
2026-07-18 14:10:59,244	INFO worker.py:2015 -- Started a local Ray instance. View the dashboard at http://127.0.0.1:8265 
http://127.0.0.1:8265
```

