# Reinforcement Learning - notes while reading book

Closed-loop system: learner's actions become future rewards

RL elements: Agent, Environment, Policy (environment -> what action?), Reward signal (at each time step, environment sends a reward; goal is to maximize total reward over time), value function, (optional) a model of environment (planning: state, action -> try predict env's next state, next reward) 

Reward: good immediately short-term: env gives
Value: long-term expectation of total future reward: agent must keep estimating this again & again
Actions are based on values (except in case of RL policy-gradient methods) 

Evolutionary (genetic) algos are alternative to RL: they don't depend on value estimation, generally don't interact with environment ; RL is more efficient usually

Types: Model-based (use model of env to plan) vs model-free (trial & error) 

*Example: Tic Tac Toe (with Reinforcement Learning)*: RL player, in tree of moves (our move, then opponent move, then our move again, etc.) - most of the time makes "best" move (ie where our probability estimate of winning in one board state is better than all others), but sometimes also makes exploratory moves (not strictly best move). We "learn" during backprop to improve our probability estimate model - from our moves made and opponents' responses (excluding exploratory moves).

win probability estimates is obviously 1 or 0 in won or lost/draw situations - rest are esimates.

EVOLUTIONARY EXAMPLE (where we DON'T learn after every move via value functions as in RL, only directly after game is over):

**Temporal difference learning method**: The "greedy" move (excluding occasional exploratory moves that allow us to see states we may never otherwise see) is given by update rule:

$$V(s) \leftarrow V(s) + \alpha (V(s^`) - V(s))$$

where we update our estimate of value of current state $s$ based on difference between estimated value of $s$ and state after greedy move (anticipatory) $s^`$, $\alpha$ is *step-size parameter*.

Here if step-size is reduced over time, then estimate tends towards true probability estimate, so we tend towards optimal play style (against same opponent who we played with all games). OTOH if step-size is reduced but not completely to 0, then we learn how to play against opponents who slowly change their style of play.

------

*An RL player can achieve effect of planning + look-ahead without actually having a model of opponent and searching through game space tree of possible states.*