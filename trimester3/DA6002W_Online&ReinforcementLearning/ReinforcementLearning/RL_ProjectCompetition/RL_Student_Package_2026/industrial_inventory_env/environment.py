"""Gymnasium-compatible three-product industrial inventory environment."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable

import gymnasium as gym
from gymnasium import spaces
import numpy as np

from .config import validate_student_config


class IndustrialInventoryEnv(gym.Env):
    """Multi-product inventory-control environment for the RL course project.

    Internal actions are indices in ``MultiDiscrete([11, 11, 11])``.  Index ``a_i``
    represents an order quantity of ``10 * a_i`` units for product ``i``.

    Parameters
    ----------
    student_config:
        Configuration returned by ``generate_student_config``.
    scenario_mode:
        One of ``"random"``, ``"stationary"``, ``"seasonal"``, ``"trend"``,
        ``"shock"`` or ``"mixed"``.  A sequence such as ``["seasonal", "trend"]``
        is also accepted.
    domain_randomization:
        When True, each episode applies small bounded perturbations around the
        assigned student profile.  All realised values remain within the ranges
        declared in the problem statement.
    """

    metadata = {"render_modes": []}

    NUM_PRODUCTS = 3
    CAPACITY = 1000.0
    PRODUCT_VOLUMES = np.asarray([2.0, 3.0, 1.5], dtype=np.float64)
    HOLDING_COST_PER_VOLUME = 5.0
    STOCKOUT_COSTS = np.asarray([400.0, 500.0, 300.0], dtype=np.float64)
    FIXED_ORDERING_COSTS = np.asarray([80.0, 200.0, 120.0], dtype=np.float64)
    DISCARDING_COSTS = np.asarray([200.0, 250.0, 150.0], dtype=np.float64)
    REFERENCE_LEAD_TIMES = np.asarray([3, 2, 1], dtype=np.int64)
    REFERENCE_DEMAND_MEANS = np.asarray([30.0, 25.0, 35.0], dtype=np.float64)
    HORIZON = 50
    PIPELINE_DAYS = 4
    DEMAND_HISTORY_DAYS = 7

    _VALID_SCENARIO_COMPONENTS = {"seasonal", "trend", "shock"}

    def __init__(
        self,
        student_config: dict[str, Any],
        scenario_mode: str | Iterable[str] = "random",
        domain_randomization: bool = True,
    ) -> None:
        super().__init__()
        validate_student_config(student_config)
        self.student_config = deepcopy(student_config)
        self.scenario_mode = scenario_mode
        self.domain_randomization = bool(domain_randomization)

        self.action_space = spaces.MultiDiscrete(
            np.asarray([11, 11, 11], dtype=np.int64)
        )
        self.observation_space = spaces.Dict(
            {
                "inventory": spaces.Box(
                    low=0,
                    high=1000,
                    shape=(3,),
                    dtype=np.int32,
                ),
                "arrival_pipeline": spaces.Box(
                    low=0,
                    high=10000,
                    shape=(3, 4),
                    dtype=np.int32,
                ),
                "demand_history": spaces.Box(
                    low=0,
                    high=10000,
                    shape=(7, 3),
                    dtype=np.int32,
                ),
                "day": spaces.Box(
                    low=0,
                    high=self.HORIZON,
                    shape=(1,),
                    dtype=np.int32,
                ),
                "capacity_utilisation": spaces.Box(
                    low=0.0,
                    high=1.0,
                    shape=(1,),
                    dtype=np.float32,
                ),
            }
        )

        self.day = 0
        self.inventory = np.zeros(3, dtype=np.int64)
        self.arrival_pipeline = np.zeros((3, 4), dtype=np.int64)
        self.demand_history = np.zeros((7, 3), dtype=np.int64)
        self.episode_cost = 0.0
        self.episode_parameters: dict[str, Any] = {}
        self._demand_sequence = np.zeros((self.HORIZON, 3), dtype=np.int64)
        self._delay_flags = np.zeros((self.HORIZON, 3), dtype=bool)

    @staticmethod
    def quantities_to_action_indices(quantities: Iterable[int]) -> np.ndarray:
        """Convert actual order quantities to internal action indices."""
        array = np.asarray(list(quantities))
        if array.shape != (3,):
            raise ValueError("Order quantities must contain exactly three values.")
        if not np.issubdtype(array.dtype, np.number):
            raise TypeError("Order quantities must be numeric.")
        if not np.all(np.isfinite(array)):
            raise ValueError("Order quantities must be finite.")
        if not np.all(array == np.round(array)):
            raise ValueError("Order quantities must be integers.")
        array = array.astype(np.int64)
        if not np.all((array >= 0) & (array <= 100) & (array % 10 == 0)):
            raise ValueError("Each order quantity must be one of 0, 10, ..., 100.")
        return array // 10

    @staticmethod
    def action_indices_to_quantities(
        action: Iterable[int],
    ) -> np.ndarray:
        """Convert internal action indices to order quantities."""

        array = np.asarray(list(action))

        if array.shape != (3,):
            raise ValueError(
                "Action must contain exactly three values."
            )

        if not np.issubdtype(array.dtype, np.number):
            raise TypeError("Action indices must be numeric.")

        if not np.all(np.isfinite(array)):
            raise ValueError("Action indices must be finite.")

        if not np.all(array == np.round(array)):
            raise ValueError("Action indices must be integers.")

        array = array.astype(np.int64)

        if not np.all((array >= 0) & (array <= 10)):
            raise ValueError(
                "Action must contain three integer indices in [0, 10]."
            )

        return array * 10

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
        super().reset(seed=seed)
        options = options or {}

        self.day = 0
        self.episode_cost = 0.0
        self.arrival_pipeline = np.zeros((3, 4), dtype=np.int64)
        self.demand_history = np.zeros((7, 3), dtype=np.int64)

        self.episode_parameters = self._sample_episode_parameters(options)
        self.inventory = np.asarray(
            self.episode_parameters["initial_inventory"], dtype=np.int64
        ).copy()
        self._prepare_episode_sequences()

        observation = self._get_observation()
        info = self._reset_info(seed)
        return observation, info

    def step(
        self, action: np.ndarray | list[int] | tuple[int, int, int]
    ) -> tuple[dict[str, np.ndarray], float, bool, bool, dict[str, Any]]:
        if self.day >= self.HORIZON:
            raise RuntimeError("Episode is complete. Call reset() before step().")

        action_array = np.asarray(action, dtype=np.int64)
        if not self.action_space.contains(action_array):
            raise ValueError(
                "Environment action must contain three integer indices in [0, 10]. "
                "Use quantities_to_action_indices() when starting from actual quantities."
            )
        order_quantities = action_array * 10

        # 1. Receive orders due today, then advance the future-arrival pipeline.
        scheduled_arrivals = self.arrival_pipeline[:, 0].copy()
        self.arrival_pipeline[:, :-1] = self.arrival_pipeline[:, 1:]
        self.arrival_pipeline[:, -1] = 0

        # 2. Enforce warehouse capacity after arrivals.
        accepted_arrivals, discarded = self._accept_arrivals_with_capacity(
            scheduled_arrivals
        )
        self.inventory += accepted_arrivals

        # 3. Add today's order to its future arrival position.
        realised_delays = self._delay_flags[self.day].astype(np.int64)
        for product in range(self.NUM_PRODUCTS):
            quantity = int(order_quantities[product])
            if quantity == 0:
                continue
            lead_time = int(self.REFERENCE_LEAD_TIMES[product] + realised_delays[product])
            pipeline_index = lead_time - 1
            self.arrival_pipeline[product, pipeline_index] += quantity

        # 4-5. Generate and serve demand.
        demand = self._demand_sequence[self.day].copy()
        fulfilled = np.minimum(self.inventory, demand)
        unfulfilled = demand - fulfilled
        self.inventory -= fulfilled

        # 6. Update history and state summaries.
        self.demand_history[:-1] = self.demand_history[1:]
        self.demand_history[-1] = demand

        # 7. Calculate official costs and reward.
        holding_cost = float(
            np.dot(self.inventory, self.PRODUCT_VOLUMES)
            * self.HOLDING_COST_PER_VOLUME
        )
        stockout_cost = float(np.dot(unfulfilled, self.STOCKOUT_COSTS))
        ordering_cost = float(
            np.dot(order_quantities > 0, self.FIXED_ORDERING_COSTS)
        )
        discard_cost = float(np.dot(discarded, self.DISCARDING_COSTS))
        daily_cost = holding_cost + stockout_cost + ordering_cost + discard_cost
        reward = -daily_cost / 100.0
        self.episode_cost += daily_cost

        current_day = self.day
        self.day += 1
        terminated = False
        truncated = self.day >= self.HORIZON

        observation = self._get_observation()
        info = {
            "day": current_day,
            "demand": demand.astype(np.int32),
            "fulfilled_demand": fulfilled.astype(np.int32),
            "unfulfilled_demand": unfulfilled.astype(np.int32),
            "scheduled_arrivals": scheduled_arrivals.astype(np.int32),
            "accepted_arrivals": accepted_arrivals.astype(np.int32),
            "discarded_units": discarded.astype(np.int32),
            "order_quantities": order_quantities.astype(np.int32),
            "realised_one_day_delay": realised_delays.astype(np.int32),
            "costs": {
                "holding": holding_cost,
                "stockout": stockout_cost,
                "ordering": ordering_cost,
                "discarding": discard_cost,
                "daily_total": daily_cost,
                "episode_total": self.episode_cost,
            },
        }
        return observation, float(reward), terminated, truncated, info

    def _sample_episode_parameters(self, options: dict[str, Any]) -> dict[str, Any]:
        base_demand = np.asarray(
            self.student_config["demand_multiplier_profile"], dtype=np.float64
        )
        base_inventory = np.asarray(
            self.student_config["initial_inventory_profile"], dtype=np.int64
        )
        base_delay = np.asarray(
            self.student_config["lead_time_delay_profile"], dtype=np.float64
        )

        if self.domain_randomization:
            demand_offsets = self.np_random.choice(
                np.asarray([-0.05, 0.0, 0.05]), size=3
            )
            demand_multipliers = np.clip(
                base_demand + demand_offsets, 0.85, 1.15
            )

            inventory_offsets = self.np_random.choice(
                np.asarray([-10, 0, 10]), size=3
            )
            initial_inventory = np.clip(
                base_inventory + inventory_offsets, 80, 120
            ).astype(np.int64)

            delay_offsets = self.np_random.choice(
                np.asarray([-0.02, 0.0, 0.02]), size=3
            )
            delay_probabilities = np.clip(
                base_delay + delay_offsets, 0.0, 0.10
            )
        else:
            demand_multipliers = base_demand.copy()
            initial_inventory = base_inventory.copy()
            delay_probabilities = base_delay.copy()

        scenario_components = self._resolve_scenario_components(
            options.get("scenario_mode", self.scenario_mode)
        )

        return {
            "variant_id": self.student_config["variant_id"],
            "demand_multipliers": demand_multipliers.tolist(),
            "initial_inventory": initial_inventory.tolist(),
            "delay_probabilities": delay_probabilities.tolist(),
            "scenario_components": scenario_components,
        }

    def _resolve_scenario_components(
        self, mode: str | Iterable[str]
    ) -> list[str]:
        if isinstance(mode, str):
            normalized = mode.strip().lower()
            if normalized == "stationary":
                return []
            if normalized in self._VALID_SCENARIO_COMPONENTS:
                return [normalized]
            if normalized == "mixed":
                count = 2
                return sorted(
                    self.np_random.choice(
                        sorted(self._VALID_SCENARIO_COMPONENTS),
                        size=count,
                        replace=False,
                    ).tolist()
                )
            if normalized == "random":
                count = int(self.np_random.choice([0, 1, 2], p=[0.25, 0.50, 0.25]))
                if count == 0:
                    return []
                return sorted(
                    self.np_random.choice(
                        sorted(self._VALID_SCENARIO_COMPONENTS),
                        size=count,
                        replace=False,
                    ).tolist()
                )
            raise ValueError(
                "scenario_mode must be random, stationary, seasonal, trend, shock or mixed."
            )

        components = sorted({str(item).strip().lower() for item in mode})
        invalid = set(components).difference(self._VALID_SCENARIO_COMPONENTS)
        if invalid:
            raise ValueError(f"Unsupported scenario components: {sorted(invalid)}")
        return components

    def _prepare_episode_sequences(self) -> None:
        multipliers = np.asarray(
            self.episode_parameters["demand_multipliers"], dtype=np.float64
        )
        expected = np.tile(
            self.REFERENCE_DEMAND_MEANS * multipliers,
            (self.HORIZON, 1),
        )
        days = np.arange(self.HORIZON, dtype=np.float64)
        components = set(self.episode_parameters["scenario_components"])
        scenario_details: dict[str, Any] = {}

        if "seasonal" in components:
            amplitudes = self.np_random.uniform(0.05, 0.12, size=3)
            phases = self.np_random.uniform(0.0, 2.0 * np.pi, size=3)
            seasonal_factor = 1.0 + amplitudes[None, :] * np.sin(
                2.0 * np.pi * days[:, None] / 7.0 + phases[None, :]
            )
            expected *= seasonal_factor
            scenario_details["seasonal_amplitudes"] = amplitudes.tolist()

        if "trend" in components:
            direction = int(self.np_random.choice([-1, 1]))
            magnitude = float(self.np_random.uniform(0.10, 0.22))
            centered = np.linspace(-0.5, 0.5, self.HORIZON)
            trend_factor = 1.0 + direction * magnitude * centered
            expected *= trend_factor[:, None]
            scenario_details["trend_direction"] = "up" if direction > 0 else "down"
            scenario_details["trend_total_change"] = magnitude

        if "shock" in components:
            product = int(self.np_random.integers(0, self.NUM_PRODUCTS))
            start = int(self.np_random.integers(8, 36))
            duration = int(self.np_random.integers(3, 8))
            factor = float(self.np_random.uniform(1.20, 1.45))
            end = min(start + duration, self.HORIZON)
            expected[start:end, product] *= factor
            scenario_details["shock_product"] = product + 1
            scenario_details["shock_start_day"] = start
            scenario_details["shock_duration"] = end - start
            scenario_details["shock_factor"] = factor

        expected = np.maximum(expected, 0.01)
        self._demand_sequence = self.np_random.poisson(expected).astype(np.int64)
        delay_probabilities = np.asarray(
            self.episode_parameters["delay_probabilities"], dtype=np.float64
        )
        self._delay_flags = (
            self.np_random.random((self.HORIZON, self.NUM_PRODUCTS))
            < delay_probabilities[None, :]
        )
        self.episode_parameters["scenario_details"] = scenario_details

    def _accept_arrivals_with_capacity(
        self, arrivals: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        arrivals = np.asarray(arrivals, dtype=np.int64)
        current_volume = float(np.dot(self.inventory, self.PRODUCT_VOLUMES))
        available_volume = max(self.CAPACITY - current_volume, 0.0)
        arrival_volume = float(np.dot(arrivals, self.PRODUCT_VOLUMES))

        if arrival_volume <= available_volume + 1e-9:
            return arrivals.copy(), np.zeros(3, dtype=np.int64)
        if available_volume <= 0.0:
            return np.zeros(3, dtype=np.int64), arrivals.copy()

        fraction = available_volume / arrival_volume
        raw_acceptance = arrivals.astype(np.float64) * fraction
        accepted = np.floor(raw_acceptance).astype(np.int64)
        used_volume = float(np.dot(accepted, self.PRODUCT_VOLUMES))
        remaining_volume = max(available_volume - used_volume, 0.0)

        fractional_parts = raw_acceptance - accepted
        priority = sorted(
            range(self.NUM_PRODUCTS),
            key=lambda index: (-fractional_parts[index], index),
        )
        made_progress = True
        while made_progress:
            made_progress = False
            for product in priority:
                if accepted[product] >= arrivals[product]:
                    continue
                volume = float(self.PRODUCT_VOLUMES[product])
                if volume <= remaining_volume + 1e-9:
                    accepted[product] += 1
                    remaining_volume -= volume
                    made_progress = True

        discarded = arrivals - accepted
        return accepted, discarded

    def _get_observation(self) -> dict[str, np.ndarray]:
        utilisation = float(
            np.dot(self.inventory, self.PRODUCT_VOLUMES) / self.CAPACITY
        )
        return {
            "inventory": self.inventory.astype(np.int32).copy(),
            "arrival_pipeline": self.arrival_pipeline.astype(np.int32).copy(),
            "demand_history": self.demand_history.astype(np.int32).copy(),
            "day": np.asarray([self.day], dtype=np.int32),
            "capacity_utilisation": np.asarray([utilisation], dtype=np.float32),
        }

    def _reset_info(self, seed: int | None) -> dict[str, Any]:
        return {
            "seed": seed,
            "roll_number": self.student_config["roll_number"],
            "variant_id": self.student_config["variant_id"],
            "config_fingerprint": self.student_config.get("config_fingerprint"),
            "episode_parameters": deepcopy(self.episode_parameters),
        }
