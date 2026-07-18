"""Ray Tune: 8-trial sweep over a tiny sklearn classifier (ASHA scheduler)."""
import os, ray
from ray import tune
from ray.tune.schedulers import ASHAScheduler

ray.init(address="auto")

def trainable(config):
    from sklearn.datasets import make_classification
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score
    X, y = make_classification(n_samples=400, n_features=20, random_state=0)
    clf = LogisticRegression(C=config["C"], max_iter=int(config["max_iter"]))
    score = cross_val_score(clf, X, y, cv=3).mean()
    tune.report({"accuracy": float(score)})

search_space = {
    "C": tune.loguniform(1e-3, 1e1),
    "max_iter": tune.choice([50, 100, 200, 400]),
}

tuner = tune.Tuner(
    trainable,
    param_space=search_space,
    tune_config=tune.TuneConfig(
        num_samples=8,
        scheduler=ASHAScheduler(metric="accuracy", mode="max"),
    ),
)
results = tuner.fit()
best = results.get_best_result(metric="accuracy", mode="max")
print("best config:", best.config, "accuracy:", best.metrics.get("accuracy"))

out = f"/storage/runs/{__STUDENT_USERNAME}/{__JOB_NAME}/"
os.makedirs(out, exist_ok=True)
with open(out + "best.txt", "w") as f:
    f.write(repr(best.config) + "\n")
print("wrote", out + "best.txt")
