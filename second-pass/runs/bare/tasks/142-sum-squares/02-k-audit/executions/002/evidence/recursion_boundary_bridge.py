#!/usr/bin/env python3
import importlib.util
import re
import subprocess
import sys

sys.dont_write_bytecode = True


def load_function(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


canonical = load_function("boundary_canonical", "/reference/canonical.py")
generated = load_function("boundary_generated", "/candidate/solution.py")
values = list(range(1500))
args = "ListVal(" + ", ".join(str(value) for value in values) + ")"
command = [
    "krun",
    "/tmp/audit-work/candidate-src/solution.mpy",
    "--definition",
    "/tmp/audit-work/semantic-llvm-kompiled-audit",
    f"-cARGS={args}",
]
print("COMMAND: krun solution.mpy --definition semantic-llvm-kompiled-audit "
      "-cARGS='ListVal(0, 1, ..., 1499)'")
completed = subprocess.run(command, text=True, capture_output=True, timeout=120)
print(f"K_EXIT_STATUS={completed.returncode}")
match = re.search(r"VInt\s*\(\s*(-?\d+)\s*\)\s*~>\s*\.K", completed.stdout)
if completed.returncode != 0 or match is None:
    print(completed.stderr.rstrip())
    print(completed.stdout.rstrip())
    raise SystemExit(1)
k_value = int(match.group(1))
canonical_value = canonical(values.copy())
print(f"K_RESULT={k_value}")
print(f"CANONICAL_RESULT={canonical_value}")
print(f"K_MATCHES_CANONICAL={k_value == canonical_value}")
try:
    generated_value = generated(values.copy())
    print(f"GENERATED_PYTHON_RESULT={generated_value}")
    print(f"K_MATCHES_GENERATED_PYTHON={k_value == generated_value}")
except Exception as error:
    print(f"GENERATED_PYTHON_EXCEPTION={type(error).__name__}: {error}")
    print("K_MATCHES_GENERATED_PYTHON=False")
