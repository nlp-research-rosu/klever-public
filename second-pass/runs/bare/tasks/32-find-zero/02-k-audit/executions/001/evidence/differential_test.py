#!/usr/bin/env python3
"""Independent differential check of trusted canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
import json
import math
import random
import signal
import sys
from pathlib import Path

CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/32-find-zero-audit/solution.py")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def polynomial(coefficients: list[float], x: float) -> float:
    return sum(coefficient * math.pow(x, exponent)
               for exponent, coefficient in enumerate(coefficients))


def evaluate(function, coefficients):
    def timeout_handler(_signal_number, _frame):
        raise TimeoutError("per-call 1-second limit")

    previous_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.setitimer(signal.ITIMER_REAL, 1.0)
    try:
        return {"kind": "value", "value": function(list(coefficients))}
    except TimeoutError as error:
        return {"kind": "timeout", "text": str(error)}
    except Exception as error:  # The comparison deliberately records outside-domain behavior.
        return {"kind": "exception", "type": type(error).__name__, "text": str(error)}
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        signal.signal(signal.SIGALRM, previous_handler)


def main() -> int:
    canonical = load_module("trusted_canonical", CANONICAL_PATH)
    candidate = load_module("candidate_solution", CANDIDATE_PATH)

    cases: list[dict[str, object]] = [
        {"label": "prompt-linear", "coefficients": [1, 2], "domain": True},
        {"label": "prompt-cubic", "coefficients": [-6, 11, -6, 1], "domain": True},
        {"label": "empty-list", "coefficients": [], "domain": False},
        {"label": "all-zero-boundary", "coefficients": [0, 0], "domain": False},
        {"label": "zero-leading-boundary", "coefficients": [1, 0], "domain": False},
        {"label": "initial-midpoint-root", "coefficients": [0, 1], "domain": True},
        {"label": "left-endpoint-root", "coefficients": [1, 1], "domain": True},
        {"label": "right-endpoint-root", "coefficients": [-1, 1], "domain": True},
        {"label": "bracket-expands-positive", "coefficients": [-8, 0, 0, 1], "domain": True},
        {"label": "bracket-expands-negative", "coefficients": [8, 0, 0, 1], "domain": True},
        {"label": "bisection-left-update", "coefficients": [-1, 4], "domain": True},
        {"label": "bisection-right-update", "coefficients": [1, 4], "domain": True},
        {"label": "small-coefficients", "coefficients": [1e-9, 1], "domain": True},
        {"label": "fractional-coefficients", "coefficients": [0.75, -0.5], "domain": True},
    ]

    rng = random.Random(320032)
    for index in range(60):
        length = rng.choice((2, 4, 6))
        coefficients = [rng.randint(-5, 5) for _ in range(length)]
        while coefficients[-1] == 0:
            coefficients[-1] = rng.randint(-5, 5)
        cases.append({
            "label": f"generated-{index:02d}",
            "coefficients": coefficients,
            "domain": True,
        })

    mismatches: list[dict[str, object]] = []
    results: list[dict[str, object]] = []
    for case in cases:
        coefficients = case["coefficients"]
        canonical_result = evaluate(canonical.find_zero, coefficients)
        candidate_result = evaluate(candidate.find_zero, coefficients)
        record = dict(case)
        record["canonical"] = canonical_result
        record["candidate"] = candidate_result

        mismatch_reason = None
        if (canonical_result["kind"] == "value"
                and candidate_result["kind"] == "value"):
            canonical_value = canonical_result["value"]
            candidate_value = candidate_result["value"]
            record["absolute_difference"] = abs(candidate_value - canonical_value)
            record["canonical_residual"] = polynomial(coefficients, canonical_value)
            record["candidate_residual"] = polynomial(coefficients, candidate_value)
            if bool(case["domain"]):
                if not (math.isfinite(canonical_value) and math.isfinite(candidate_value)):
                    mismatch_reason = "non-finite intended-domain result"
                elif abs(candidate_value - canonical_value) > 1e-8:
                    mismatch_reason = "material result divergence (> 1e-8)"
        elif bool(case["domain"]):
            if canonical_result["kind"] != candidate_result["kind"]:
                mismatch_reason = "different result kinds"
            elif canonical_result["kind"] == "exception":
                if canonical_result["type"] != candidate_result["type"]:
                    mismatch_reason = "different exception types"
            elif canonical_result["kind"] == "timeout":
                mismatch_reason = "both intended-domain executions timed out"
        elif canonical_result != candidate_result:
            record["outside_domain_difference"] = True

        if mismatch_reason is not None:
            record["mismatch_reason"] = mismatch_reason
            mismatches.append(record)
        results.append(record)

    print(json.dumps({
        "oracle": str(CANONICAL_PATH),
        "candidate": str(CANDIDATE_PATH),
        "seed": 320032,
        "case_count": len(cases),
        "intended_domain": (
            "nonempty even-length numeric coefficient lists with a nonzero "
            "highest-degree (last) coefficient"
        ),
        "comparison_threshold": 1e-8,
        "prompt_rounding": {
            "canonical_linear": round(canonical.find_zero([1, 2]), 2),
            "candidate_linear": round(candidate.find_zero([1, 2]), 2),
            "canonical_cubic": round(canonical.find_zero([-6, 11, -6, 1]), 2),
            "candidate_cubic": round(candidate.find_zero([-6, 11, -6, 1]), 2),
        },
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "results": results,
    }, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
