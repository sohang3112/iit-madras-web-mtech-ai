Week 1: Foundations of Sequential Decision-Making

Lecture 1: The Online Learning Paradigm
Industry use cases: Recommendation systems, logistics matching, dynamic pricing, clinical
trials, and ad selection.
Formalising the Multi-Armed Bandit (MAB): Arms, rewards, horizons, and the exploration–
exploitation tradeoff.
The Bandit-vs-RL contrast: Sequential games (Chess/Go) vs. independent state assumptions
in bandits.
Cumulative regret as the canonical objective for ongoing optimisation.
Simple strategies: The mechanics and production limitations of $\epsilon$-greedy.

Lecture 2: Best-Arm Identification (BAI)
BAI as adaptive A/B testing: Finding the best arm with high confidence.
Statistical foundations: Hoeffding's Inequality and concentration bounds.
Successive elimination algorithms and sample complexity.
Objective selection: When to prioritise BAI over regret minimisation.

Week 2: Stochastic Bandit Algorithms

Lecture 3: UCB Algorithms
Explore-then-Commit (ETC) strategies and the transition from BAI.
The "Optimism in the Face of Uncertainty" principle.
Upper Confidence Bound (UCB1): Derivation, implementation, and regret bounds.

Lecture 4: Thompson Sampling (TS)
Bayesian foundations: Beta–Binomial conjugacy and posterior updates.
Posterior sampling as a randomized exploration strategy.
Empirical comparisons: Performance and robustness to delayed/batched feedback.

Week 3: Practical Stochastic Bandits and Context

Lecture 5: Non-Stationarity and Practical Constraints
Handling distribution shift: Sliding-window UCB and discounted Thompson Sampling.
Case Study: Spotify "Impatient Bandits" (Managing 60-day delayed rewards).
Reward design: Using progressive feedback and intermediate proxies for long-term
engagement.

Lecture 6: Introduction to Contextual Bandits
Incorporating observable context: User features, device, and temporal metadata.
Case Study: Yahoo! Front Page news personalisation.
Modern representations: Two-tower architectures and learned embeddings for context
vectors.

Week 4: Linear Bandit Frameworks

Lecture 7: LinUCB
Linear reward models and parameter estimation via ridge regression.
Geometric intuition: Confidence ellipsoids in high-dimensional feature spaces.
Regret analysis and the impact of feature dimensionality ($d$).

Lecture 8: Linear Thompson Sampling
Bayesian linear regression: Multivariate Gaussian posteriors over weight vectors.
Posterior sampling for structured exploration in linear spaces.
Selection criteria: Comparative advantages of LinUCB vs. Linear TS in production.

Week 5: Evaluation and Production Systems

Lecture 9: Off-Policy Evaluation (OPE)
The "Logging Trap": Requirements for context, action probabilities, and reward logging.
Inverse Propensity Scoring (IPS): Importance weighting and unbiased estimation.

Lecture 10: Production Architectures
System design: Two-stage retrieval funnels (candidate generation) and ranking
architectures.
Exploratory nominators and the impact of retrieval bias.
Case Study: Udemy’s multi-armed bandit infrastructure for item ranking.

Week 6: Resource Constraints and Preference Feedback

Lecture 12: Dueling Bandits
Learning from ordinal feedback: Pairwise user preferences vs. numerical rewards.
Solution concepts: Condorcet winners

Week 7: Structured Feedback and Synthesis

Lecture 13: Cascading Bandits
The cascade click model: Modelling user interaction with ranked lists.
Handling position bias through structural assumptions and examination models.
CascadeUCB: Exploration over slates and ordered items.
