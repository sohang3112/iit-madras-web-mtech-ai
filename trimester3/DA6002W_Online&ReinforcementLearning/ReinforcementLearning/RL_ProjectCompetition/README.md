Submission Deadlines:
* Project Leaderboard: 2 September
* Project Report (make using given report template LATEX): 4 September

https://35.206.92.146.nip.io/ -- Submit here and see your public eval score and public leaderboard ranking.

NOTE: Need to submit 5 approaches from the following:

IMPORTANT: hyperparameter tuning in training is compulsory I think -- so do that!!

My submitted RL policies:

| Policy     | Public Leaderboard Cost | Local Eval Cost | Remarks               |
| ---------- | ----------------------- | --------------- | --------------------- |
| A2C        | 552,491.50              | 543,485.0       |
| PPO        | 112,479.75              | 081,770.0       | Hyper-Parameter Tuned |
| DQN        | 116,214.38              | 108,775.0       | Hyper-Parameter Tuned |
| Double DQN | 456,673.50              | 613,727.5       |

the 3 initial tabular methods are NOT FEASIBLE due to very large state & action space of environment.

- [ ] Tabular Q-Learning -- **NOT FEASIBLE**
- [ ] Tabular SARSA -- **NOT FEASIBLE** -- can use tutorials/RL_Gymnasium_MC_SARSA_Tutorial (2).ipynb
- [ ] TD(lambda) with Eligibility Traces -- **NOT FEASIBLE**
- [ ] Neural Network based Q-Learning -- **DOABLE, BUT LOW ON RECOMMENDATION LIST BY Gemini**
- [ ] Neural Network based SARSA -- **NOT RECOMMENDED BY Gemini**
- [ ] REINFORCE with or without a baseline -- **NOT RECOMMENDED BY Gemini**  -- TODO using tutorials/RL_REINFORCE_A2C_A3C_Tutorial_WebMtech.ipynb
    * Gemini says: It is an episodic Monte Carlo method. For supply chain/inventory management environments with horizons of 30–90+ days, cumulative return $G_t$ has massive variance. Even with a learned value baseline, REINFORCE has strictly worse sample efficiency and stability compared to A2C/PPO.
- [x] A2C - **TODO: hyper-parameter tuning**
    * cost reduced by more than 3 times just by training parallelly on 4 environments instead of one env!!
    * synchronous, deterministic variant of Asynchronous Advantage Actor Critic (A3C).
- [ ] A3C -- TODO using tutorials/RL_REINFORCE_A2C_A3C_Tutorial_WebMtech.ipynb
- [x] Proximal Policy Optimization (PPO) - **TODO: hyper-parameter tuning**
- [x] DQN (Deep Q Network) - **TODO: hyper-parameter tuning**
- [x] Double DQN -- **TODO: hyper-parameter tuning**

Arnav (my colleague) said: he is working with:
- [x] Double DQN
- [ ] A3C
- [x] A2C
- [x] PPO
- [x] DQN. 

He said: I wasted too much time trying to get tabular methods to work as the state and action spaces are fairly discrete or can be easily discretised. I would suggest only working with Neural Nets and surprisingly deep networks did not help my algos at all either. I did run extensive hyper param experiments etc using MLflow etc which helped quite a bit.

Gemini says: PPO requires the least hyperparameter tuning, while custom naive neural network methods (lacking replay buffers or target networks) require the most. Note that Stable-Baselines3 (SB3) only natively supports PPO, A2C, and DQN; the remaining methods require custom implementations or third-party extensions. *Have saved its ranking (least to most difficult / require tuning) in CSV*.

It says top 5 (least difficult to tune):

- [x] PPO: builtin
- [ ] DDQN (not builtin, but Gemini said "modded / contrib")
- [x] A2C: builtin
- [x] DQN: builtin
- [ ] A3C: suggested by Arnav, not builtin
- [ ] Tabular Q learning: not builtin

https://stable-baselines3.readthedocs.io/en/master/guide/rl_tips.html says this, so try PPO next! (the others - SAC, TD3, DroQ - don't seem to be part of above options)

List of builtin RL algorithms: https://stable-baselines3.readthedocs.io/en/master/guide/algos.html

> Recent algorithms (PPO, SAC, TD3, DroQ) normally require little hyperparameter tuning, however, don’t expect the default ones to work in every environment.

Full forms are: 
* SAC: Soft Actor-Critic
* TD3: Twin Delayed Deep Deterministic Policy Gradient
* DroQ: Dropout Q-Functions for Doubly Efficient Reinforcement Learning

Submit: *.py* file or else *.zip* archive (it must contain *policy.py* at the root).
**NOTE**: I have put actual leaderboard submissions in policies/ folder. While making zip, ensure to cd into folder first to ensure policy.py is at root of zip, NOT inside a folder:

```bash
# makes zip at: policies/a2c/a2c.zip
$ cd policies/a2c/
$ zip -r a2c.zip *
```

RL_Student_Package_2026 :

* starter_notebook.ipynb - after putting my roll number, it generated my specific randomized parameters

## RL_Course_Project_2026_Problem & Instructions.pdf :

### Problem & Objective/Cost

1. 3 products (diff daily volumes, demands, lead time (see pt 3)), policy called daily => quantities to order for each product (only [0, 10, 20 .. 100]).
2. Total inventory volume (sum of all 3 products' volumes) cannot exceed warehouse capacity => Else Discarding Cost incurred on excess products.
3. Orders arrive after a product-specific lead time. In some episodes, an order may experience a limited one-day delay.

Cost types:

* Holding excess inventory, which consumes warehouse capacity and incurs a daily holding cost.
* Stockouts, which occur when demand exceeds available inventory.
* Ordering, where a fixed cost is incurred whenever a non-zero order is placed for a product.
* Discarding, when arriving inventory causes the volume capacity to be exceeded.

Public Leaderboard & Private Leaderboard tests run on 20 episodes.

1 episode is simulated for 50 days => after that `truncated = True`. `terminated` is always False.

```python
observation, info = env.reset(seed=seed)
next_observation, reward, terminated, truncated, info = env.step(action)
```

