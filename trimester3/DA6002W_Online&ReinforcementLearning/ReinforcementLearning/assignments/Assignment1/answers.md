NOTE: Assignment questions were till lecture 2 - Monte Carlo

## Answer 5 (of MCQ) Explanation

**Question**: Which statement correctly distinguishes policy evaluation and value iteration?

**Correct Answer:** **B**

### Explanation of Options:

* **A. Incorrect:** This statement flips the concepts. Policy evaluation does not find an optimal policy; it calculates the expected returns for a given, fixed policy. Value iteration does not evaluate a fixed policy; it iteratively updates value estimates to find the optimal value function and optimal policy.
* **B. Correct:** Policy evaluation calculates the state-value function $V^\pi(s)$ for a specific, fixed policy $\pi$. Value iteration incorporates a maximization step over all possible actions ($\max_a$) in its update rule to iteratively converge toward the optimal value function $V^*(s)$ and the optimal policy.
* **C. Incorrect:** Both policy evaluation and value iteration are dynamic programming methods. They require a model of the environment, meaning they specifically use transition probabilities and expected rewards rather than requiring observed episodes (which are used in model-free methods like Monte Carlo or Temporal Difference learning).
* **D. Incorrect:** Both standard policy evaluation and value iteration are model-based dynamic programming algorithms, not model-free. They rely on complete knowledge of the environment's transition dynamics.