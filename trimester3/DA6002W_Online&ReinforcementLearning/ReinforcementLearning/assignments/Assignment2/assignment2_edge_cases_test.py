import json
from pathlib import Path

import gymnasium as gym
import numpy as np

NOTEBOOK_PATH = Path("2026_ID6002W_RL_Programming_Assignment_2.ipynb")


def load_notebook_namespace(notebook_path: Path) -> dict:
    source = json.loads(notebook_path.read_text(encoding="utf-8"))
    namespace: dict = {}
    for cell in source["cells"]:
        if cell.get("cell_type") != "code":
            continue
        cell_source = "".join(cell.get("source", []))
        if not cell_source.strip():
            continue
        exec(cell_source, namespace)
    return namespace


def test_discounted_returns(ns: dict):
    discounted_returns = ns["discounted_returns"]
    out = discounted_returns([1.0, -1.0, 2.0], gamma=0.5)
    assert np.allclose(out, np.array([1.0, 0.0, 2.0], dtype=float))
    empty = discounted_returns([], gamma=0.9)
    assert isinstance(empty, np.ndarray)
    assert empty.shape == (0,)
    print("test_discounted_returns passed")


def test_mc_prediction(ns: dict):
    LoopWorldEnv = ns["LoopWorldEnv"]
    mc_prediction = ns["mc_prediction"]

    def policy(state, rng):
        del state, rng
        return 1

    env = LoopWorldEnv(max_steps=50)
    values_first, counts_first = mc_prediction(env, policy, num_episodes=5, gamma=0.99, visit="first", seed=123)
    assert values_first.shape == (7,)
    assert counts_first.shape == (7,)
    assert counts_first[0] == 0 and counts_first[-1] == 0
    assert values_first[0] == 0.0 and values_first[-1] == 0.0

    env = LoopWorldEnv(max_steps=50)
    values_every, counts_every = mc_prediction(env, policy, num_episodes=5, gamma=0.99, visit="every", seed=123)
    assert counts_every.shape == (7,)
    assert np.all(counts_every >= counts_first)
    assert np.all(counts_every >= 0)
    print("test_mc_prediction passed")


def test_td_lambda_prediction(ns: dict):
    LoopWorldEnv = ns["LoopWorldEnv"]
    td_lambda_prediction = ns["td_lambda_prediction"]

    def policy(state, rng):
        del state, rng
        return 1

    env = LoopWorldEnv(max_steps=50)
    values, diagnostics = td_lambda_prediction(
        env,
        policy,
        num_episodes=3,
        alpha=0.05,
        gamma=0.99,
        lam=0.7,
        seed=42,
    )
    assert values.shape == (7,)
    assert values[0] == 0.0 and values[-1] == 0.0
    assert isinstance(diagnostics, dict)
    assert diagnostics["value_history"].shape == (3, 7)
    print("test_td_lambda_prediction passed")


def test_train_and_predict_values(ns: dict):
    train_value_network = ns["train_value_network"]
    predict_values = ns["predict_values"]
    nn = ns["nn"]

    def policy(state, rng):
        del state, rng
        return 2

    env = gym.make("MountainCar-v0")
    model, diagnostics = train_value_network(env, policy, num_steps=300, gamma=0.99, lr=1e-3, seed=555)
    assert isinstance(model, nn.Module)
    assert diagnostics["loss"].shape == (300,)
    assert isinstance(diagnostics["episode_return"], list)
    assert isinstance(diagnostics["episode_length"], list)
    assert len(diagnostics["episode_return"]) == len(diagnostics["episode_length"])

    states = np.array([[-0.3, 0.0], [0.0, 0.05]], dtype=np.float32)
    values = predict_values(model, states)
    assert values.shape == (2,)
    assert np.all(np.isfinite(values))
    print("test_train_and_predict_values passed")


def run_all():
    ns = load_notebook_namespace(NOTEBOOK_PATH)
    test_discounted_returns(ns)
    test_mc_prediction(ns)
    test_td_lambda_prediction(ns)
    test_train_and_predict_values(ns)
    print("All edge-case tests passed")


if __name__ == "__main__":
    run_all()
