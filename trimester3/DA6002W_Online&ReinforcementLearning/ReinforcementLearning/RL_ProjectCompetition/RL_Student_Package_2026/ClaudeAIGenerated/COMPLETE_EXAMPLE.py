"""
COMPLETE EXAMPLE: Evaluation Function Definition & Usage
=========================================================

This file shows the exact code to add to your Jupyter notebook for Section 8.
Copy and paste this into a new cell (or two separate cells) in your notebook.
"""

# ===========================================================================
# CELL 1: Define the evaluation function
# ===========================================================================

import time
import numpy as np
import pandas as pd

def evaluate_policy(policy, env, seeds, scenario_modes, verbose=True):
    """
    Evaluate a reinforcement learning policy across multiple seeds and 
    scenario modes for the Industrial Inventory Control environment.
    
    Parameters
    ----------
    policy : Callable
        Policy function with signature:
            observation_dict -> list of 3 order quantities
        Each quantity must be in {0, 10, 20, ..., 100}
    
    env : IndustrialInventoryEnv
        The environment instance (created in Section 3)
    
    seeds : List[int]
        List of random seeds for evaluation.
        Example: [42, 123, 456, 789, 2026]
    
    scenario_modes : List[str]
        List of demand scenario modes.
        Example: ["random", "stationary"]
    
    verbose : bool
        If True, print progress and summary statistics.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with one row per (seed, scenario_mode) pair.
        Columns:
        - seed, scenario_mode: evaluation parameters
        - total_cost: unscaled episode cost (holding + stockout + ordering + discarding)
        - holding_cost: inventory holding cost
        - stockout_cost: shortage cost
        - ordering_cost: order processing cost
        - discarding_cost: waste disposal cost
        - service_level: fraction of demand fulfilled (0 to 1)
        - unfulfilled_demand: units of unmet demand
        - total_demand: total units demanded during episode
        - computation_time: wall-clock time for episode (seconds)
        - episode_data: list of trajectory dictionaries (one per step)
    """
    results = []
    episode_length = 50  # Fixed 50-day episodes
    
    # Iterate over all (scenario_mode, seed) combinations
    for scenario_mode in scenario_modes:
        for seed in seeds:
            if verbose:
                print(f"Evaluating seed={seed:4d}, scenario='{scenario_mode:10s}'...", end=" ", flush=True)
            
            start_time = time.time()
            
            # Initialize environment with scenario mode and seed
            env.scenario_mode = scenario_mode
            observation, info = env.reset(seed=seed)
            
            # Track trajectory and metrics
            episode_trajectory = []
            episode_costs = {
                "holding": 0.0,
                "stockout": 0.0,
                "ordering": 0.0,
                "discarding": 0.0,
            }
            total_demand = 0.0
            fulfilled_demand = 0.0
            
            # =====================================================================
            # EPISODE LOOP: Run complete 50-day episode
            # =====================================================================
            for day in range(episode_length):
                # 1. Get policy action (order quantities)
                order_quantities = policy(observation)
                
                # 2. Convert order quantities {0, 10, ..., 100} to action indices {0, ..., 10}
                action_indices = env.quantities_to_action_indices(order_quantities)
                
                # 3. Execute step in environment
                observation, reward, terminated, truncated, info = env.step(action_indices)
                
                # 4. Record step data for trajectory
                step_info = {
                    "day": day,
                    "inventory": observation["inventory"].copy(),  # (3,) current inventory
                    "order_quantities": order_quantities,           # [q1, q2, q3]
                    "reward": reward,                               # scalar reward
                }
                
                # 5. Accumulate costs from environment info
                if "cost_components" in info:
                    costs = info["cost_components"]
                    episode_costs["holding"] += costs.get("holding", 0.0)
                    episode_costs["stockout"] += costs.get("stockout", 0.0)
                    episode_costs["ordering"] += costs.get("ordering", 0.0)
                    episode_costs["discarding"] += costs.get("discarding", 0.0)
                    step_info["cost_components"] = costs
                
                # 6. Track demand fulfillment for service level
                if "demand" in info:
                    total_demand += np.sum(info["demand"])  # (3,) demand array
                if "fulfilled_demand" in info:
                    fulfilled_demand += np.sum(info["fulfilled_demand"])  # (3,) fulfilled array
                
                episode_trajectory.append(step_info)
                
                # Stop if episode terminates early
                if terminated or truncated:
                    if verbose:
                        pass  # Will be printed after episode finishes
                    break
            
            # =====================================================================
            # AGGREGATE METRICS
            # =====================================================================
            
            # Total unscaled cost (sum of all components)
            total_cost = sum(episode_costs.values())
            
            # Service level (fulfillment rate)
            if total_demand > 0:
                service_level = fulfilled_demand / total_demand
                unfulfilled_units = total_demand - fulfilled_demand
            else:
                service_level = 1.0  # Perfect service if no demand
                unfulfilled_units = 0.0
            
            computation_time = time.time() - start_time
            
            # Store results for this (seed, scenario_mode) pair
            result_record = {
                "seed": seed,
                "scenario_mode": scenario_mode,
                "total_cost": total_cost,
                "holding_cost": episode_costs["holding"],
                "stockout_cost": episode_costs["stockout"],
                "ordering_cost": episode_costs["ordering"],
                "discarding_cost": episode_costs["discarding"],
                "service_level": service_level,
                "unfulfilled_demand": unfulfilled_units,
                "total_demand": total_demand,
                "computation_time": computation_time,
                "episode_data": episode_trajectory,
            }
            
            results.append(result_record)
            
            if verbose:
                print(f"cost={total_cost:8.2f}, service={service_level:.4f}, time={computation_time:.3f}s")
    
    # =========================================================================
    # CREATE RESULTS DATAFRAME
    # =========================================================================
    results_df = pd.DataFrame(results)
    
    # Print summary statistics to console
    if verbose:
        print("\n" + "="*85)
        print("EVALUATION SUMMARY")
        print("="*85)
        
        # Statistics grouped by scenario mode
        summary_by_mode = results_df.groupby("scenario_mode").agg({
            "total_cost": ["mean", "std", "min", "max"],
            "holding_cost": "mean",
            "stockout_cost": "mean",
            "ordering_cost": "mean",
            "discarding_cost": "mean",
            "service_level": ["mean", "std"],
            "computation_time": "sum",
        }).round(3)
        
        print("\nMetrics by Scenario Mode:")
        print(summary_by_mode)
        
        # Overall statistics
        print("\n" + "-"*85)
        print("Overall Statistics (all seeds and scenarios):")
        print(f"  Total Episodes Evaluated:   {len(results_df)}")
        print(f"  Average Total Cost:         {results_df['total_cost'].mean():.2f} ± {results_df['total_cost'].std():.2f}")
        print(f"  Minimum Cost:               {results_df['total_cost'].min():.2f}")
        print(f"  Maximum Cost:               {results_df['total_cost'].max():.2f}")
        print(f"  Cost Coefficient of Var:    {(results_df['total_cost'].std() / results_df['total_cost'].mean()):.3f}")
        print(f"  Average Service Level:      {results_df['service_level'].mean():.4f} ± {results_df['service_level'].std():.4f}")
        print(f"  Total Computation Time:     {results_df['computation_time'].sum():.2f} seconds")
        print("="*85 + "\n")
    
    return results_df


# ===========================================================================
# CELL 2: Define your policy and call the evaluation function
# ===========================================================================

# Define a simple baseline policy (replace with your trained RL policy)
def simple_baseline_policy(observation):
    """
    Baseline policy: Order proportional to recent demand.
    
    Parameters
    ----------
    observation : dict
        Keys: 'inventory', 'arrival_pipeline', 'demand_history', 'day', 'capacity_utilisation'
    
    Returns
    -------
    list of 3 ints
        Order quantities for 3 products, each in {0, 10, 20, ..., 100}
    """
    # Extract recent demand history (last 7 days, 3 products)
    demand_history = observation["demand_history"]  # shape (7, 3)
    
    # Compute average recent demand per product
    avg_recent_demand = np.mean(demand_history, axis=0)  # shape (3,)
    
    # Order 1.2x recent average (safety stock factor)
    order_quantities = np.minimum(avg_recent_demand * 1.2, 100)
    
    # Round to nearest 10 (valid action space: {0, 10, 20, ..., 100})
    order_quantities = np.round(order_quantities / 10) * 10
    
    # Ensure within bounds and convert to list
    order_quantities = np.clip(order_quantities, 0, 100).astype(int).tolist()
    
    return order_quantities


# ===========================================================================
# Run the evaluation
# ===========================================================================

# Configuration: Use multiple seeds and different scenarios
validation_seeds = [42, 123, 456, 789, 2026]  # 5 diverse seeds for robustness
scenario_modes = ["random", "stationary"]     # Test both demand patterns

# Execute evaluation
results_df = evaluate_policy(
    policy=simple_baseline_policy,  # ← Replace with your trained policy
    env=env,                         # ← Environment from Section 3
    seeds=validation_seeds,
    scenario_modes=scenario_modes,
    verbose=True,  # Print progress and summaries
)

# ===========================================================================
# INSPECT AND ANALYZE RESULTS
# ===========================================================================

# View the results dataframe
print("\nDetailed Results DataFrame:")
print(results_df[["seed", "scenario_mode", "total_cost", "holding_cost", 
                  "stockout_cost", "ordering_cost", "discarding_cost", 
                  "service_level", "computation_time"]])

# Get average cost by scenario
print("\nAverage Cost by Scenario Mode:")
print(results_df.groupby("scenario_mode")["total_cost"].agg(['mean', 'std', 'min', 'max']))

# Get the best performing episode
best_idx = results_df["total_cost"].idxmin()
best_episode = results_df.loc[best_idx]
print(f"\nBest Episode:")
print(f"  Seed: {best_episode['seed']}, Scenario: {best_episode['scenario_mode']}")
print(f"  Cost: {best_episode['total_cost']:.2f}")
print(f"  Service Level: {best_episode['service_level']:.4f}")

# ===========================================================================
# EXTRACT EPISODE TRAJECTORY FOR VISUALIZATION
# ===========================================================================

def extract_episode_trajectory(results_df, seed, scenario_mode):
    """Extract and return trajectory data for a specific episode."""
    row = results_df[(results_df["seed"] == seed) & 
                     (results_df["scenario_mode"] == scenario_mode)]
    
    if row.empty:
        print(f"No episode found for seed={seed}, scenario='{scenario_mode}'")
        return None
    
    episode_data = row.iloc[0]["episode_data"]
    
    # Build trajectory arrays
    trajectory = {
        "days": [],
        "inventory_p1": [],
        "inventory_p2": [],
        "inventory_p3": [],
        "orders_p1": [],
        "orders_p2": [],
        "orders_p3": [],
        "daily_costs": [],
    }
    
    for step in episode_data:
        trajectory["days"].append(step["day"])
        trajectory["inventory_p1"].append(step["inventory"][0])
        trajectory["inventory_p2"].append(step["inventory"][1])
        trajectory["inventory_p3"].append(step["inventory"][2])
        trajectory["orders_p1"].append(step["order_quantities"][0])
        trajectory["orders_p2"].append(step["order_quantities"][1])
        trajectory["orders_p3"].append(step["order_quantities"][2])
        
        # Sum cost components if available
        if "cost_components" in step:
            daily_cost = sum(step["cost_components"].values())
            trajectory["daily_costs"].append(daily_cost)
    
    return trajectory


# Extract trajectory for best episode
best_trajectory = extract_episode_trajectory(
    results_df, 
    seed=best_episode["seed"], 
    scenario_mode=best_episode["scenario_mode"]
)

# ===========================================================================
# PLOTTING EXAMPLE
# ===========================================================================

if best_trajectory is not None:
    # Plot inventory levels over time
    plt.figure(figsize=(14, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(best_trajectory["days"], best_trajectory["inventory_p1"], 
             marker="o", label="Product 1", markersize=3)
    plt.plot(best_trajectory["days"], best_trajectory["inventory_p2"], 
             marker="s", label="Product 2", markersize=3)
    plt.plot(best_trajectory["days"], best_trajectory["inventory_p3"], 
             marker="^", label="Product 3", markersize=3)
    plt.xlabel("Day")
    plt.ylabel("Inventory (units)")
    plt.title(f"Inventory Levels\n(seed={best_episode['seed']}, scenario={best_episode['scenario_mode']})")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot orders over time
    plt.subplot(1, 2, 2)
    plt.plot(best_trajectory["days"], best_trajectory["orders_p1"], 
             marker="o", label="Product 1", markersize=3)
    plt.plot(best_trajectory["days"], best_trajectory["orders_p2"], 
             marker="s", label="Product 2", markersize=3)
    plt.plot(best_trajectory["days"], best_trajectory["orders_p3"], 
             marker="^", label="Product 3", markersize=3)
    plt.xlabel("Day")
    plt.ylabel("Order Quantity (units)")
    plt.title("Order Decisions")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# ===========================================================================
# SAVE RESULTS FOR TECHNIQUE TRACKER (Section 9)
# ===========================================================================

# Update your technique tracker with these results
avg_cost = results_df["total_cost"].mean()
std_cost = results_df["total_cost"].std()

print(f"\nTo update technique_tracker (Section 9):")
print(f"  technique_tracker.loc[YOUR_ROW, 'local_average_cost'] = {avg_cost:.2f}")

# Example for Technique 1:
# technique_tracker.loc[0, "local_average_cost"] = avg_cost
