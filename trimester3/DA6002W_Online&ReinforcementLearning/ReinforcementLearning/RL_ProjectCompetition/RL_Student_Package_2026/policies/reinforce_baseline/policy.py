from __future__ import annotations
from pathlib import Path
from typing import TypedDict, TYPE_CHECKING
from functools import partial
from collections import deque

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
import gymnasium as gym
from torch.distributions import Categorical

if TYPE_CHECKING:
    from jaxtyping import Int32, Float32

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")


class PolicyNetwork(nn.Module):
    """Policy network for industrial inventory environment."""
    def __init__(self, hidden_dims=[256, 128], num_actions=11):
        super().__init__()
        
        total_state_dim = 3 + 12 + 21 + 1 + 1  # 38 total
        
        layers = []
        prev_dim = total_state_dim
        for h_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, h_dim))
            layers.append(nn.ReLU())
            prev_dim = h_dim
        
        self.shared = nn.Sequential(*layers)
        self.action_head = nn.Linear(prev_dim, 3 * num_actions)
        self.num_actions = num_actions
        
    def forward(self, obs_dict):
        if obs_dict['inventory'].dim() == 1:
            batch_size = 1
            inventory = obs_dict['inventory'].float().unsqueeze(0)
            arrival_pipeline = obs_dict['arrival_pipeline'].float().flatten().unsqueeze(0)
            demand_history = obs_dict['demand_history'].float().flatten().unsqueeze(0)
            day = obs_dict['day'].float().unsqueeze(0)
            capacity_utilisation = obs_dict['capacity_utilisation'].float().unsqueeze(0)
        else:
            batch_size = obs_dict['inventory'].shape[0]
            inventory = obs_dict['inventory'].float()
            arrival_pipeline = obs_dict['arrival_pipeline'].float().view(batch_size, -1)
            demand_history = obs_dict['demand_history'].float().view(batch_size, -1)
            day = obs_dict['day'].float().view(batch_size, -1)
            capacity_utilisation = obs_dict['capacity_utilisation'].float().view(batch_size, -1)
        
        features = torch.cat([inventory, arrival_pipeline, demand_history, day, capacity_utilisation], dim=1)
        x = self.shared(features)
        logits = self.action_head(x)
        logits = logits.view(batch_size, 3, self.num_actions)
        
        if batch_size == 1:
            logits = logits.squeeze(0)
        return logits


class ValueNetwork(nn.Module):
    """Value network for baseline."""
    def __init__(self, hidden_dims=[256, 128]):
        super().__init__()
        
        total_state_dim = 3 + 12 + 21 + 1 + 1
        
        layers = []
        prev_dim = total_state_dim
        for h_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, h_dim))
            layers.append(nn.ReLU())
            prev_dim = h_dim
        
        self.shared = nn.Sequential(*layers)
        self.value_head = nn.Linear(prev_dim, 1)
        
    def forward(self, obs_dict):
        if obs_dict['inventory'].dim() == 1:
            batch_size = 1
            inventory = obs_dict['inventory'].float().unsqueeze(0)
            arrival_pipeline = obs_dict['arrival_pipeline'].float().flatten().unsqueeze(0)
            demand_history = obs_dict['demand_history'].float().flatten().unsqueeze(0)
            day = obs_dict['day'].float().unsqueeze(0)
            capacity_utilisation = obs_dict['capacity_utilisation'].float().unsqueeze(0)
        else:
            batch_size = obs_dict['inventory'].shape[0]
            inventory = obs_dict['inventory'].float()
            arrival_pipeline = obs_dict['arrival_pipeline'].float().view(batch_size, -1)
            demand_history = obs_dict['demand_history'].float().view(batch_size, -1)
            day = obs_dict['day'].float().view(batch_size, -1)
            capacity_utilisation = obs_dict['capacity_utilisation'].float().view(batch_size, -1)
        
        features = torch.cat([inventory, arrival_pipeline, demand_history, day, capacity_utilisation], dim=1)
        x = self.shared(features)
        value = self.value_head(x)
        
        if batch_size == 1:
            value = value.squeeze(0)
        else:
            value = value.squeeze(-1)
        return value


def obs_to_tensor(obs):
    """Convert dictionary observation to tensors."""
    return {
        'inventory': torch.as_tensor(obs['inventory'], dtype=torch.float32, device=DEVICE),
        'arrival_pipeline': torch.as_tensor(obs['arrival_pipeline'], dtype=torch.float32, device=DEVICE),
        'demand_history': torch.as_tensor(obs['demand_history'], dtype=torch.float32, device=DEVICE),
        'day': torch.as_tensor(obs['day'], dtype=torch.float32, device=DEVICE),
        'capacity_utilisation': torch.as_tensor(obs['capacity_utilisation'], dtype=torch.float32, device=DEVICE)
    }


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
policy = PolicyNetwork().to(DEVICE).eval()
policy.load_state_dict(torch.load(script_dir / "best_policy_tuned.pth"))
# for prediction, only policy is used, best_value_net_tuned.pth is ignored

def get_action_and_log_prob(policy, obs_tensor, deterministic=False):
    """
    Get action and log probability from policy.
    
    Args:
        policy: Policy network
        obs_tensor: Dictionary of observation tensors
        deterministic: If True, use argmax instead of sampling
    
    Returns:
        action: Array of 3 integer actions [0, 10]
        log_prob: Log probability of the action
    """
    logits = policy(obs_tensor)  # Shape: [3, num_actions] (no batch dimension)
    
    # Get action for each product
    actions = []
    log_probs = []
    
    for product_idx in range(3):
        product_logits = logits[product_idx]
        
        if deterministic:
            # Take the action with highest probability
            action = torch.argmax(product_logits)
            log_prob = F.log_softmax(product_logits, dim=-1)[action]
        else:
            # Sample from categorical distribution
            dist = Categorical(logits=product_logits)
            action = dist.sample()
            log_prob = dist.log_prob(action)
        
        actions.append(action.item())
        log_probs.append(log_prob)
    
    return np.array(actions, dtype=np.int32), torch.stack(log_probs).sum()

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
    with torch.no_grad():
        obs_tensor = obs_to_tensor(observation)
        action, _ = get_action_and_log_prob(policy, obs_tensor, deterministic=True)
    order_quantities = action * 10
    return order_quantities.tolist()