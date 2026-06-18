environment (*rewards have randomness!*), action, learner, bandits: 2-armed, policy (history -> action/arm - *may have randomness in chosen arm*)
k-armed (one-armed means 2-armed bandits where one arm's rewards are fixed known)
exploration-exploitation tradeoff

total n rounds in horizon, A is set of all arms

*Book uses Regret to mean Cumulative Regret over all n rounds*.

**Stochastic Bernoulli Bandits**: reward = 0,1; characterized by *mean vector (of all arms)*. Best policy is to always play the arm mean. 

$$Regret = n \max{a \in A} - E[\sum_{t=1}^n X_t]$$

Here first term is best expected reward under best (theoritical) policy, which (if we know true arm means over all n rounds) is to identify at start arm with max mean, and always choose that only.
2nd term is actual learner's total reward - taking expected value to account for all possible histories (as environment and policy both contain randomness).

Above is for cumulative regret; regret for a single action a (called *suboptimality gap* or *action gap* or *immediate regret*) is $\mu - \mu_a^*$ (true mean - estimated mean for action a) -- TODO: CHECK AND UNDERSTAND

A/B Testing: traditionally A/B testing is done (old or new site), then chosen version only is used. With bandits, we could instead always choose which site to show and reward is 1 if user bought product or 0 otherwise.

*Unstructured* (pulling one arm tells nothing about distribution of another arm) vs *Structured* (linear) bandits 

Any good bandit algorithm should have *sub-linear* regret growth.