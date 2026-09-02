Submission Deadlines:
* Project Leaderboard: 2 September
* Project Report (make using given report template LATEX): 4 September

https://35.206.92.146.nip.io/ -- Submit here and see your public eval score and public leaderboard ranking.

NOTE: Need to submit 5 approaches from the following:

- [ ] Tabular Q-Learning
- [ ] Tabular SARSA
- [ ] TD(lambda) with Eligibility Traces
- [ ] Neural Network based Q-Learning
- [ ] Neural Network based SARSA
- [ ] REINFORCE with or without a baseline
- [x] A2C (did no hyper-param tuning etc. right now BUT cost reduced by more than 3 times just by training parallelly on 4 environments instead of one env!!)
    * synchronous, deterministic variant of Asynchronous Advantage Actor Critic (A3C).
    * *Public Leaderboard Cost is 552,491.50*
    * *My local measured eval cost: is 543,485.0.*
- [ ] A3C
- [x] Proximal Policy Optimization (PPO) (did no hyper-param tuning)
    * *Public Leaderboard Cost: 1,224,555.00*
    * *My local measured eval cost: 1,249,722.5*
- [x] DQN (Deep Q Network)
    * *Public Leaderboard Cost: 1,881,862.50* (considerably worse than the other 2 i submitted!)
    * *My local measured eval cost: 1,944,380.0*
- [ ] Double DQN

Arnav (my colleague) said: he is working with DDQN, A3C, A2C, PPO and DQN. He said: I wasted too much time trying to get tabular methods to work as the state and action spaces are fairly discrete or can be easily discretised. I would suggest only working with Neural Nets and surprisingly deep networks did not help my algos at all either. I did run extensive hyper param experiments etc using MLflow etc which helped quite a bit.

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

