"""Official environment package for the IITM RL inventory-control project."""
from .config import (
    PROJECT_VERSION,
    generate_student_config,
    normalize_roll_number,
    public_config_summary,
    validate_student_config,
)
from .environment import IndustrialInventoryEnv


def make_env(
    roll_number: str,
    *,
    scenario_mode: str = "random",
    domain_randomization: bool = True,
) -> IndustrialInventoryEnv:
    """Convenience constructor using a roll number."""
    config = generate_student_config(roll_number)
    return IndustrialInventoryEnv(
        config,
        scenario_mode=scenario_mode,
        domain_randomization=domain_randomization,
    )


__all__ = [
    "IndustrialInventoryEnv",
    "PROJECT_VERSION",
    "generate_student_config",
    "make_env",
    "normalize_roll_number",
    "public_config_summary",
    "validate_student_config",
]
