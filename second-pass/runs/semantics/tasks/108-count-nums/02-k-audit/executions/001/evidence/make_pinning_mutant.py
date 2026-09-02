#!/usr/bin/env python3
"""Create a body-sensitivity mutant of the submitted program in scratch."""

from pathlib import Path

source_path = Path("/tmp/audit-work/audit-108/source/solution.py")
mutant_dir = Path("/tmp/audit-work/audit-108/pinning-mutant")
mutant_path = mutant_dir / "solution.py"
harness_path = mutant_dir / "pinning_mutant_harness.py"

source = source_path.read_text(encoding="utf-8")
needle = "            count += 1"
replacement = "            count += 2"
if source.count(needle) != 1:
    raise RuntimeError(f"expected exactly one mutation site, found {source.count(needle)}")

mutant = source.replace(needle, replacement)
mutant_path.write_text(mutant, encoding="utf-8")
harness_path.write_text(
    mutant + "\n\nassert count_nums([1]) == 2\n", encoding="utf-8"
)

print(f"source={source_path}")
print(f"mutant={mutant_path}")
print("mutation=count increment changed from 1 to 2")
print(f"harness={harness_path}")
