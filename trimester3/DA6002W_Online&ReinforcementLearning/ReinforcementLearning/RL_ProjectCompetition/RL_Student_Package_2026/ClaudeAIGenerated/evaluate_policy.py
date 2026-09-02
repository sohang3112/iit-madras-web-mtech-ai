import time
import numpy as np
import pandas as pd
from typing import Callable, List, Dict, Any


def evaluate_policy(
    policy: Callable,
    env,
    seeds: List[int],
    scenario_modes: List[str],
    num_products: int = 3,
    episode_length: int = 50,
    verbose: bool = True,
) -> pd.DataFrame:
    """
    Evaluate a policy across multiple seeds and scenario modes.
    
    Parameters
    ----------
    policy : Callable
        Policy function that takes an observation dict and returns a list of 
        order quantities (one per product, in {0, 10, 20, ..., 100}).
    env : IndustrialInventoryEnv
        The environment instance to evaluate against.
    seeds : List[int]
        List of random seeds for evaluation episodes.
    scenario_modes : List[str]
        List of scenario modes (e.g., ["random", "stationary"]).
    num_products : int
        Number of products (default 3).
    episode_length : int
        Length of each episode in days (default 50).
    verbose : bool
        Whether to print progress information.
    
    Returns
    -------
    pd.DataFrame
        Results dataframe with columns:
        - seed, scenario_mode: evaluation conditions
        - total_cost, cost_std: episode cost statistics
        - holding_cost, stockout_cost, ordering_cost, discarding_cost: component costs
        - service_level, unfulfilled_demand: service metrics
        - computation_time: time taken for the episode
        - episode_data: raw episode trajectory (list of dicts)
    """
    results = []
    
    for scenario_mode in scenario_modes:
        for seed in seeds:
            if verbose:
                print(f"Evaluating seed={seed}, scenario_mode='{scenario_mode}'...", end=" ", flush=True)
            
            start_time = time.time()
            
            # Reset environment with the given seed and scenario mode
            observation, info = env.reset(seed=seed)
            
            # Modify environment scenario mode
            env.scenario_mode = scenario_mode
            # Re-reset to apply the scenario mode
            observation, info = env.reset(seed=seed)
            
            episode_trajectory = []
            episode_costs = {
                "holding": 0.0,
                "stockout": 0.0,
                "ordering": 0.0,
                "discarding": 0.0,
            }
            total_demand = 0
            fulfilled_demand = 0
            
            # Run complete episode
            for day in range(episode_length):
                # Get policy action (in order quantities)
                order_quantities = policy(observation)
                
                # Convert to action indices
                action_indices = env.quantities_to_action_indices(order_quantities)
                
                # Step environment
                observation, reward, terminated, truncated, info = env.step(action_indices)
                
                # Extract cost information from step info
                step_info = {
                    "day": day,
                    "inventory": observation["inventory"].copy(),
                    "order_quantities": order_quantities,
                    "reward": reward,
                }
                
                # Accumulate costs from info (if available)
                if "cost_components" in info:
                    costs = info["cost_components"]
                    episode_costs["holding"] += costs.get("holding", 0.0)
                    episode_costs["stockout"] += costs.get("stockout", 0.0)
                    episode_costs["ordering"] += costs.get("ordering", 0.0)
                    episode_costs["discarding"] += costs.get("discarding", 0.0)
                    step_info["cost_components"] = costs
                
                # Track demand fulfillment if available
                if "demand" in info:
                    total_demand += np.sum(info["demand"])
                if "fulfilled_demand" in info:
                    fulfilled_demand += np.sum(info["fulfilled_demand"])
                
                episode_trajectory.append(step_info)
                
                if terminated or truncated:
                    break
            
            # Calculate aggregate episode cost
            total_cost = sum(episode_costs.values())
            
            # Calculate service level
            if total_demand > 0:
                service_level = fulfilled_demand / total_demand
                unfulfilled = total_demand - fulfilled_demand
            else:
                service_level = 1.0
                unfulfilled = 0.0
            
            computation_time = time.time() - start_time
            
            # Record results
            result_record = {
                "seed": seed,
                "scenario_mode": scenario_mode,
                "total_cost": total_cost,
                "holding_cost": episode_costs["holding"],
                "stockout_cost": episode_costs["stockout"],
                "ordering_cost": episode_costs["ordering"],
                "discarding_cost": episode_costs["discarding"],
                "service_level": service_level,
                "unfulfilled_demand": unfulfilled,
                "total_demand": total_demand,
                "computation_time": computation_time,
                "episode_length_actual": len(episode_trajectory),
                "episode_data": episode_trajectory,
            }
            
            results.append(result_record)
            
            if verbose:
                print(f"cost={total_cost:.2f}, service_level={service_level:.3f}, time={computation_time:.3f}s")
    
    # Create results dataframe
    results_df = pd.DataFrame(results)
    
    # Add summary statistics
    if verbose:
        print("\n" + "="*70)
        print("EVALUATION SUMMARY")
        print("="*70)
        
        summary_stats = results_df.groupby("scenario_mode").agg({
            "total_cost": ["mean", "std"],
            "holding_cost": "mean",
            "stockout_cost": "mean",
            "ordering_cost": "mean",
            "discarding_cost": "mean",
            "service_level": "mean",
            "computation_time": "sum",
        }).round(3)
        
        print("\nBy Scenario Mode:")
        print(summary_stats)
        
        print("\nOverall Statistics:")
        print(f"  Average Total Cost:     {results_df['total_cost'].mean():.2f} ± {results_df['total_cost'].std():.2f}")
        print(f"  Average Service Level:  {results_df['service_level'].mean():.3f}")
        print(f"  Total Computation Time: {results_df['computation_time'].sum():.3f}s")
        print("="*70 + "\n")
    
    return results_df


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    """
    Example of how to use the evaluate_policy function in your notebook.
    """
    
    # Assuming 'env' is already created and 'student_config' is available
    # from the notebook setup sections
    
    # Define a simple baseline policy (you'll replace this with your RL policy)
    def baseline_policy(observation):
        """
        Simple baseline: order proportional to recent demand.
        Returns order quantities for 3 products in {0, 10, 20, ..., 100}.
        """
        # Extract recent demand (last 7 days average)
        demand_history = observation["demand_history"]  # shape (7, 3)
        recent_avg_demand = np.mean(demand_history, axis=0)
        
        # Convert to order quantities (scale to 0-100 range)
        # Cap at 100 units max per product
        order_quantities = np.minimum(np.round(recent_avg_demand * 1.2), 100).astype(int)
        
        # Round to nearest 10 (valid action space)
        order_quantities = (order_quantities // 10) * 10
        
        return order_quantities.tolist()
    
    # Example evaluation configuration
    validation_seeds = [42, 123, 456]  # Multiple seeds for robustness
    scenario_modes = ["random", "stationary"]  # Different demand patterns
    
    # Uncomment to run (requires env and student_config from notebook):
    # results_df = evaluate_policy(
    #     policy=baseline_policy,
    #     env=env,
    #     seeds=validation_seeds,
    #     scenario_modes=scenario_modes,
    #     verbose=True,
    # )
    #
    # # Inspect detailed results
    # print("\nDetailed Results:")
    # print(results_df[["seed", "scenario_mode", "total_cost", "service_level"]])
    #
    # # Extract episode trajectory for a specific run
    # first_episode = results_df.iloc[0]["episode_data"]
    # for step in first_episode[:5]:
    #     print(f"Day {step['day']}: inventory={step['inventory']}, cost={step['cost_components']}")
