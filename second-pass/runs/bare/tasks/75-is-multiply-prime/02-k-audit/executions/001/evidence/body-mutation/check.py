#!/usr/bin/env python3
"""Pin the body mutation and show its concrete false-result witnesses."""

import importlib.util
from pathlib import Path

base = Path("/audit-output/evidence/body-mutation")
mpy = (base / "solution.mpy").read_text(encoding="utf-8")
wrapper = (base / "solution-program.k").read_text(encoding="utf-8")
marker = "rule solutionProgram =>"
embedded_start = wrapper.index(marker) + len(marker)
embedded_end = wrapper.index("\nendmodule", embedded_start)
embedded = wrapper[embedded_start:embedded_end]
normalize = lambda value: "".join(value.split())


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_multiply_prime


mutated = load_entry("mutated_solution", base / "solution.py")
canonical = load_entry("mutation_canonical", Path("/reference/canonical.py"))

pin_ok = normalize(mpy) == normalize(embedded)
witnesses = [
    (30, mutated(30), canonical(30)),
    (31, mutated(31), canonical(31)),
]
print("mutation=replace equality arm 30 with 31")
print("generated_mpy_matches_embedded_term=", pin_ok)
for value, mutated_result, canonical_result in witnesses:
    print(
        f"A={value} mutated={mutated_result} canonical={canonical_result} "
        f"diverges={mutated_result != canonical_result}"
    )

if not pin_ok or not all(mutated_result != canonical_result for _, mutated_result, canonical_result in witnesses):
    raise SystemExit(1)
