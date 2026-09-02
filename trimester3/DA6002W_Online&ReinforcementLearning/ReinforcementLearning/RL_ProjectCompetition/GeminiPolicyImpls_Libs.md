Yes, there **are** pre-implemented RL libraries that have these out of the box! You do **not** need to hand-roll training loops or custom buffers if you don't want to.

Because you can use any library during training and only need to output artifacts runnable with standard `torch` / `numpy` / `gymnasium` / `stable-baselines3`, you can leverage dedicated libraries like **Tianshou** (for policy gradients and DQN variants) and **skrl** or **Gymnasium Basic RL** (for SARSA and tabular methods).

---

### Library Mapping Overview

| Algorithm                   | Training Library (Pre-Implemented)            | Saved Artifact Format                     | Leaderboard Inference Method         |
| --------------------------- | --------------------------------------------- | ----------------------------------------- | ------------------------------------ |
| **Double DQN**              | `tianshou` or `cleanrl`                       | PyTorch weights (`.pt`) or SB3 checkpoint | `torch.load()` or `DoubleDQN.load()` |
| **REINFORCE**               | `tianshou` (`DiscreteActorPolicy`)            | PyTorch weights (`.pt`)                   | `torch.load()` policy network        |
| **A3C**                     | `tianshou` (asynchronous parallel collector)  | PyTorch weights (`.pt`)                   | `torch.load()` policy network        |
| **Tabular Q-Learning**      | `skrl` (`agents.torch.q_learning.Q_Learning`) | Numpy table (`.npy`)                      | Simple `np.argmax(table[s])` lookup  |
| **Tabular SARSA**           | `skrl` (`agents.torch.sarsa.SARSA`)           | Numpy table (`.npy`)                      | Simple `np.argmax(table[s])` lookup  |
| **NN-based SARSA**          | `skrl` (`SARSA` with MLP Model)               | PyTorch weights (`.pt`)                   | `torch.load()` policy network        |
| **TD($\lambda$) w/ Traces** | `tabular-rl` / `gymnasium-robotics` tools     | Numpy array (`.npy`)                      | Direct table lookup                  |

*(Note: Install `pip install tianshou skrl` in your local/colab training environment only. The leaderboard evaluation machine does not need them.)*

---

### 1. REINFORCE & A3C — Pre-Implemented via `tianshou`

Tianshou provides ready-made, fully tested trainer classes for both vanilla Policy Gradients / REINFORCE and asynchronous Actor-Critic.

#### Training Script (Local / Colab)

```python
import gymnasium as gym
import torch
import torch.nn as nn
from tianshou.algorithm.modelfree.reinforce import DiscreteActorPolicy
from tianshou.data import Collector, VectorReplayBuffer
from tianshou.env import DummyVectorEnv
from tianshou.trainer import OnPolicyTrainer

env_id = "CartPole-v1"
env = gym.make(env_id)
state_shape = env.observation_space.shape or env.observation_space.n
action_shape = env.action_space.shape or env.action_space.n

# Standard PyTorch MLP backbone
net = nn.Sequential(
    nn.Linear(state_shape[0], 128),
    nn.ReLU(),
    nn.Linear(128, action_shape)
)
optim = torch.optim.Adam(net.parameters(), lr=1e-3)

# 1. Built-in REINFORCE Policy
policy = DiscreteActorPolicy(actor=net, optim=optim, gamma=0.99)

# 2. Built-in Rollout Engine & On-Policy Trainer
train_envs = DummyVectorEnv([lambda: gym.make(env_id) for _ in range(4)])
train_collector = Collector(policy, train_envs, VectorReplayBuffer(20000, 4))

trainer = OnPolicyTrainer(
    policy=policy,
    train_collector=train_collector,
    max_epoch=10,
    step_per_epoch=10000,
    repeat_per_collect=1,
    episode_per_test=10,
    batch_size=64,
    step_per_collect=2000,
)
trainer.run()

# Save pure PyTorch weights for the leaderboard
torch.save(net.state_dict(), "reinforce_model.pt")

```

#### Evaluation Script (Leaderboard-Compliant)

```python
import torch
import torch.nn as nn
import gymnasium as gym

# Re-declare identical backbone architecture
def get_actor(obs_dim, act_dim):
    return nn.Sequential(
        nn.Linear(obs_dim, 128),
        nn.ReLU(),
        nn.Linear(128, act_dim)
    )

env = gym.make("CartPole-v1")
model = get_actor(env.observation_space.shape[0], env.action_space.n)
model.load_state_dict(torch.load("reinforce_model.pt"))
model.eval()

# Inference loop using only torch and gymnasium
obs, _ = env.reset()
with torch.no_grad():
    logits = model(torch.tensor(obs, dtype=torch.float32))
    action = torch.argmax(logits).item()

```

---

### 2. Tabular SARSA & Tabular Q-Learning — Pre-Implemented via `skrl`

`skrl` natively features discrete tabular algorithms (`skrl.agents.torch.sarsa.SARSA` and `skrl.agents.torch.q_learning.Q_Learning`) designed for Gym/Gymnasium.

#### Training Script (Local / Colab)

```python
import gymnasium as gym
import numpy as np
from skrl.agents.torch.sarsa import SARSA, SARSA_DEFAULT_CONFIG
from skrl.models.torch import TabularModel
from skrl.trainers.torch import StepTrainer
from skrl.envs.wrappers.torch import wrap_env

# Gymnasium environment (e.g. Taxi-v3, CliffWalking-v0, or discretized CartPole)
raw_env = gym.make("Taxi-v3")
env = wrap_env(raw_env)

# Pre-implemented tabular model and SARSA agent
models = {"policy": TabularModel(env.observation_space, env.action_space)}
cfg = SARSA_DEFAULT_CONFIG.copy()
cfg["timesteps"] = 50000
cfg["learning_rate"] = 0.1
cfg["discount_factor"] = 0.99

agent = SARSA(models=models, memory=None, cfg=cfg, observation_space=env.observation_space, action_space=env.action_space)

trainer = StepTrainer(env=env, agents=agent, timesteps=50000)
trainer.train()

# Export Q-table matrix as a standard numpy array
q_table = agent.models["policy"].table.detach().cpu().numpy()
np.save("sarsa_q_table.npy", q_table)

```

#### Evaluation Script (Leaderboard-Compliant)

```python
import numpy as np
import gymnasium as gym

env = gym.make("Taxi-v3")
q_table = np.load("sarsa_q_table.npy")

obs, _ = env.reset()
# Greedy action inference using only numpy
action = int(np.argmax(q_table[obs]))

```

---

### 3. Double DQN — Native SB3 (No Training Override Needed)

If you prefer staying entirely within `stable-baselines3`, you do not even have to subclass `DQN`. SB3's pre-implemented `DQN` includes a parameter switch for Target Q-learning vs. Double-DQN through policy architecture:

Double DQN is also fully built into **CleanRL** (as a self-contained 1-file script) and **Tianshou** (`tianshou.algorithm.modelfree.dqn.DQNPolicy(..., is_double=True)`):

#### Training with Tianshou's Built-in Double DQN

```python
from tianshou.algorithm.modelfree.dqn import DQNPolicy
import gymnasium as gym
import torch, torch.nn as nn
from tianshou.data import Collector, VectorReplayBuffer
from tianshou.env import DummyVectorEnv
from tianshou.trainer import OffPolicyTrainer

env = gym.make("CartPole-v1")
obs_dim = env.observation_space.shape[0]
act_dim = env.action_space.n

net = nn.Sequential(nn.Linear(obs_dim, 128), nn.ReLU(), nn.Linear(128, act_dim))
optim = torch.optim.Adam(net.parameters(), lr=1e-3)

# Built-in Double DQN flag
policy = DQNPolicy(
    model=net,
    optim=optim,
    discount_factor=0.99,
    estimation_step=1,
    target_update_freq=320,
    is_double=True  # Enables Double-DQN target calculation
)

train_envs = DummyVectorEnv([lambda: gym.make("CartPole-v1") for _ in range(4)])
train_collector = Collector(policy, train_envs, VectorReplayBuffer(20000, 4), exploration_noise=True)

trainer = OffPolicyTrainer(
    policy=policy,
    train_collector=train_collector,
    max_epoch=5,
    step_per_epoch=5000,
    step_per_collect=10,
    update_per_step=0.1,
    batch_size=64
)
trainer.run()

# Save model
torch.save(net.state_dict(), "double_dqn.pt")

```

#### Evaluation Script (Leaderboard-Compliant)

```python
import torch, gymnasium as gym
import torch.nn as nn

net = nn.Sequential(nn.Linear(4, 128), nn.ReLU(), nn.Linear(128, 2))
net.load_state_dict(torch.load("double_dqn.pt"))
net.eval()

env = gym.make("CartPole-v1")
obs, _ = env.reset()
action = net(torch.tensor(obs, dtype=torch.float32)).argmax().item()

```

---

### Summary of What to Run

You can avoid writing custom training loops by using:

1. **`tianshou`** for **REINFORCE**, **A3C**, and **Double DQN**.
2. **`skrl`** for **Tabular Q-Learning**, **Tabular SARSA**, and **NN SARSA**.
3. **`stable-baselines3`** for **PPO**, **A2C**, and **DQN**.

All of them can export standard `.pt` (PyTorch state dicts) or `.npy` (lookup matrices) that run directly on the evaluation server using only `torch` and `numpy`.