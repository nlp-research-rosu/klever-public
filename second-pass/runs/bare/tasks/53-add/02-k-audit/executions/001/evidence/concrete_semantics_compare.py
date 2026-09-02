#!/usr/bin/env python3
import importlib.util
import json
import re
import subprocess
from pathlib import Path

SCRATCH = Path("/tmp/audit-work/53-add")
EVIDENCE = Path("/audit-output/evidence")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical_for_k", SCRATCH / "trusted-canonical.py")
generated = load_module("generated_solution_for_k", SCRATCH / "solution.py")

cases = [
    {"label": "documented-1", "x": 2, "y": 3},
    {"label": "documented-2", "x": 5, "y": 7},
    {"label": "zero-boundary", "x": 0, "y": 0},
    {"label": "negative-normal", "x": -8, "y": 3},
    {"label": "signed-cancellation", "x": -1, "y": 1},
    {"label": "beyond-64-bit", "x": 2**63 - 1, "y": 1},
    {"label": "unbounded-int", "x": 10**100, "y": -(10**100) + 7},
]
(EVIDENCE / "concrete-semantics-inputs.json").write_text(
    json.dumps(cases, indent=2) + "\n"
)

failures = []
for case in cases:
    x = case["x"]
    y = case["y"]
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "reviewer-concrete-kompiled",
        f"-cARG1={x}",
        f"-cARG2={y}",
    ]
    print("CASE:", case["label"])
    print("COMMAND:", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"KRUN_EXIT_STATUS: {completed.returncode}")
    print("KRUN_OUTPUT_BEGIN")
    print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    print("KRUN_OUTPUT_END")
    matches = re.findall(r"<result>\s*(-?\d+)\s*</result>", completed.stdout)
    k_value = int(matches[-1]) if matches else None
    canonical_value = canonical.add(x, y)
    generated_value = generated.add(x, y)
    print(
        "VALUES:",
        json.dumps(
            {
                "k": k_value,
                "canonical_python": canonical_value,
                "generated_python": generated_value,
            },
            sort_keys=True,
        ),
    )
    if (
        completed.returncode != 0
        or len(matches) != 1
        or k_value != canonical_value
        or k_value != generated_value
    ):
        failures.append(case["label"])

print(f"TOTAL_CASES: {len(cases)}")
print(f"MISMATCH_OR_EXECUTION_FAILURE_COUNT: {len(failures)}")
for label in failures:
    print(f"FAILURE: {label}")
raise SystemExit(1 if failures else 0)
