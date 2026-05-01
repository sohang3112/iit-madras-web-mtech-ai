# Reinforcement Learning - notes while reading book

Closed-loop system: learner's actions become future rewards

RL elements: Agent, Environment, Policy (environment -> what action?), Reward signal (at each time step, environment sends a reward; goal is to maximize total reward over time), value function, (optional) a model of environment (planning: state, action -> try predict env's next state, next reward) 

Reward: good immediately short-term: env gives
Value: long-term expectation of total future reward: agent must keep estimating this again & again
Actions are based on values (except in case of RL policy-gradient methods) 

Evolutionary (genetic) algos are alternative to RL: they don't depend on value estimation, generally don't interact with environment ; RL is more efficient usually

Types: Model-based (use model of env to plan) vs model-free (trial & error) 
