Stable-Baselines3 (SB3) deliberately excludes tabular methods, vanilla REINFORCE, and SARSA to focus strictly on actor-critic and deep Q-learning architectures. However, you do **not** need to hand-roll messy low-level code from scratch.

By subclassing SB3's existing machinery and writing compact PyTorch modules, you can fulfill all training requirements while exporting standard checkpoints (`.zip` or `.pt`) that evaluate cleanly on the leaderboard using only `torch`, `numpy`, and `gymnasium`.

---

### Strategy & Algorithm Availability

| Algorithm                   | Implementation Approach                                    | Leaderboard Eval Artifact                   |
| --------------------------- | ---------------------------------------------------------- | ------------------------------------------- |
| **Double DQN**              | Subclass `stable_baselines3.DQN` (override `train()`)      | Native SB3 `DoubleDQN.load(...)`            |
| **Tabular Q-Learning**      | Discretization wrapper + Q-table dictionary                | `.npy` / `.pkl` table lookup                |
| **Tabular SARSA**           | Discretization wrapper + On-policy update                  | `.npy` / `.pkl` table lookup                |
| **TD($\lambda$) w/ Traces** | Value estimation + $\epsilon$-greedy action selection      | `.npy` / `.pkl` table + eligibility vectors |
| **NN-based SARSA**          | PyTorch target computation ($Q(s', a')$ instead of $\max$) | Standard PyTorch `state_dict` (`.pt`)       |
| **REINFORCE (w/ baseline)** | PyTorch Policy + Value baseline network                    | Standard PyTorch `state_dict` (`.pt`)       |
| **A3C**                     | Multi-threaded Hogwild PyTorch worker loops                | Standard PyTorch Actor-Critic `state_dict`  |

---

### 1. Double DQN (SB3 Subclass)

Vanilla SB3 `DQN` calculates target values as $r + \gamma \max_{a'} Q_{\text{target}}(s', a')$. Double DQN decouples action selection from evaluation:


$$y = r + \gamma \, Q_{\text{target}}\left(s',\, \arg\max_{a'} Q_{\text{online}}(s', a')\right)$$

Because this subclasses `stable_baselines3.DQN`, it works natively with `.save()` and `.load()` on the leaderboard.

```python
import torch
from stable_baselines3 import DQN

class DoubleDQN(DQN):
    def train(self, gradient_steps: int, batch_size: int = 100) -> None:
        self.policy.set_training_mode(True)
        self._update_learning_rate(self.policy.optimizer)

        losses = []
        for _ in range(gradient_steps):
            replay_data = self.replay_buffer.sample(batch_size, env=self._vec_normalize_env)

            with torch.no_grad():
                # 1. Select greedy actions using ONLINE network
                next_state_actions = self.q_net(replay_data.next_observations).argmax(dim=1, keepdim=True)
                # 2. Evaluate selected actions using TARGET network
                next_q_values = self.q_net_target(replay_data.next_observations).gather(1, next_state_actions)
                target_q_values = replay_data.rewards + (1 - replay_data.dones) * self.gamma * next_q_values

            current_q_values = self.q_net(replay_data.observations).gather(1, replay_data.actions.long())
            loss = torch.nn.functional.smooth_l1_loss(current_q_values, target_q_values)
            losses.append(loss.item())

            self.policy.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.policy.parameters(), self.max_grad_norm)
            self.policy.optimizer.step()

        self._n_updates += gradient_steps
        self.logger.record("train/n_updates", self._n_updates, exclude="tensorboard")
        self.logger.record("train/loss", float(torch.tensor(losses).mean()))

# --- Usage ---
# Train:
# env = gymnasium.make("CartPole-v1")
# model = DoubleDQN("MlpPolicy", env, verbose=0)
# model.learn(total_timesteps=50_000)
# model.save("double_dqn_model")

# Eval:
# model = DoubleDQN.load("double_dqn_model")
# action, _ = model.predict(obs, deterministic=True)

```

---

### 2. Tabular Q-Learning, SARSA, & TD($\lambda$)

If your environment has continuous state observations (like `CartPole-v1` or `LunarLander-v2`), discretize continuous states into discrete bins using `numpy.digitize`.

```python
import numpy as np
import gymnasium as gym

class Discretizer:
    def __init__(self, low, high, bins=(10, 10, 10, 10)):
        self.bins = [np.linspace(l, h, b - 1) for l, h, b in zip(low, high, bins)]

    def transform(self, obs):
        return tuple(int(np.digitize(o, b)) for o, b in zip(obs, self.bins))

def train_tabular(env_id="CartPole-v1", algo="q_learning", episodes=1000, alpha=0.1, gamma=0.99, lam=0.8):
    env = gym.make(env_id)
    disc = Discretizer(env.observation_space.low.clip(-3, 3), env.observation_space.high.clip(-3, 3))
    n_actions = env.action_space.n
    Q = {}
    
    def get_q(s):
        if s not in Q: Q[s] = np.zeros(n_actions)
        return Q[s]

    def eps_greedy(s, eps=0.1):
        if np.random.rand() < eps: return env.action_space.sample()
        return int(np.argmax(get_q(s)))

    for ep in range(episodes):
        obs, _ = env.reset()
        s = disc.transform(obs)
        a = eps_greedy(s)
        E = {} if algo == "td_lambda" else None  # Eligibility traces

        terminated, truncated = False, False
        while not (terminated or truncated):
            next_obs, r, terminated, truncated, _ = env.step(a)
            s_next = disc.transform(next_obs)
            a_next = eps_greedy(s_next)

            if algo == "q_learning":
                target = r + (0 if terminated else gamma * np.max(get_q(s_next)))
                get_q(s)[a] += alpha * (target - get_q(s)[a])
            elif algo == "sarsa":
                target = r + (0 if terminated else gamma * get_q(s_next)[a_next])
                get_q(s)[a] += alpha * (target - get_q(s)[a])
            elif algo == "td_lambda":
                target = r + (0 if terminated else gamma * get_q(s_next)[a_next])
                delta = target - get_q(s)[a]
                E[(s, a)] = E.get((s, a), 0.0) + 1.0
                for (state, act), trace in list(E.items()):
                    get_q(state)[act] += alpha * delta * trace
                    E[(state, act)] = gamma * lam * trace
            
            s, a = s_next, a_next

    # Export compact dictionary
    np.save(f"{algo}_table.npy", Q, allow_pickle=True)

# --- Eval ---
# Q_loaded = np.load("q_learning_table.npy", allow_pickle=True).item()
# disc = Discretizer(env.observation_space.low.clip(-3, 3), env.observation_space.high.clip(-3, 3))
# action = int(np.argmax(Q_loaded.get(disc.transform(obs), np.zeros(env.action_space.n))))

```

---

### 3. Neural Network SARSA & REINFORCE with Baseline

Both algorithms use pure PyTorch (`torch.nn.Module`) and export a `.pt` file loadable anywhere.

**Neural Network SARSA:**

```python
import torch
import torch.nn as nn
import gymnasium as gym
import numpy as np

class QNetwork(nn.Module):
    def __init__(self, obs_dim, act_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 64), nn.ReLU(),
            nn.Linear(64, 64), nn.ReLU(),
            nn.Linear(64, act_dim)
        )
    def forward(self, x):
        return self.net(x)

def train_nn_sarsa(env_id="CartPole-v1", episodes=500, lr=1e-3, gamma=0.99):
    env = gym.make(env_id)
    q_net = QNetwork(env.observation_space.shape[0], env.action_space.n)
    opt = torch.optim.Adam(q_net.parameters(), lr=lr)

    def select_action(s_t, eps):
        if np.random.rand() < eps: return env.action_space.sample()
        with torch.no_grad(): return q_net(s_t).argmax().item()

    for ep in range(episodes):
        obs, _ = env.reset()
        s = torch.tensor(obs, dtype=torch.float32)
        eps = max(0.01, 1.0 - ep / 300)
        a = select_action(s, eps)
        
        terminated, truncated = False, False
        while not (terminated or truncated):
            next_obs, r, terminated, truncated, _ = env.step(a)
            s_next = torch.tensor(next_obs, dtype=torch.float32)
            a_next = select_action(s_next, eps)

            q_val = q_net(s)[a]
            with torch.no_grad():
                q_next_val = 0.0 if terminated else q_net(s_next)[a_next]
                target = r + gamma * q_next_val

            loss = nn.functional.mse_loss(q_val, torch.tensor(target))
            opt.zero_grad()
            loss.backward()
            opt.step()

            s, a = s_next, a_next

    torch.save(q_net.state_dict(), "nn_sarsa.pt")

# --- Eval ---
# net = QNetwork(obs_dim, act_dim)
# net.load_state_dict(torch.load("nn_sarsa.pt"))
# action = net(torch.tensor(obs, dtype=torch.float32)).argmax().item()

```

**REINFORCE with Baseline:**

```python
class REINFORCE(nn.Module):
    def __init__(self, obs_dim, act_dim):
        super().__init__()
        self.actor = nn.Sequential(nn.Linear(obs_dim, 64), nn.ReLU(), nn.Linear(64, act_dim))
        self.critic = nn.Sequential(nn.Linear(obs_dim, 64), nn.ReLU(), nn.Linear(64, 1))

    def forward(self, x):
        logits = self.actor(x)
        val = self.critic(x)
        return torch.distributions.Categorical(logits=logits), val

def train_reinforce(env_id="CartPole-v1", episodes=600, gamma=0.99):
    env = gym.make(env_id)
    model = REINFORCE(env.observation_space.shape[0], env.action_space.n)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)

    for ep in range(episodes):
        obs, _ = env.reset()
        log_probs, values, rewards = [], [], []
        terminated, truncated = False, False

        while not (terminated or truncated):
            s = torch.tensor(obs, dtype=torch.float32)
            dist, val = model(s)
            a = dist.sample()

            log_probs.append(dist.log_prob(a))
            values.append(val.squeeze())

            obs, r, terminated, truncated, _ = env.step(a.item())
            rewards.append(r)

        # Discounted returns
        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)
        returns = torch.tensor(returns)
        values = torch.stack(values)
        log_probs = torch.stack(log_probs)

        advantage = returns - values.detach()
        actor_loss = -(log_probs * advantage).mean()
        critic_loss = nn.functional.mse_loss(values, returns)

        loss = actor_loss + 0.5 * critic_loss
        opt.zero_grad()
        loss.backward()
        opt.step()

    torch.save(model.state_dict(), "reinforce.pt")

# --- Eval ---
# model = REINFORCE(obs_dim, act_dim)
# model.load_state_dict(torch.load("reinforce.pt"))
# action = model.actor(torch.tensor(obs, dtype=torch.float32)).argmax().item()

```

---

### 4. A3C (Asynchronous Advantage Actor-Critic)

A3C uses Python's standard `torch.multiprocessing` to run multiple asynchronous rollout workers against a shared parameter model, completely avoiding any extra dependencies.

```python
import torch
import torch.nn as nn
import torch.multiprocessing as mp
import gymnasium as gym

class SharedActorCritic(nn.Module):
    def __init__(self, obs_dim, act_dim):
        super().__init__()
        self.actor = nn.Sequential(nn.Linear(obs_dim, 64), nn.ReLU(), nn.Linear(64, act_dim))
        self.critic = nn.Sequential(nn.Linear(obs_dim, 64), nn.ReLU(), nn.Linear(64, 1))

    def forward(self, x):
        logits = self.actor(x)
        return torch.distributions.Categorical(logits=logits), self.critic(x)

def worker(worker_id, shared_model, optimizer, env_id, max_steps=10000, gamma=0.99):
    env = gym.make(env_id)
    local_model = SharedActorCritic(env.observation_space.shape[0], env.action_space.n)
    
    step_count = 0
    while step_count < max_steps:
        local_model.load_state_dict(shared_model.state_dict())
        obs, _ = env.reset()
        log_probs, values, rewards = [], [], []
        
        for _ in range(5):  # 5-step rollouts
            s = torch.tensor(obs, dtype=torch.float32)
            dist, val = local_model(s)
            a = dist.sample()
            
            log_probs.append(dist.log_prob(a))
            values.append(val.squeeze())
            
            obs, r, term, trunc, _ = env.step(a.item())
            rewards.append(r)
            step_count += 1
            if term or trunc: break

        with torch.no_grad():
            R = 0.0 if (term or trunc) else local_model(torch.tensor(obs, dtype=torch.float32))[1].item()
        
        returns = []
        for r in reversed(rewards):
            R = r + gamma * R
            returns.insert(0, R)
        returns = torch.tensor(returns)
        values = torch.stack(values)
        log_probs = torch.stack(log_probs)
        
        adv = returns - values
        loss = -(log_probs * adv.detach()).mean() + 0.5 * adv.pow(2).mean()

        optimizer.zero_grad()
        loss.backward()
        # Transfer local gradients to shared model parameters
        for lp, sp in zip(local_model.parameters(), shared_model.parameters()):
            if sp.grad is None:
                sp._grad = lp.grad
            else:
                sp.grad.copy_(lp.grad)
        optimizer.step()

def train_a3c(env_id="CartPole-v1", num_workers=4):
    env = gym.make(env_id)
    shared_model = SharedActorCritic(env.observation_space.shape[0], env.action_space.n)
    shared_model.share_memory()
    optimizer = torch.optim.Adam(shared_model.parameters(), lr=1e-3)

    processes = []
    for rank in range(num_workers):
        p = mp.Process(target=worker, args=(rank, shared_model, optimizer, env_id))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()

    torch.save(shared_model.state_dict(), "a3c.pt")

```

---

### Unified Leaderboard Inference Script

On the evaluation machine, run deterministic actions using only `torch`, `numpy`, and `gymnasium`:

```python
import torch
import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO, A2C, DQN

def evaluate_agent(algo_name, model_path, env_id="CartPole-v1", episodes=10):
    env = gym.make(env_id)
    
    # 1. SB3 standard models
    if algo_name in ["ppo", "a2c", "dqn", "double_dqn"]:
        loader = DoubleDQN if algo_name == "double_dqn" else {"ppo": PPO, "a2c": A2C, "dqn": DQN}[algo_name]
        model = loader.load(model_path)
        policy = lambda o: model.predict(o, deterministic=True)[0]
    
    # 2. Tabular methods
    elif algo_name in ["tabular_q", "tabular_sarsa", "td_lambda"]:
        table = np.load(model_path, allow_pickle=True).item()
        disc = Discretizer(env.observation_space.low.clip(-3, 3), env.observation_space.high.clip(-3, 3))
        policy = lambda o: int(np.argmax(table.get(disc.transform(o), np.zeros(env.action_space.n))))
        
    # 3. PyTorch direct models
    elif algo_name in ["nn_sarsa", "reinforce", "a3c"]:
        obs_dim, act_dim = env.observation_space.shape[0], env.action_space.n
        if algo_name == "nn_sarsa":
            net = QNetwork(obs_dim, act_dim)
            net.load_state_dict(torch.load(model_path))
            policy = lambda o: net(torch.tensor(o, dtype=torch.float32)).argmax().item()
        else:
            net = REINFORCE(obs_dim, act_dim) if algo_name == "reinforce" else SharedActorCritic(obs_dim, act_dim)
            net.load_state_dict(torch.load(model_path))
            policy = lambda o: net(torch.tensor(o, dtype=torch.float32))[0].probs.argmax().item()

    # Evaluation Loop
    total_rewards = []
    for _ in range(episodes):
        obs, _ = env.reset()
        ep_reward = 0
        done = False
        while not done:
            action = policy(obs)
            obs, r, term, trunc, _ = env.step(action)
            ep_reward += r
            done = term or trunc
        total_rewards.append(ep_reward)

    print(f"[{algo_name.upper()}] Mean Reward: {np.mean(total_rewards):.2f} +/- {np.std(total_rewards):.2f}")

```