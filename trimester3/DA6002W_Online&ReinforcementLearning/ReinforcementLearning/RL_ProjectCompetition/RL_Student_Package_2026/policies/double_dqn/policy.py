from __future__ import annotations
from pathlib import Path
from typing import TypedDict, TYPE_CHECKING

import numpy as np
from stable_baselines3 import DQN
import gymnasium as gym

if TYPE_CHECKING:
    from jaxtyping import Int32, Float32


class Observation(TypedDict):
    """Current environment observation.

    Input:
        inventory (shape (3,)): volumes of the 3 products
        arrival_pipeline (shape (3,4)): For each of the products, outstanding order quantities separated by expected arrival day. 
           The pipeline covers up to 4 days so that the normal maximum lead time and a possible one-day delay are represented.
        demand_history: Demand for each of the 3 products observed during the previous seven days, zero-padded at the beginning of an episode.
        day: Current day index (episode ends (truncated=True) after 50 days).
        capacity_utilisation: Current inventory volume / Total warehouse capacity.
    """

    inventory: Int32[np.ndarray, "3"]
    arrival_pipeline: Int32[np.ndarray, "3 4"]
    demand_history: Int32[np.ndarray, "7 3"]
    day: Int32[np.ndarray, "1"]       # has exactly one value
    capacity_utilisation: Float32[np.ndarray, "1"]      # has exactly one value


script_dir = Path(__file__).parent
# NOTE: at training, DoubleDQN is implemented as a subclass of DQN that overrides only train() function
# since prediction is exactly the same as DQN, we can use DQN.load() to load the trained DoubleDQN model
model = DQN.load(script_dir / "best_tuned_double_dqn.zip")

def run_policy(observation: Observation) -> list[int]:
    """
    Return the order quantities for the three products.

    Input:
        observation: Dictionary containing the current environment observation.

    Output:
        A list of 3 order quantities to be ordered (for 3 products).
        Each quantity must be one of:
        0, 10, 20, ..., 100
    """
    action_scalar, _ = model.predict(observation, deterministic=True)
    # since env defines action_space as MultiDiscrete([11, 11, 11])
    action = np.array(np.unravel_index(action_scalar, (11,11,11))) # convert action_scalar (int) back to list of [int, int, int]
    order_quantities = action * 10
    return order_quantities.tolist()