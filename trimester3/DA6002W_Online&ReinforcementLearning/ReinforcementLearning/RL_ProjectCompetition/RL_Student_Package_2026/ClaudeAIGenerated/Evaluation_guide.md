Based on provided starter_notebook.ipynb ONLY , Claude generated the following:

---------

# RL Evaluation Function Implementation Guide

## Overview

This guide explains the complete evaluation function implementation for your IITM Reinforcement Learning course project on Industrial Inventory Control.

## Files Provided

1. **`evaluate_policy.py`** - Standalone module with the evaluation function (can be imported)
2. **`notebook_cell_code.py`** - Ready-to-paste code for your Jupyter notebook
3. **`EVALUATION_GUIDE.md`** - This documentation

## Quick Start

### For Jupyter Notebook (Section 8)

Replace the TODO cell with the code from **`notebook_cell_code.py`**:

```python
# Paste the evaluate_policy function definition here

# Then call it with your policy:
results_df = evaluate_policy(
    policy=your_policy_function,
    env=env,
    seeds=[42, 123, 456],
    scenario_modes=["random", "stationary"],
    verbose=True,
)
```

### For Standalone Use

```python
from evaluate_policy import evaluate_policy

results_df = evaluate_policy(
    policy=policy_function,
    env=env,
    seeds=[42, 123, 456, 789, 2026],
    scenario_modes=["random", "stationary"],
    verbose=True,
)
```

## Function Signature

```python
def evaluate_policy(policy, env, seeds, scenario_modes, verbose=True):
    """
    Evaluate a policy across multiple seeds and scenario modes.
    
    Parameters
    ----------
    policy : Callable
        Function that takes observation dict → list of order quantities
        Returns [qty_p1, qty_p2, qty_p3] where each qty ∈ {0, 10, 20, ..., 100}
    
    env : IndustrialInventoryEnv
        Environment instance (from notebook setup)
    
    seeds : List[int]
        Random seeds for reproducible episodes
        Example: [42, 123, 456, 789, 2026]
    
    scenario_modes : List[str]
        Demand pattern modes: ["random", "stationary", ...]
        "random" uses seasonal/trend/shock combinations
        "stationary" uses fixed patterns
    
    verbose : bool
        Print progress and summary statistics (default: True)
    
    Returns
    -------
    pd.DataFrame
        Results with columns:
        - seed: evaluation seed
        - scenario_mode: demand pattern mode
        - total_cost: sum of all cost components (unscaled)
        - holding_cost: inventory holding cost
        - stockout_cost: demand shortage cost
        - ordering_cost: order processing cost
        - discarding_cost: excess inventory disposal cost
        - service_level: fraction of demand fulfilled (0-1)
        - unfulfilled_demand: units not fulfilled
        - total_demand: total units demanded
        - computation_time: seconds to run episode
        - episode_data: list of step dicts with trajectory details
    """
```

## Policy Function Requirements

Your policy function must:

1. **Accept** a dictionary observation with keys:
   - `inventory`: (3,) array - current stock levels
   - `arrival_pipeline`: (3, 4) array - incoming orders
   - `demand_history`: (7, 3) array - recent demand
   - `day`: (1,) array - current day (0-49)
   - `capacity_utilisation`: (1,) array - warehouse utilization

2. **Return** a list of 3 integers:
   ```python
   return [qty_p1, qty_p2, qty_p3]  # Each in {0, 10, 20, ..., 100}
   ```

3. **Must be deterministic** or use fixed random seeds for reproducibility

### Example Policies

#### Random Baseline
```python
def random_policy(observation):
    """Order random quantities (0-100 in multiples of 10)."""
    return [np.random.randint(0, 11) * 10 for _ in range(3)]
```

#### Demand-Response Policy
```python
def demand_response_policy(observation):
    """Order proportional to recent demand."""
    demand_history = observation["demand_history"]  # (7, 3)
    recent_avg = np.mean(demand_history, axis=0)
    
    # Order 1.2x recent average, capped at 100
    orders = np.minimum(recent_avg * 1.2, 100).astype(int)
    
    # Round to nearest 10
    orders = (orders // 10) * 10
    
    return orders.tolist()
```

#### RL Policy (Neural Network Example)
```python
def nn_policy(observation):
    """RL policy using trained neural network."""
    # Flatten observation
    obs_flat = np.concatenate([
        observation["inventory"],
        observation["arrival_pipeline"].flatten(),
        observation["demand_history"].flatten(),
        observation["day"],
        observation["capacity_utilisation"],
    ]).reshape(1, -1)
    
    # Get NN output
    logits = model.predict(obs_flat)  # shape (1, 11*3)
    action_indices = np.argmax(logits.reshape(3, 11), axis=1)
    
    # Convert to quantities
    quantities = action_indices * 10
    return quantities.tolist()
```

## Understanding the Output

### Results DataFrame

```python
print(results_df.head())
```

Shows one row per (seed, scenario_mode) combination:

```
   seed scenario_mode  total_cost  holding_cost  stockout_cost  ...
0    42        random      2847.3        1205.4         842.1
1   123        random      2965.1        1320.2         644.9
2   456        stationary  2621.5        1089.3         532.2
```

### Summary Statistics

The function prints:

1. **By Scenario Mode**:
   - Mean and std of total_cost
   - Average component costs
   - Average service level

2. **Overall**:
   - Total episodes evaluated
   - Average cost ± std
   - Best and worst costs
   - Average service level

### Example Output

```
================================================================================
EVALUATION SUMMARY
================================================================================

Results by Scenario Mode:
                        total_cost              holding_cost  ...
scenario_mode                           mean       std
random              2903.47  123.45       1242.35  ...
stationary          2621.50         NaN       1089.30  ...

Overall Statistics (across all seeds & scenarios):
  Total Episodes:         6
  Average Total Cost:     2762.49 ± 145.67
  Best Cost:              2621.50
  Worst Cost:             2965.10
  Average Service Level:  0.9847
  Total Computation Time: 3.24s
================================================================================
```

## Accessing Episode Details

Each episode's trajectory is stored in the DataFrame:

```python
# Get first episode data
episode_data = results_df.iloc[0]["episode_data"]

# Each step is a dict with:
for step in episode_data:
    day = step["day"]
    inventory = step["inventory"]  # (3,) array
    order_quantities = step["order_quantities"]  # [qty1, qty2, qty3]
    reward = step["reward"]
    costs = step.get("cost_components", {})  # {holding, stockout, ...}
```

## Recommended Evaluation Strategy

### Development (Local Testing)
```python
# Few seeds, focus on debugging
results_df = evaluate_policy(
    policy=my_policy,
    env=env,
    seeds=[42, 123],
    scenario_modes=["random"],
    verbose=True,
)
```

### Validation (Before Submission)
```python
# Multiple seeds, both scenario types
results_df = evaluate_policy(
    policy=my_policy,
    env=env,
    seeds=[42, 123, 456, 789, 2026],
    scenario_modes=["random", "stationary"],
    verbose=True,
)

# Check variance across seeds
print(results_df.groupby("scenario_mode")["total_cost"].std())
```

### Track in Technique Table (Section 9)

After evaluation, update your technique tracker:

```python
avg_cost = results_df["total_cost"].mean()
technique_tracker.loc[0, "local_average_cost"] = avg_cost
```

## Common Issues & Solutions

### Issue: Policy returns wrong shape
```
Error: Expected [qty1, qty2, qty3], got [[[q1, q2, q3]]]
```
**Solution**: Ensure policy returns flat list:
```python
return np.squeeze(output).tolist()  # or list(output.flatten())
```

### Issue: Quantities outside {0, 10, ..., 100}
```
ValueError: Invalid quantity 55 (not multiple of 10)
```
**Solution**: Round to nearest 10:
```python
quantities = np.round(quantities / 10) * 10
quantities = np.clip(quantities, 0, 100).astype(int)
return quantities.tolist()
```

### Issue: Computation time very high
- Policy inference is slow: profile with `time.time()`
- Environment step is slow: check if `verbose=False` helps
- Consider batch evaluation if policy supports it

### Issue: Service level = 0 or 1 always
- Check if environment provides `demand` and `fulfilled_demand` in info
- Some environment versions may require manual tracking from rewards

## Integration with Your Workflow

### Training Loop
```python
# Train your policy
for episode in range(num_episodes):
    # ... training code ...
    pass

# Evaluate at checkpoints
if episode % 100 == 0:
    results = evaluate_policy(my_policy, env, seeds=[42], scenario_modes=["random"])
    print(f"Checkpoint {episode}: cost = {results['total_cost'].mean():.2f}")
```

### Comparing Techniques
```python
# Evaluate all 5 techniques
techniques = [technique1, technique2, technique3, technique4, technique5]

for i, technique_func in enumerate(techniques):
    results = evaluate_policy(technique_func, env, seeds, scenario_modes)
    avg_cost = results["total_cost"].mean()
    technique_tracker.loc[i, "local_average_cost"] = avg_cost

# Display comparison
print(technique_tracker[["technique", "local_average_cost"]])
```

## Visualization Examples

### Cost per Episode
```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
for scenario in results_df["scenario_mode"].unique():
    data = results_df[results_df["scenario_mode"] == scenario]
    plt.plot(data["seed"], data["total_cost"], marker="o", label=scenario)

plt.xlabel("Seed")
plt.ylabel("Total Cost")
plt.legend()
plt.title("Cost Across Different Seeds")
plt.show()
```

### Cost Component Breakdown
```python
# Average costs by component
components = ["holding_cost", "stockout_cost", "ordering_cost", "discarding_cost"]
avg_costs = [results_df[col].mean() for col in components]

plt.figure(figsize=(8, 5))
plt.bar(components, avg_costs)
plt.ylabel("Average Cost")
plt.title("Cost Component Breakdown")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### Inventory Trajectory
```python
def plot_episode(results_df, seed, scenario_mode):
    """Plot inventory over time for one episode."""
    row = results_df[(results_df["seed"] == seed) & 
                     (results_df["scenario_mode"] == scenario_mode)].iloc[0]
    
    episode = row["episode_data"]
    days = [s["day"] for s in episode]
    inv_p1 = [s["inventory"][0] for s in episode]
    inv_p2 = [s["inventory"][1] for s in episode]
    inv_p3 = [s["inventory"][2] for s in episode]
    
    plt.figure(figsize=(12, 4))
    plt.plot(days, inv_p1, marker="o", label="Product 1")
    plt.plot(days, inv_p2, marker="s", label="Product 2")
    plt.plot(days, inv_p3, marker="^", label="Product 3")
    plt.xlabel("Day")
    plt.ylabel("Inventory (units)")
    plt.title(f"Inventory: seed={seed}, scenario={scenario_mode}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Usage:
plot_episode(results_df, seed=42, scenario_mode="random")
```

## Performance Benchmarks

On a typical laptop, one 50-day episode takes:
- **Simple policy** (e.g., demand-response): ~0.01-0.05 seconds
- **Neural network policy**: ~0.1-0.5 seconds
- **Complex policy** (e.g., MPC): ~1-10 seconds

Total time for 5 seeds × 2 scenarios = 10 episodes:
- Simple: < 1 second
- Neural network: 1-5 seconds
- Complex: 10-100 seconds

## Notes

- **Do not tune on a single favorable seed** - use multiple seeds to avoid overfitting
- **Keep public/private evaluation hidden** - only use the provided validation seeds locally
- **Record your seed and scenario choices** in the brief report
- **Compute unscaled costs** - don't normalize or scale the cost values
- **Service level tracking** depends on environment providing demand information in `info`

## Questions?

Refer to:
1. The notebook demonstration (Section 7) for environment interaction
2. Your course materials for RL technique requirements
3. The `industrial_inventory_env` documentation for environment details