"""Deterministic student-variant generation for the 2026 inventory project.

The generator is intentionally deterministic: the same normalized roll number and
project version always map to the same variant.  The catalogue uses balanced
profiles so that aggregate demand, starting inventory and delay exposure remain
similar across variants while product-level values differ.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import re
from typing import Any

PROJECT_VERSION = "IITM-6002W-RL-Inventory-2026-v1"

# All profiles remain within the ranges declared in the problem statement.
_DEMAND_PROFILES = [
    [0.90, 1.00, 1.10],
    [0.90, 1.10, 1.00],
    [1.00, 0.90, 1.10],
    [1.00, 1.10, 0.90],
    [1.10, 0.90, 1.00],
    [1.10, 1.00, 0.90],
    [0.95, 1.00, 1.05],
    [0.95, 1.05, 1.00],
    [1.00, 0.95, 1.05],
    [1.00, 1.05, 0.95],
    [1.05, 0.95, 1.00],
    [1.05, 1.00, 0.95],
    [0.85, 1.00, 1.15],
    [0.85, 1.15, 1.00],
    [1.00, 0.85, 1.15],
    [1.00, 1.15, 0.85],
    [1.15, 0.85, 1.00],
    [1.15, 1.00, 0.85],
]

_INITIAL_INVENTORY_PROFILES = [
    [80, 100, 120],
    [80, 120, 100],
    [100, 80, 120],
    [100, 120, 80],
    [120, 80, 100],
    [120, 100, 80],
    [90, 100, 110],
    [90, 110, 100],
    [100, 90, 110],
    [100, 110, 90],
    [110, 90, 100],
    [110, 100, 90],
]

_DELAY_PROFILES = [
    [0.00, 0.05, 0.10],
    [0.00, 0.10, 0.05],
    [0.05, 0.00, 0.10],
    [0.05, 0.10, 0.00],
    [0.10, 0.00, 0.05],
    [0.10, 0.05, 0.00],
    [0.02, 0.05, 0.08],
    [0.02, 0.08, 0.05],
    [0.05, 0.02, 0.08],
    [0.05, 0.08, 0.02],
    [0.08, 0.02, 0.05],
    [0.08, 0.05, 0.02],
]


def _build_variant_catalogue() -> list[dict[str, Any]]:
    """Create a fixed catalogue of balanced variants.

    The catalogue is generated from constant lists, not from runtime randomness,
    so its contents are stable across machines and Python versions.
    """
    catalogue: list[dict[str, Any]] = []
    count = 36
    for index in range(count):
        demand = _DEMAND_PROFILES[index % len(_DEMAND_PROFILES)]
        inventory = _INITIAL_INVENTORY_PROFILES[(index * 5 + 2) % len(_INITIAL_INVENTORY_PROFILES)]
        delay = _DELAY_PROFILES[(index * 7 + 1) % len(_DELAY_PROFILES)]
        catalogue.append(
            {
                "variant_id": f"V{index + 1:03d}",
                "demand_multiplier_profile": list(demand),
                "initial_inventory_profile": list(inventory),
                "lead_time_delay_profile": list(delay),
            }
        )
    return catalogue


VARIANT_CATALOGUE = _build_variant_catalogue()


def normalize_roll_number(roll_number: str) -> str:
    """Normalize and validate a student roll number."""
    if not isinstance(roll_number, str):
        raise TypeError("roll_number must be a string")

    normalized = re.sub(r"\s+", "", roll_number).upper()
    if not normalized or normalized == "ENTER_YOUR_ROLL_NUMBER":
        raise ValueError("Enter your official roll number before generating the configuration.")
    if not re.fullmatch(r"[A-Z0-9_\-/]{4,40}", normalized):
        raise ValueError(
            "Roll number may contain only letters, digits, underscore, hyphen or slash."
        )
    return normalized


def _fingerprint(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def generate_student_config(roll_number: str) -> dict[str, Any]:
    """Generate the official deterministic configuration for a roll number.

    Parameters
    ----------
    roll_number:
        Official student roll number.

    Returns
    -------
    dict
        A JSON-serialisable configuration dictionary.
    """
    normalized = normalize_roll_number(roll_number)
    digest = hashlib.sha256(
        f"{PROJECT_VERSION}:{normalized}".encode("utf-8")
    ).digest()
    variant_index = int.from_bytes(digest[:8], byteorder="big") % len(VARIANT_CATALOGUE)
    variant = deepcopy(VARIANT_CATALOGUE[variant_index])

    config: dict[str, Any] = {
        "project_version": PROJECT_VERSION,
        "roll_number": normalized,
        **variant,
        "declared_ranges": {
            "demand_multiplier": [0.85, 1.15],
            "initial_inventory": [80, 120],
            "lead_time_delay_probability": [0.00, 0.10],
        },
    }
    config["config_fingerprint"] = _fingerprint(config)
    validate_student_config(config)
    return config


def validate_student_config(config: dict[str, Any]) -> None:
    """Validate structure and declared parameter limits."""
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")

    required = {
        "project_version",
        "roll_number",
        "variant_id",
        "demand_multiplier_profile",
        "initial_inventory_profile",
        "lead_time_delay_profile",
    }
    missing = required.difference(config)
    if missing:
        raise ValueError(f"Configuration is missing fields: {sorted(missing)}")

    if config["project_version"] != PROJECT_VERSION:
        raise ValueError(
            f"Configuration project version must be {PROJECT_VERSION!r}."
        )

    normalize_roll_number(config["roll_number"])

    demand = config["demand_multiplier_profile"]
    inventory = config["initial_inventory_profile"]
    delays = config["lead_time_delay_profile"]

    if len(demand) != 3 or not all(0.85 <= float(value) <= 1.15 for value in demand):
        raise ValueError("Demand multiplier profile must contain three values in [0.85, 1.15].")
    if len(inventory) != 3 or not all(
        80 <= int(value) <= 120 and int(value) % 10 == 0 for value in inventory
    ):
        raise ValueError(
            "Initial inventory profile must contain three multiples of 10 in [80, 120]."
        )
    if len(delays) != 3 or not all(0.0 <= float(value) <= 0.10 for value in delays):
        raise ValueError("Delay profile must contain three probabilities in [0.00, 0.10].")


def public_config_summary(config: dict[str, Any]) -> dict[str, Any]:
    """Return the fields students should record in their notebook/report."""
    validate_student_config(config)
    keys = [
        "project_version",
        "roll_number",
        "variant_id",
        "config_fingerprint",
        "demand_multiplier_profile",
        "initial_inventory_profile",
        "lead_time_delay_profile",
    ]
    return {key: deepcopy(config[key]) for key in keys}
