I searched specifically for **copyable/reference implementations**, prioritizing Python + Gym/Gymnasium + NumPy/PyTorch, and not SB3 wrappers.

One important constraint emerges from the search: your professor's environment appears to be a **Dict observation space + MultiDiscrete action space** from your PPO script. Most online implementations assume simple `Discrete` observations/actions, so some algorithms will require an adaptation layer rather than being literal drop-ins. Gymnasium itself is deliberately algorithm-agnostic: the agent only needs to interact through `reset()` and `step()`. ([gymnasium.farama.org][1])

## Best recipes I found

| Required algorithm             | Best online recipe                                           | Fit for your project |
| ------------------------------ | ------------------------------------------------------------ | -------------------- |
| **Tabular Q-Learning**         | Imperial College RL course repo                              | ★★★★☆                |
| **Tabular SARSA**              | MountainCar Q-learning/SARSA repo                            | ★★★★☆                |
| **TD(λ) + eligibility traces** | RL course/research repos below                               | ★★★☆☆                |
| **NN Q-Learning**              | `rlcode/reinforcement-learning`                              | ★★★★★                |
| **NN SARSA**                   | `JohDonald/Deep-Q-Learning-Deep-SARSA-LunarLander-v2`        | ★★★★★                |
| **REINFORCE**                  | Official PyTorch example                                     | ★★★★★                |
| **REINFORCE + baseline**       | `tsen159/REINFORCE-algorithm`                                | ★★★★★                |
| **A3C**                        | `MorvanZhou/pytorch-A3C` / `ikostrikov/pytorch-a3c`          | ★★★★☆                |
| **Double DQN**                 | `dxyang/DQN_pytorch` or `XinJingHao/Duel-Double-DQN-Pytorch` | ★★★★★                |

---

# 1. Tabular Q-Learning

### Best match: Imperial College London

[Imperial College London — RL course repository](https://github.com/ImperialCollegeLondon/ReCoDE-Solving-Combinatorial-Problems-using-Reinforcement-Learning?utm_source=chatgpt.com)

This is particularly good for you because it uses **Gymnasium** and contains an explicit `tabular_q_learning.py`, plus a Jupyter notebook and complete solutions. It even demonstrates applying the algorithm to a custom **News Vendor** environment. ([GitHub][2])

Relevant structure:

```text
notebooks/
    2-Tabular-Q-Learning.ipynb
    solutions/
src/
    rl/
        tabular_q_learning.py
```

This is probably the cleanest recipe to start from.

### Another useful recipe

[Microsoft CyberBattleSim tabular Q-learning notebook](https://github.com/microsoft/CyberBattleSim/blob/main/notebooks/notebook_tabularq.py?utm_source=chatgpt.com)

It is explicitly a **Gymnasium tabular Q-learning agent** and has the complete training loop. ([GitHub][3])

### Important problem for your environment

Tabular Q-learning fundamentally wants something like:

```text
state = integer
action = integer
Q[state, action]
```

Your environment apparently has:

```text
observation = Dict(...)
action = MultiDiscrete(...)
```

So you cannot directly use the usual `Q[state, action]` recipe.

You would first need to decide how to represent your professor's observation as a finite/discrete state. If the observation contains continuous values, a straightforward tabular implementation requires **discretization**.

---

# 2. Tabular SARSA

[Q-Learning and SARSA — MountainCar Gym repository](https://github.com/viniciusenari/Q-Learning-and-SARSA-Mountain-Car-v0?utm_source=chatgpt.com)

This is a particularly useful reference because it contains **both algorithms**, including separate training programs:

```text
train_qlearning.py
train_sarsa.py
run_qlearning_agent.py
run_sarsa_agent.py
```

and saves/loads the learned Q tables. ([GitHub][4])

There's also a very straightforward Gymnasium SARSA implementation:

[BexTuychiev — SARSA Gymnasium implementation](https://gist.github.com/BexTuychiev/1296693d7b50e000aaecf894c3d9537d?utm_source=chatgpt.com)

It explicitly uses:

```python
import gymnasium as gym
```

and implements the Q-table, epsilon-greedy action selection, SARSA update, etc. ([Gist][5])

For your project, I'd use the **Imperial College Q-learning code + this SARSA recipe** as the conceptual pair.

---

# 3. TD(λ) with Eligibility Traces

I found two particularly relevant repositories.

### Best educational/reference repository

[Emilia Nahapetyan — Reinforcement Learning implementations](https://github.com/EmiliaNahapetyan/Reinforcement_Learning?utm_source=chatgpt.com)

This specifically contains:

```text
mountain-car-et/
random-walk-et/
```

for **eligibility traces**, including experiments with TD(λ). ([GitHub][6])

That's much more useful than a generic TD explanation because it contains actual experimental code.

### More directly applicable implementation

[MoliaiELS — RL Project](https://github.com/MoliaiELS/RL_Project?utm_source=chatgpt.com)

This has:

```text
train/train_td.py
```

with:

* `td0`
* `tdlambda`
* eligibility traces
* on-policy next-action bootstrapping

and also has function-approximation variants. ([GitHub][7])

There's even:

```text
train_td_cnn.py
```

for TD(λ) with a neural network and eligibility traces in parameter space.

### Simple code reference

[Hitchhiker's Guide — TD(lambda) implementation](https://github.com/serp-ai/the-hitchhikers-guide-to-machine-learning-algorithms/blob/main/chapters/td-lambda.md?utm_source=chatgpt.com)

The page contains the actual core implementation:

```text
delta = ...
e = gamma * lambda * e + state
theta += alpha * delta * e
```

so it's useful if you want the smallest possible implementation to adapt. ([GitHub][8])

---

# 4. Neural-Network Q-Learning

This is where I would **not** start with a DQN implementation.

You specifically need:

> Neural Network based Q-Learning

which is conceptually **Q-learning + function approximation**, whereas DQN adds replay buffers, target networks, etc.

### Best overall RL implementation repository

[rlcode — Minimal and Clean RL Examples](https://github.com/rlcode/reinforcement-learning?utm_source=chatgpt.com)

This repository has separate implementations including:

```text
Deep SARSA
REINFORCE
...
```

and is designed as relatively minimal examples. ([GitHub][9])

### Another useful repository

[FrozenLakeRL — Q-learning/SARSA/Deep Q-learning/Deep SARSA](https://github.com/MarcinPerka/FrozenLakeRL?utm_source=chatgpt.com)

This is unusually relevant because it implements **all of these in the same repository**:

* Q-learning
* SARSA
* Deep Q-learning
* Deep SARSA
* DQN with target network + replay
* Deep SARSA with target network + replay

([GitHub][10])

That makes it excellent for understanding the progression you're being asked to demonstrate.

---

# 5. Neural-Network SARSA

### Best direct match

[Deep Q-Learning / Deep SARSA — LunarLander](https://github.com/JohDonald/Deep-Q-Learning-Deep-SARSA-LunarLander-v2?utm_source=chatgpt.com)

This is probably my **#1 recommendation for this particular item**.

It has a Jupyter notebook specifically containing:

```text
DSN_and_DQN_LunarLander.ipynb
```

and explicitly implements **Deep SARSA and DQN using PyTorch**. ([GitHub][11])

So you can see the distinction between:

```text
Q-learning:
    target = r + γ max Q(s', a')

SARSA:
    target = r + γ Q(s', a')
```

while keeping essentially the same neural-network machinery.

---

# 6. REINFORCE

### Best choice: official PyTorch

[PyTorch official REINFORCE example](https://github.com/pytorch/examples/blob/main/reinforcement_learning/reinforce.py?utm_source=chatgpt.com)

This is unusually good for your assignment because it:

* uses **Gymnasium**
* uses **PyTorch**
* implements REINFORCE from scratch
* uses `Categorical`
* has an actual training loop
* handles `terminated`
* has model prediction/action sampling

([GitHub][12])

Gymnasium itself also has an official REINFORCE tutorial showing the complete algorithm implemented from scratch with PyTorch. ([gymnasium.farama.org][13])

So for this one I would use the **official PyTorch/Gymnasium recipe**, not a random GitHub implementation.

---

# 7. REINFORCE with a baseline

### Best direct repository

[tsen159 — REINFORCE algorithm](https://github.com/tsen159/REINFORCE-algorithm?utm_source=chatgpt.com)

This repository explicitly contains:

```text
reinforce.py
reinforce_baseline.py
reinforce_gae.py
```

and therefore gives you:

1. vanilla REINFORCE
2. REINFORCE + baseline
3. REINFORCE + GAE

It uses PyTorch and supports discrete environments. ([GitHub][14])

This is probably the **best single recipe** for the two REINFORCE variants you're likely to need.

---

# 8. A3C

### Best simple PyTorch implementation

[MorvanZhou — PyTorch A3C](https://github.com/MorvanZhou/pytorch-A3C?utm_source=chatgpt.com)

This is a simple A3C implementation using:

```text
PyTorch
multiprocessing
Gym
```

and is specifically intended as a relatively simple A3C example. ([GitHub][15])

### More serious implementation

[ikostrikov — PyTorch A3C](https://github.com/ikostrikov/pytorch-a3c?utm_source=chatgpt.com)

This is the implementation repeatedly referenced by other A3C repositories and is based directly on the original asynchronous actor-critic work. ([GitHub][16])

### Another complete implementation

[pranz24 — A3C-GRU](https://github.com/pranz24/A3C-GRU?utm_source=chatgpt.com)

This one explicitly documents:

```text
training
multiple worker processes
evaluation
saved models
```

although it targets older Gym/Atari and therefore requires more adaptation for your environment. ([GitHub][16])

**For your assignment, I'd use MorvanZhou as the easiest code recipe**, rather than the Atari-focused implementations.

---

# 9. Double DQN

You have two very good choices.

### Best simple/reference implementation

[dxyang — DQN / Double DQN / Dueling DQN in PyTorch](https://github.com/dxyang/DQN_pytorch?utm_source=chatgpt.com)

One repository contains:

```text
Vanilla DQN
Double DQN
Dueling DQN
```

with a switch for:

```text
--double-dqn
```

so it's very easy to see exactly what changes between DQN and Double DQN. ([GitHub][17])

### Best modern Gymnasium implementation

[XinJingHao — Duel/Double DQN PyTorch](https://github.com/XinJingHao/Duel-Double-DQN-Pytorch?utm_source=chatgpt.com)

This explicitly supports:

```text
DQN
Double DQN
Dueling DQN
Dueling Double DQN
```

and uses **Gymnasium + PyTorch**. ([GitHub][18])

You can literally disable both enhancements:

```text
Duel=False
Double=False
```

to get ordinary DQN, and:

```text
Duel=False
Double=True
```

to isolate **Double DQN**. ([GitHub][18])

That's extremely useful for your assignment because you're already treating DQN as completed.

---

# A particularly useful repository for your whole project

There is one repository I would keep open while doing the assignment:

[s-4-m-a-n — Hands-on RL implementations](https://github.com/s-4-m-a-n/hands-on-reinforcement-learning?utm_source=chatgpt.com)

The GitHub topic listing describes it as implementing, from scratch:

* Q-learning
* SARSA
* TD learning
* DQN
* PPO
* A2C
* policy gradient
* REINFORCE
* actor-critic

and it was updated in **May 2026**. ([GitHub][19])

Another useful "everything in one place" repository is:

[Aakash Thakare — Reinforcement Learning](https://github.com/Aakashthakre-tech/Reinforcement-Learning?utm_source=chatgpt.com)

Its stated progression is almost exactly your assignment:

```text
Value Based RL
    SARSA
    Q-Learning
    DQN
    Double DQN

Policy Based RL
    REINFORCE

Actor Critic
    A2C
    A3C
    PPO
```

and it uses Gymnasium/PyTorch. ([GitHub][20])

---

## What I would actually use for your assignment

Given your exact requirements and existing **Gymnasium custom environment**, I'd use this mapping:

| Your requirement     | Recipe I'd start from                                    |
| -------------------- | -------------------------------------------------------- |
| Tabular Q-Learning   | **Imperial College**                                     |
| Tabular SARSA        | **BexTuychiev** or Imperial College-style implementation |
| TD(λ)                | **MoliaiELS**                                            |
| Neural Q-Learning    | **rlcode** / FrozenLakeRL                                |
| Neural SARSA         | **JohDonald Deep SARSA**                                 |
| REINFORCE            | **official PyTorch**                                     |
| REINFORCE + baseline | **tsen159**                                              |
| A3C                  | **MorvanZhou**                                           |
| Double DQN           | **XinJingHao** or **dxyang**                             |

### One important architectural issue

Your three existing SB3 algorithms work conveniently because SB3 handles the messy parts of:

```text
Dict observation
        ↓
feature extraction
        ↓
neural network
        ↓
MultiDiscrete action distribution
        ↓
training
```

The hand-written algorithms will **not** automatically handle that.

In particular, **tabular Q-learning/SARSA are the awkward ones**. The online recipes overwhelmingly assume:

```text
Discrete observation
Discrete action
```

while your environment appears to have:

```text
Dict observation
MultiDiscrete action
```

So before copying any recipe, the first thing I'd inspect in the professor's environment is the **exact contents/ranges/dtypes of `observation_space` and `action_space`**. That determines whether each of these nine algorithms can be adapted directly, needs flattening, or needs state/action encoding. The Gymnasium API itself permits arbitrary observation/action structures, but the algorithm implementation has to handle them. ([GitHub][21])

Also, I would **not use CleanRL as the main source for this assignment**. CleanRL is excellent for DQN/PPO/A2C-style implementations, but its current project is primarily aimed at deep RL and its documented dependency versions don't match your `gymnasium>=1.2,<1.4` / `torch>=2.6` environment particularly well. ([GitHub][22])

The recipes above are better because they expose the actual algorithmic training loops rather than hiding them behind an RL framework.

[1]: https://gymnasium.farama.org/?utm_source=chatgpt.com "Gymnasium Documentation"
[2]: https://github.com/ImperialCollegeLondon/ReCoDE-Solving-Combinatorial-Problems-using-Reinforcement-Learning?utm_source=chatgpt.com "GitHub - ImperialCollegeLondon/ReCoDE-Solving-Combinatorial-Problems-using-Reinforcement-Learning: Learn how to model and solve combinatorial problems using Reinforcement Learning. Provided as a ReCoDE Exemplar by Imperial College London. · GitHub"
[3]: https://github.com/microsoft/CyberBattleSim/blob/main/notebooks/notebook_tabularq.py?utm_source=chatgpt.com "CyberBattleSim/notebooks/notebook_tabularq.py at main · microsoft/CyberBattleSim · GitHub"
[4]: https://github.com/viniciusenari/Q-Learning-and-SARSA-Mountain-Car-v0?utm_source=chatgpt.com "GitHub - viniciusenari/Q-Learning-and-SARSA-Mountain-Car-v0: Demonstration of Q-Learning and SARSA algorithms utilizing Python and OpenAI GYM · GitHub"
[5]: https://gist.github.com/BexTuychiev/1296693d7b50e000aaecf894c3d9537d?utm_source=chatgpt.com "sarsa.py · GitHub"
[6]: https://github.com/EmiliaNahapetyan/Reinforcement_Learning?utm_source=chatgpt.com "GitHub - EmiliaNahapetyan/Reinforcement_Learning · GitHub"
[7]: https://github.com/MoliaiELS/RL_Project?utm_source=chatgpt.com "GitHub - MoliaiELS/RL_Project · GitHub"
[8]: https://github.com/serp-ai/the-hitchhikers-guide-to-machine-learning-algorithms/blob/main/chapters/td-lambda.md?utm_source=chatgpt.com "the-hitchhikers-guide-to-machine-learning-algorithms/chapters/td-lambda.md at main · serp-ai/the-hitchhikers-guide-to-machine-learning-algorithms · GitHub"
[9]: https://github.com/rlcode/reinforcement-learning/blob/master/README.md?utm_source=chatgpt.com "reinforcement-learning/README.md at master"
[10]: https://github.com/MarcinPerka/FrozenLakeRL?utm_source=chatgpt.com "Implementation of Reinforcement Learning temporal ..."
[11]: https://github.com/JohDonald/Deep-Q-Learning-Deep-SARSA-LunarLander-v2/blob/main/DSN_and_DQN_LunarLander.ipynb?utm_source=chatgpt.com "DSN_and_DQN_LunarLander.ipynb"
[12]: https://github.com/pytorch/examples/blob/main/reinforcement_learning/reinforce.py?utm_source=chatgpt.com "examples/reinforcement_learning/reinforce.py at main · pytorch/examples · GitHub"
[13]: https://gymnasium.farama.org/v0.27.1/tutorials/training_agents/reinforce_invpend_gym_v26/?utm_source=chatgpt.com "Training using REINFORCE for Mujoco - Gymnasium Documentation"
[14]: https://github.com/tsen159/REINFORCE-algorithm?utm_source=chatgpt.com "GitHub - tsen159/REINFORCE-algorithm: PyTorch implementation of vanilla REINFORCE algorithm, REINFORCE with baseline and REINFORCE with GAE · GitHub"
[15]: https://github.com/topics/actor-critic?utm_source=chatgpt.com "actor-critic"
[16]: https://github.com/pranz24/A3C-GRU?utm_source=chatgpt.com "GitHub - pranz24/A3C-GRU: A3C Algorithm for classic Atari games · GitHub"
[17]: https://github.com/dxyang/DQN_pytorch?utm_source=chatgpt.com "GitHub - dxyang/DQN_pytorch: Vanilla DQN, Double DQN, and Dueling DQN implemented in PyTorch · GitHub"
[18]: https://github.com/XinJingHao/Duel-Double-DQN-Pytorch?utm_source=chatgpt.com "GitHub - XinJingHao/Duel-Double-DQN-Pytorch: A clean and robust implementation of Duel Double DQN · GitHub"
[19]: https://github.com/topics/deep-qlearning-algorithm?utm_source=chatgpt.com "deep-qlearning-algorithm"
[20]: https://github.com/Aakashthakre-tech/Reinforcement-Learning?utm_source=chatgpt.com "GitHub - Aakashthakre-tech/Reinforcement-Learning: A complete Reinforcement Learning journey covering fundamentals to advanced concepts with practical implementations using Gymnasium, NumPy, PyTorch, and modern RL algorithms. · GitHub"
[21]: https://github.com/farama-foundation/gymnasium?utm_source=chatgpt.com "GitHub - Farama-Foundation/Gymnasium: An API standard for single-agent reinforcement learning environments, with popular reference environments and related utilities (formerly Gym) · GitHub"
[22]: https://github.com/vwxyzjn/cleanrl?utm_source=chatgpt.com "GitHub - vwxyzjn/cleanrl: High-quality single file implementation of Deep Reinforcement Learning algorithms with research-friendly features (PPO, DQN, C51, DDPG, TD3, SAC, PPG) · GitHub"
