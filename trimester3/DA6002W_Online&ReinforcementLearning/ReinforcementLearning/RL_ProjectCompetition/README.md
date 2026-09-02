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
- [x] A2C (*Cost is very bad: 1,619,501.75 (last rank in public leaderboard!)*)
- [ ] A3C
- [ ] Proximal Policy Optimization (PPO)
- [ ] DQN
- [ ] Double DQN

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

