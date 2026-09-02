#!/usr/bin/env python3
"""Ground witness for the false leading-999 postcondition mutation."""

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_third


canonical = load(Path("/reference/canonical.py"), "canonical_for_vacuity")
submitted = load(
    Path("/tmp/audit-work/33-sort-third/solution.py"), "submitted_for_vacuity"
)
input_value: list[int] = []
actual_canonical = canonical(input_value)
actual_submitted = submitted(input_value)
mutated_required = [999] + actual_submitted
print(f"input={input_value!r}")
print(f"canonical={actual_canonical!r}")
print(f"submitted={actual_submitted!r}")
print(f"mutated_required={mutated_required!r}")
assert actual_canonical == actual_submitted == []
assert actual_submitted != mutated_required
print("witness_satisfies_precondition=true mutation_is_false=true")
