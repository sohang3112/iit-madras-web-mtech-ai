"""Local validation checks for an inventory-project policy submission.

Usage
-----
python policy_validation_tests_updated.py submission_template.py
python policy_validation_tests_updated.py my_policy.py --max-seconds-per-call 0.25

What this script checks
-----------------------
1. The submitted file is a Python (.py) file and can be imported.
2. It defines exactly one required policy function: run_policy(observation).
3. The function accepts the documented observation dictionary.
4. It returns exactly three integer order quantities.
5. Each quantity is one of 0, 10, 20, ..., 100.
6. It does not modify the observation supplied by the evaluator.
7. It behaves deterministically when reloaded and given the same observation sequence.
8. It does not directly call env.step() or env.reset().
9. Its average inference time is below the configured local limit.

Important
---------
- This script validates only the submission interface.
- Passing these checks does not guarantee leaderboard eligibility or good performance.
- The actual leaderboard evaluator may apply additional security, packaging and runtime checks.
- If the policy requires a trained model file, place that file in the location and format
  specified separately by the course team.
"""
from __future__ import annotations

import argparse
import ast
from copy import deepcopy
import importlib.util
import inspect
from pathlib import Path
import sys
import time
from types import ModuleType
from typing import Any
import uuid

import numpy as np

VALID_QUANTITIES = set(range(0, 101, 10))


def representative_observations() -> list[dict[str, np.ndarray]]:
    """Return representative observations matching the documented interface."""
    return [
        {
            "inventory": np.asarray([100, 100, 100], dtype=np.int32),
            "arrival_pipeline": np.zeros((3, 4), dtype=np.int32),
            "demand_history": np.zeros((7, 3), dtype=np.int32),
            "day": np.asarray([0], dtype=np.int32),
            "capacity_utilisation": np.asarray([0.65], dtype=np.float32),
        },
        {
            "inventory": np.asarray([20, 35, 15], dtype=np.int32),
            "arrival_pipeline": np.asarray(
                [[0, 20, 40, 0], [10, 0, 30, 0], [40, 20, 0, 0]],
                dtype=np.int32,
            ),
            "demand_history": np.asarray(
                [
                    [28, 23, 36],
                    [35, 24, 31],
                    [31, 27, 42],
                    [29, 21, 37],
                    [34, 28, 39],
                    [33, 26, 35],
                    [38, 29, 44],
                ],
                dtype=np.int32,
            ),
            "day": np.asarray([18], dtype=np.int32),
            "capacity_utilisation": np.asarray([0.1675], dtype=np.float32),
        },
        {
            "inventory": np.asarray([180, 150, 120], dtype=np.int32),
            "arrival_pipeline": np.asarray(
                [[60, 20, 0, 0], [50, 0, 0, 0], [80, 0, 0, 0]],
                dtype=np.int32,
            ),
            "demand_history": np.asarray(
                [
                    [30, 25, 34],
                    [29, 24, 37],
                    [31, 26, 33],
                    [30, 25, 36],
                    [28, 27, 35],
                    [33, 24, 32],
                    [30, 25, 35],
                ],
                dtype=np.int32,
            ),
            "day": np.asarray([34], dtype=np.int32),
            "capacity_utilisation": np.asarray([0.99], dtype=np.float32),
        },
        {
            "inventory": np.asarray([0, 5, 0], dtype=np.int32),
            "arrival_pipeline": np.asarray(
                [[0, 0, 60, 0], [0, 40, 0, 0], [20, 0, 0, 0]],
                dtype=np.int32,
            ),
            "demand_history": np.asarray(
                [
                    [42, 32, 48],
                    [39, 31, 50],
                    [45, 34, 55],
                    [47, 36, 53],
                    [41, 33, 51],
                    [44, 35, 56],
                    [48, 37, 58],
                ],
                dtype=np.int32,
            ),
            "day": np.asarray([47], dtype=np.int32),
            "capacity_utilisation": np.asarray([0.015], dtype=np.float32),
        },
    ]


def load_policy_module(path: Path) -> ModuleType:
    """Import a policy file under a unique module name."""
    module_name = f"student_policy_{uuid.uuid4().hex}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to create an import specification for {path}.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def normalize_action(action: Any) -> tuple[int, int, int]:
    """Validate and normalize the returned action."""
    if isinstance(action, np.ndarray):
        action = action.tolist()
    if not isinstance(action, (list, tuple)):
        raise TypeError("run_policy() must return a list, tuple or NumPy array.")
    if len(action) != 3:
        raise ValueError("run_policy() must return exactly three order quantities.")

    normalized: list[int] = []
    for index, value in enumerate(action, start=1):
        if isinstance(value, (bool, np.bool_)):
            raise TypeError(f"Product {index} action must be an integer, not bool.")
        if not isinstance(value, (int, np.integer)):
            raise TypeError(f"Product {index} action must be an integer.")
        integer = int(value)
        if integer not in VALID_QUANTITIES:
            raise ValueError(
                f"Product {index} action {integer} is invalid; use 0, 10, ..., 100."
            )
        normalized.append(integer)
    return tuple(normalized)


def observations_equal(
    left: dict[str, np.ndarray], right: dict[str, np.ndarray]
) -> bool:
    return left.keys() == right.keys() and all(
        np.array_equal(left[key], right[key]) for key in left
    )


def find_forbidden_env_calls(path: Path) -> list[str]:
    """Detect direct calls to env.step() or env.reset() in executable code."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    findings: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr not in {"step", "reset"}:
            continue
        base = node.func.value
        if isinstance(base, ast.Name) and base.id == "env":
            findings.append(f"line {getattr(node, 'lineno', '?')}: env.{node.func.attr}()")
    return findings


def validate_signature(run_policy: Any) -> None:
    """Require the exact student-facing interface run_policy(observation)."""
    if not callable(run_policy):
        raise TypeError(
            "The policy file must define a callable function named "
            "run_policy(observation)."
        )

    signature = inspect.signature(run_policy)
    parameters = list(signature.parameters.values())

    if len(parameters) != 1:
        raise TypeError(
            "run_policy() must accept exactly one argument named observation."
        )

    parameter = parameters[0]
    if parameter.name != "observation":
        raise TypeError(
            "The argument of run_policy() must be named observation."
        )

    if parameter.kind not in (
        inspect.Parameter.POSITIONAL_ONLY,
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
    ):
        raise TypeError(
            "run_policy(observation) must use a normal positional argument."
        )

    if parameter.default is not inspect.Parameter.empty:
        raise TypeError(
            "The observation argument must not have a default value."
        )


def run_validation(path: Path, max_seconds_per_call: float) -> list[str]:
    failures: list[str] = []

    try:
        forbidden = find_forbidden_env_calls(path)
        if forbidden:
            failures.append(
                "Direct environment calls are not permitted: " + ", ".join(forbidden)
            )
    except Exception as exc:  # syntax errors are also reported during import
        failures.append(f"Unable to inspect source code: {exc}")

    try:
        import_started = time.perf_counter()
        module = load_policy_module(path)
        import_seconds = time.perf_counter() - import_started
    except Exception as exc:
        failures.append(f"Policy file could not be imported: {type(exc).__name__}: {exc}")
        return failures

    try:
        run_policy = getattr(module, "run_policy")
        validate_signature(run_policy)
    except Exception as exc:
        failures.append(str(exc))
        return failures

    observations = representative_observations()

    # Interface, output and input-mutation checks.
    for index, observation in enumerate(observations, start=1):
        before = deepcopy(observation)
        try:
            action = normalize_action(run_policy(observation))
            _ = action
        except Exception as exc:
            failures.append(
                f"Representative observation {index} failed: {type(exc).__name__}: {exc}"
            )
            continue
        if not observations_equal(before, observation):
            failures.append(
                f"Representative observation {index}: run_policy() modified its input."
            )

    # Determinism is checked across fresh module loads. This permits a policy to
    # maintain deterministic internal state across calls, while ensuring that a
    # fresh policy load given the same observation sequence produces the same actions.
    try:
        sequences: list[list[tuple[int, int, int]]] = []
        for _ in range(3):
            fresh_module = load_policy_module(path)
            fresh_policy = getattr(fresh_module, "run_policy")
            sequence = [
                normalize_action(fresh_policy(deepcopy(observation)))
                for observation in observations
            ]
            sequences.append(sequence)
        if not all(sequence == sequences[0] for sequence in sequences[1:]):
            failures.append(
                "Determinism check failed: fresh policy loads produced different actions "
                "for the same observation sequence. Do not use uncontrolled randomness "
                "during evaluation."
            )
    except Exception as exc:
        failures.append(f"Determinism check failed with an error: {exc}")

    # Basic inference-time check. Import/model-loading time is reported separately.
    try:
        timing_module = load_policy_module(path)
        timing_policy = getattr(timing_module, "run_policy")
        repetitions = 100
        started = time.perf_counter()
        for iteration in range(repetitions):
            observation = deepcopy(observations[iteration % len(observations)])
            normalize_action(timing_policy(observation))
        elapsed = time.perf_counter() - started
        seconds_per_call = elapsed / repetitions
        if seconds_per_call > max_seconds_per_call:
            failures.append(
                f"Average inference time {seconds_per_call:.4f}s exceeds the local "
                f"limit of {max_seconds_per_call:.4f}s per call."
            )
    except Exception as exc:
        failures.append(f"Runtime check failed: {type(exc).__name__}: {exc}")
        seconds_per_call = float("nan")

    print(f"Policy file: {path}")
    print(f"Import/model-loading time: {import_seconds:.4f}s")
    if np.isfinite(seconds_per_call):
        print(f"Average inference time: {seconds_per_call:.6f}s per call")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a local inventory-project submission file that defines "
            "run_policy(observation)."
        )
    )
    parser.add_argument("policy_file", type=Path, help="Path to the policy .py file")
    parser.add_argument(
        "--max-seconds-per-call",
        type=float,
        default=0.25,
        help=(
            "Maximum allowed average inference time per call during this local "
            "check (default: 0.25 seconds)"
        ),
    )
    args = parser.parse_args()

    path = args.policy_file.resolve()
    if not path.is_file():
        print(f"FAIL: Policy file not found: {path}")
        return 1
    if path.suffix.lower() != ".py":
        print("FAIL: Policy submission must be a Python (.py) file.")
        return 1
    if args.max_seconds_per_call <= 0:
        print("FAIL: --max-seconds-per-call must be positive.")
        return 1

    failures = run_validation(path, args.max_seconds_per_call)
    if failures:
        print("\nVALIDATION FAILED")
        for number, failure in enumerate(failures, start=1):
            print(f"  {number}. {failure}")
        return 1

    print("\nVALIDATION PASSED")
    print(
        "The policy satisfies the local interface checks. Passing this script does "
        "not guarantee leaderboard eligibility, security compliance or performance."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
