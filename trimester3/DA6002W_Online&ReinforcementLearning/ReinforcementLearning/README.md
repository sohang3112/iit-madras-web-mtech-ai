# Reinforcement Learning

TODO: go over this RL blog post: https://lilianweng.github.io/posts/2018-02-19-rl-overview/

## Markdov Decision Process (MDP)

Present action only depends on previous action and state.

Agent-Environment interaction

State-Transition dynamics of Environment - stochastic or deterministic

State Transision Diagram

Reward (feedback from environment about action taken by agent) is a function of present state, present action and next state. It's a scalar.

Policy function: states -> actions. Stochastic or deterministic.

RL Objective: Learn optimal Policy to maximize expected cumulative reward.

**Learning Optimal Policy (Control)**:
- Episodic (finite pre-determined terminating state) and Continuous (indefinite termination, may never stop - eg. supply chain management, optimized over time) tasks
- *Return* $G_t$ is total cumulative reward agent recieves starting from a particular time step.
- *Discounted Return* $G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + ...$ where $\gamma$ is discount factor (0 to 1) which discounts future rewards. If $\gamma=0$, agent is myopic and only cares about immediate reward. If $\gamma=1$ (can take in Episodic tasks), agent is far-sighted and cares about future rewards as well.

$$G_t = R_{t+1} + \gamma G_{t+1}$$

State Value Function of a state $s$ under policy $\pi$ is expected return starting from that state and following that policy:
$$V^\pi(s) = \mathbb{E}[G_t | S_t = s]$$

Above equation includes probabilistic nature of environment and reward function.

Action Value Function (also called action value or Q-value) of a state-action pair $(s, a)$ under policy $\pi$ is expected return starting from that state, taking that action and following that policy:
$$Q^\pi(s, a) = \mathbb{E}[G_t | S_t = s, A_t = a]$$

State-value functions, denoted as V(s), evaluate the "goodness" of being in a specific state, while action-value functions, denoted as Q(s,a), evaluate the "goodness" of taking a specific action while in that state.

![Tabular Value Function example](images/tabular_value_function_example.png)

![Tabular Value Function example continued](images/tabular_value_function_example1.png)

NOTE: In practice we don't know Value function, so we have to estimate it.

**Bellman Equation**:

![Bellman Equation](images/bellman_equation.png)

Backup Diagram shows how values of a state are updated based on Bellman Equation (nodes are state-action pairs, edges are state transitions, and rewards are associated with edges):

![Backup Diagram](images/backup_diagram.png)

Policy $\pi$ is better than policy $\pi'$ if expected return is greater for all states: $V^\pi(s) \geq V^{\pi'}(s)$ for all states $s$.
For any MDP, there exists an optimal policy $\pi^*$ better than any other policy.

State value of optimal policy is denoted as $V^*(s) = \max_\pi V^\pi(s) \forall s \in S$ and action value of optimal policy is denoted as $Q^*(s, a) = \max_\pi Q^\pi(s, a) \forall s \in S, a \in A$.

Optimal state value = max (for all actions) of optimal action values.

Bellman Optimality Equation for state value function (bellman equation applied to optimal value functions):

![Bellman Optimality Equation for state value function](images/bellman_optimality_equation.png)

If we're able to solve Bellman Optimality Equation, we can get optimal value function and then derive optimal policy from it.

* For a fixed policy, it's a system of linear equations => solvable.
* For optimal value function (i.e. we don't know policy, have to find out!), it's a system of non-linear equations => not solvable in general as expensive and requires state-transition model. We can use iterative methods to approximate the solution.

In practice verifying Markovian properties are followed isn't easy.

RL methods:

* Monte Carlo
* Temporal Difference (TD) Learning
* TODO
* Deep RL

TODO

## Lecture on July 8

(Revision of Monte Carlo Estimation)

Monte Carlo learning is simply this whole iterative process of learning.
In Monte Carlo methods expected values are used as emperical means.

Greedy learning:

Update Q values and improving it in each iteration:
- initially Q value for each action is first return we see from environment
- policy is improved to be $\epsilon$-greedy wrt Q values

On-Policy Learning (we eventually reduce $\epsilon$ to near 0 so policy converges), Off-Policy Learning (straight greedy, no need for epsilon)

Importance Sampling (rarely used nowadays due to better techniques):
* Weigh the returns of behaviour policy b to make them representative of returns of target policy $\pi$
$$\rho_{t:\tau-1} = \Pi_{i=t}^\tau \frac{\pi(A_t|S_t)}{b(A_t|S_t)}$$

Example: Blackjack game - each player's goal is to get cards whose numerical values is as great as possible without exceeding 21
**Exercise**: (TA also will cover later) solve blackjack using RL in python! see rules below:

![Blackjack](images/mdp_blackjack.png)

----------------- END OF MONTE CARLO --------------------------------

### Temporal Difference (TD) Learning Methods

Most central & novel idea to RL !
Can use for both episodic and continous tasks

We don't wait until end of episode to update -- after just 1-2 steps of MDP (partial MDP or bootstrapping) we update

In Incremental Monte Carlo, error is $G_t - V(S_t)$
In TD error, $G_t$ is replaced by TD target based on observed reward and next state at $t+1$ : $R_{t+1} + \gamma S_{t+1}$

So update step becomes:
$$V(S_t) += \alpha (R_{t+1} + \gamma V(S_{t+1}) - V(S_t))$$

Practically Temporal Difference is observed to converge to optimal policy faster than Monte Carlo.

Example: Robot chasing (safe path or shortcut ?):

![Robot: Safe Path or Shortcut?](images/robot_safe_path.png)

TODO
