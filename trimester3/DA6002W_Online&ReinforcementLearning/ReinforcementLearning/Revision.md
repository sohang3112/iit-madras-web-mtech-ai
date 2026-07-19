NOTE: Intro (course outline) is lecture 0.

**Definitions** (from lecture 1):

$$
G_t = R_{t+1} + \gamma G_{t+1} = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + ... , \quad (\text{Discounted Return}) \\
V^\pi(s) = E[G_t | S_t = s] , \quad (\text{State Value Function}) \\
Q^\pi(s, a) = E[G_t | S_t = s, A_t = a] , \quad (\text{Action Value Function aka Q-value})
$$

**Bellman Optimality Equations** (from lecture 1): Solving the Bellman optimality equation gives the optimal value function and therefore, an optimal policy.

$$
v_*(s) = \max_{a \in A} \sum_{s', r} p(s', r|s, a) (r + \gamma v_\pi(s')), \quad (\text{Optimal State Value}) \\
q_*(s, a) = \sum_{s', r} p(s', r|s, a) (r + \gamma \max_{a^`} q_*(s', a')), \quad (\text{Optimal Action Value}) \\
\pi_*(a|s) = \argmax_a q_*(s,a) , \quad (\text{Optimal Policy})
$$

**Incremental Monte Carlo Update** (from lecture 2) - $0 \le \alpha \le 1$ learning rate is or taken as $1 / n$ (n is total number of times state s or pair (s,a) has been visited till now) ; value updated iteratively by a fraction of error (because multiplied by $\alpha$) leading to reduced error:

$$
V_{n+1}(s) = V_n(s) + \alpha (G - V_n(s)) , \quad (G - V_n(s) \text{is error between observed return (target) and value estimate.}) \\
Q_{n+1}(s,a) = Q_n(s,a) + \alpha (G - Q_n(s,a))
$$

NOTE: Incremental Monte Carlo Update with $\alpha_n = 1/n$ has effect of averaging all returns, but without having to remember all history.

## 1. Markov Decision Process

Outline:
1. Intro to Markov Decision Processes (MDPs)
2. Formulation of an MDP
3. Optimal Policies for MDPs
4. Value Function and Bellman Equation

CORE Markov Property: Next state of the environment only depends on present state and present action but not on the past.
Present state of environment doesn't need to be fully observable (POMDP).

MDP is a formal mathematical formulation of describing agent-environment interactions in RL.

Task is Episodic or Continuous (no termination).

Trajectory is a sequence of states, actions and rewards.

Return: total cumulative reward agent receives starting from a timestamp. 
For Continuous tasks return would be infinite, hence we use Discounted Return only.

Value Functions (comparing policies):
- State Value Function: eval how good a state is for agent based on expected future rewards following policy. Value of terminal state is 0.
- Action Value Function (aka Action Value or Q-value): Estimates how good it is for the agent to take an action in a state in terms of expected future rewards, following a policy

Representing Value Functions:
- Tabular form (for discrete and finite state and action spaces): states or (state,action) pairs with corresponding values
- Parametric form (high dimensional continuous state and action spaces): function approximators (linear, polynomial, neural net based etc.)

Bellman Equations: value of a state or (state,action) pair in terms of possible next states. so recursive
- equations for optimal state & action value functions, and a formula that relates the 2

Bellman Optimality Equations: Value(State under optimal policy) = ExpectedReturn for best action from that state
- for fixed policy forms system of linear equations => solvable
- but finding best policy is hard: maximizing makes it non linear
- solving is tedious, expensive, requires state transition model => so practically iterative solutions used

Policy $\pi$ is better than or equal to $\pi'$ if forall states, value (expected future return) >= other
Optimal Value Policy is better than all others. Optimal state and action value functions are related in formula

Deterministic Optimal Policy must exist in MDP

RL methods to learn Near-Optimal Policies:
1. Monte Carlo Methods
2. Temporal Difference Learning
3. Policy Gradient Methods
4. Actor-Critic Methods
5. Deep RL

## 2. Monte Carlo (MC) Methods

Outline:
1. Intro to MC Methods in RL
2. MC Policy Evaluation
3. MC Control
4. On-Policy and Off-Policy Learning
5. Incremental Monte-Carlo Updates

MC only for episodic tasks; model-free (i.e. no state transition knowledge) - don't need full model of environment because we observe results of policies on whole episodes

Basic Principle: Value is approx Emperical Mean Return (used in place of Expected Return)

Parts:
* MC Policy: Estimate state and action values based on given policy
* MC Control: Update policy towards optimality based on estimated value

### MC Policy

Approach:
* Run policy over all episode, then calc discounted return $G_t$ for each action from that time $t$ to end.
* Calc average return based on all episodes in which $s$ appears

### MC Estimation of state values

Dealing with possibility of same state appearing multiple times in single episode: 1. First Visit MC state estimation 2. Every Visit MC state estimation

**First Visit MC state estimation**:
- Init $V_\pi(s) = 0$, $N(s) = 0$ (no. of first-time state s appeared in an episode), $G(s) = 0$ (total return of state)
- For time t till termination:
  - Sample whole episode (states, actions, returns) till termination
  - Only using state s (if it appeared) first visit in this episode:
    - N(s) += 1
    - Calc $G_t = R_t + \gamma R_{t+1} + ...$ ; G(s) += G(t) [total return]
- Estimated $\hat{v_pi(s)} = G(s) / N(s)$ ; by law of large numbers as $N$ approaches infinity this approaches true value

**Every Visit MC state estimation**: same as First Visit except N(s), G(s) are incremented on every visit to state s not just first in episode

### MC Estimation of action values

With a model, state values are sufficient to determine optimal policy.
But without a model, action values need to be estimated too.

Same as MC estimation of state values, except state visits are replaced by state-action visits

Dealing with problem of (if deterministic policy, same action appears for same state every episode) :
* Exploring starts with random state-action pairs
* Exploring with stochastic policy

Incremental MC update formulae --> written at top of page

MC Control: Policy Evaluation (to get action value) and Policy Improvement (greedy policy wrt action value of policy) are done alternately after every episode of experience to reasonably converge in limited episodes.

### On-Policy and Off-Policy Learning
* On-Policy (eval & improve policy currently being used to make decisions - more stable & better chance of coverage)
* Off-Policy (eval & improve Target Policy, different from Behaviour Policy used to make decisions - less stable, may result in divergence)

**On-Policy MC**:
* *Soft Policy* (eg. $\epsilon$-greedy) is followed to balance exploration & exploitation. Stochastic, all possible actions in a state can be chosen with a non-zero probability.
* Algorithms: 
  * On-Policy First Visit MC Control (similar to prev; steps note TODO; initial all action values 0, uniform policy)
    * Deciding between 2 actions (in a single state) in $\epsilon$-greedy: If one action is greedy, assign it probability $1 - \epsilon$ and other action probability $\epsilon$.
      * Deciding between multiple actions (in a single state)? I think $1 - \epsilon$ for greedy action and $\epsilon / (K-1)$ for all other actions -- not sure TODO
  
**Off-Policy MC**: TODO