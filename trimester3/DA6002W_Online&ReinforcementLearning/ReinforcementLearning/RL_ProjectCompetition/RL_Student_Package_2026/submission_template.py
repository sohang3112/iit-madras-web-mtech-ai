from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

import numpy as np

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


class TabularSARSAPolicy:
    def train(self):
        raise NotImplementedError

    def inference(
        self, 
        inventory_position: Int32[np.ndarray, "3"], 
        demand_history: Int32[np.ndarray, "7 3"], 
        day: np.int32,
        capacity_utilisation: np.int32
    ) -> Int32[np.ndarray, "3"]:
        """
        Return the final inventory quantities for the three products (which should be reached after ordering).
        POLICY INFERENCE MUST BE DETERMINISTIC.
    
        Input:
            inventory_position: For each of the 3 products, total stock available now or already scheduled to arrive.
            demand_history: Demand for each of the 3 products observed during the previous seven days, zero-padded at the beginning of an episode.
            day: Current day index (episode ends (truncated=True) after 50 days).
            capacity_utilisation: Current inventory volume / Total warehouse capacity.
        """
        raise NotImplementedError


policy = TabularSARSAPolicy()

# This is the required main function actually called by policy environment. Rest are helpers only.
def run_policy(observation: Observation) -> list[int]:
    """
    Return the order quantities for the three products.

    Deterministic Policy Inference (cannot be stochastic).
    During prior RL training in notebook, stochastic can be used. But here during inference must use a frozen policy.

    Input:
        observation: Dictionary containing the current environment observation. Policy must ONLY RELY ON THIS OBSERVATION.

    Output:
        A list of 3 order quantities to be ordered (for 3 products).
        Each quantity must be one of:
        0, 10, 20, ..., 100
    """
    
    inventory_position = observation["inventory"]+ observation["arrival_pipeline"].sum(axis=1) # Total stock available now or already scheduled to arrive
    target_inventory = policy.inference(
        inventory_position,
        observation['demand_history'],
        observation['day'][0],
        observation['capacity_utilisation'][0]
    )

    required_quantity = target_inventory - inventory_position
    required_quantity = np.maximum(required_quantity, 0)

    # Round the order quantity upward to the nearest multiple of 10
    order_quantity = np.ceil(required_quantity / 10) * 10

    # Ensure that the order is between 0 and 100 units
    order_quantity = np.clip(order_quantity, 0, 100)

    return order_quantity.astype(int).tolist()