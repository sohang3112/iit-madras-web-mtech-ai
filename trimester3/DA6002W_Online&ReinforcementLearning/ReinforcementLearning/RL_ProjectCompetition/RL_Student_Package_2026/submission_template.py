import numpy as np


def run_policy(observation):
    """
    Return the order quantities for the three products.

    Input:
        observation: Dictionary containing the current environment observation.

    Output:
        A list of three order quantities.
        Each quantity must be one of:
        0, 10, 20, ..., 100
    """

    # Read the required observations
    inventory = np.array(observation["inventory"])
    arrival_pipeline = np.array(observation["arrival_pipeline"])

    # Total stock available now or already scheduled to arrive
    inventory_position = inventory + arrival_pipeline.sum(axis=1)

    # Example policy logic
    # Students must replace this with their trained policy
    target_inventory = np.array([110, 100, 120])

    required_quantity = target_inventory - inventory_position
    required_quantity = np.maximum(required_quantity, 0)

    # Round the order quantity upward to the nearest multiple of 10
    order_quantity = np.ceil(required_quantity / 10) * 10

    # Ensure that the order is between 0 and 100 units
    order_quantity = np.clip(order_quantity, 0, 100)

    return order_quantity.astype(int).tolist()