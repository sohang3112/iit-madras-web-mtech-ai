# ============================================================================
# PASTE THIS INTO THE NOTEBOOK CELL (Section 8, replacing the TODO)
# ============================================================================

import time

def evaluate_policy(policy, env, seeds, scenario_modes, verbose=True):
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
    verbose : bool
        Whether to print progress information.
    
    Returns
    -------
    pd.DataFrame
        Results dataframe with columns:
        - seed, scenario_mode: evaluation conditions
        - total_cost: unscaled episode cost
        - holding_cost, stockout_cost, ordering_cost, discarding_cost: components
        - service_level, unfulfilled_demand: service metrics
        - computation_time: time taken for the episode
        - episode_data: raw trajectory (list of step dicts)
    """
    results = []
    episode_length = 50
    
    for scenario_mode in scenario_modes:
        for seed in seeds:
            if verbose:
                print(f"Evaluating seed={seed:4d}, scenario='{scenario_mode:10s}'...", end=" ", flush=True)
            
            start_time = time.time()
            
            # Reset environment with the given seed and scenario mode
            observation, info = env.reset(seed=seed)
            
            # Modify environment scenario mode and re-reset
            env.scenario_mode = scenario_mode
            observation, info = env.reset(seed=seed)
            
            # Track trajectory and costs
            episode_trajectory = []
            episode_costs = {
                "holding": 0.0,
                "stockout": 0.0,
                "ordering": 0.0,
                "discarding": 0.0,
            }
            total_demand = 0
            fulfilled_demand = 0
            
            # Run complete 50-day episode
            for day in range(episode_length):
                # Get policy action (returns order quantities in {0, 10, ..., 100})
                order_quantities = policy(observation)
                
                # Convert quantities to internal action indices [0, ..., 10]
                action_indices = env.quantities_to_action_indices(order_quantities)
                
                # Execute one step
                observation, reward, terminated, truncated, info = env.step(action_indices)
                
                # Record step information
                step_info = {
                    "day": day,
                    "inventory": observation["inventory"].copy(),
                    "order_quantities": order_quantities,
                    "reward": reward,
                }
                
                # Accumulate costs from step info
                if "cost_components" in info:
                    costs = info["cost_components"]
                    episode_costs["holding"] += costs.get("holding", 0.0)
                    episode_costs["stockout"] += costs.get("stockout", 0.0)
                    episode_costs["ordering"] += costs.get("ordering", 0.0)
                    episode_costs["discarding"] += costs.get("discarding", 0.0)
                    step_info["cost_components"] = costs
                
                # Track demand fulfillment
                if "demand" in info:
                    total_demand += np.sum(info["demand"])
                if "fulfilled_demand" in info:
                    fulfilled_demand += np.sum(info["fulfilled_demand"])
                
                episode_trajectory.append(step_info)
                
                if terminated or truncated:
                    break
            
            # Aggregate metrics
            total_cost = sum(episode_costs.values())
            
            # Service level calculation
            if total_demand > 0:
                service_level = fulfilled_demand / total_demand
                unfulfilled = total_demand - fulfilled_demand
            else:
                service_level = 1.0
                unfulfilled = 0.0
            
            computation_time = time.time() - start_time
            
            # Store results
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
                "episode_data": episode_trajectory,
            }
            
            results.append(result_record)
            
            if verbose:
                print(f"cost={total_cost:8.2f}, svc_lvl={service_level:.3f}, time={computation_time:.2f}s")
    
    # Create results dataframe
    results_df = pd.DataFrame(results)
    
    # Print summary statistics
    if verbose:
        print("\n" + "="*80)
        print("EVALUATION SUMMARY")
        print("="*80)
        
        # Summary by scenario mode
        summary_by_mode = results_df.groupby("scenario_mode").agg({
            "total_cost": ["mean", "std", "min", "max"],
            "holding_cost": "mean",
            "stockout_cost": "mean",
            "ordering_cost": "mean",
            "discarding_cost": "mean",
            "service_level": ["mean", "std"],
            "computation_time": "sum",
        }).round(3)
        
        print("\nResults by Scenario Mode:")
        print(summary_by_mode)
        
        # Overall statistics
        print("\n" + "-"*80)
        print("Overall Statistics (across all seeds & scenarios):")
        print(f"  Total Episodes:         {len(results_df)}")
        print(f"  Average Total Cost:     {results_df['total_cost'].mean():.2f} ± {results_df['total_cost'].std():.2f}")
        print(f"  Best Cost:              {results_df['total_cost'].min():.2f}")
        print(f"  Worst Cost:             {results_df['total_cost'].max():.2f}")
        print(f"  Average Service Level:  {results_df['service_level'].mean():.4f}")
        print(f"  Total Computation Time: {results_df['computation_time'].sum():.2f}s")
        print("="*80 + "\n")
    
    return results_df


# ============================================================================
# CALLING THE EVALUATION FUNCTION (use in a new cell after defining policy)
# ============================================================================

# Example: Baseline random policy
def random_policy(observation):
    """Returns random order quantities in multiples of 10."""
    return [np.random.randint(0, 11) * 10 for _ in range(3)]

# Define evaluation configuration
validation_seeds = [42, 123, 456, 789, 2026]  # 5 different seeds for robustness
scenario_modes = ["random", "stationary"]

# Run evaluation
results_df = evaluate_policy(
    policy=random_policy,  # Replace with your trained policy
    env=env,
    seeds=validation_seeds,
    scenario_modes=scenario_modes,
    verbose=True,
)

# Inspect results
print("Results DataFrame shape:", results_df.shape)
print("\nFirst few rows:")
print(results_df[["seed", "scenario_mode", "total_cost", "service_level", "computation_time"]])

# Extract and visualize episode trajectories
def plot_episode_trajectory(results_df, seed=None, scenario_mode=None):
    """Plot inventory levels for a specific episode."""
    if seed is None:
        seed = results_df.iloc[0]["seed"]
    if scenario_mode is None:
        scenario_mode = results_df.iloc[0]["scenario_mode"]
    
    # Find the episode
    episode_row = results_df[(results_df["seed"] == seed) & 
                             (results_df["scenario_mode"] == scenario_mode)]
    
    if episode_row.empty:
        print(f"No episode found for seed={seed}, scenario={scenario_mode}")
        return
    
    episode_data = episode_row.iloc[0]["episode_data"]
    
    # Extract trajectory data
    days = [step["day"] for step in episode_data]
    inventory_p1 = [step["inventory"][0] for step in episode_data]
    inventory_p2 = [step["inventory"][1] for step in episode_data]
    inventory_p3 = [step["inventory"][2] for step in episode_data]
    
    # Plot
    plt.figure(figsize=(12, 4))
    plt.plot(days, inventory_p1, label="Product 1", marker="o", markersize=3)
    plt.plot(days, inventory_p2, label="Product 2", marker="s", markersize=3)
    plt.plot(days, inventory_p3, label="Product 3", marker="^", markersize=3)
    plt.xlabel("Day")
    plt.ylabel("Inventory Units")
    plt.title(f"Inventory Trajectory (seed={seed}, scenario={scenario_mode})")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Example usage:
# plot_episode_trajectory(results_df, seed=42, scenario_mode="random")
