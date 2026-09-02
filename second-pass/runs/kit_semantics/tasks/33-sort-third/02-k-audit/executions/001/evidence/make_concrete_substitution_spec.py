#!/usr/bin/env python3
"""Ground the symbolic target at a prompt example and demand its explicit result."""

from __future__ import annotations

import pathlib
import re


SCRATCH = pathlib.Path("/tmp/audit-work/33-sort-third")
source = (SCRATCH / "spec.k").read_text(encoding="utf-8")
marker = "  claim [sort-third]:"
prefix, target = source.split(marker, 1)
ground = (
    "vCons(5, vCons(6, vCons(3, vCons(4, vCons(8, "
    "vCons(9, vCons(2, .ValSeq)))))))"
)
expected = (
    "vCons(2, vCons(6, vCons(3, vCons(4, vCons(8, "
    "vCons(9, vCons(5, .ValSeq)))))))"
)
prefix = prefix.replace("module SPEC", "module SPEC-CONCRETE", 1)
target = re.sub(r"\bVS\b", ground, target)
target = target.replace(
    f"2 |-> list(sortThirdResult({ground}))",
    f"2 |-> list({expected})",
    1,
)
target = target.replace("endmodule", "endmodule", 1)
grounded = prefix + "  claim [sort-third-concrete]:" + target
(SCRATCH / "spec-concrete-substitution.k").write_text(
    grounded, encoding="utf-8"
)
print(f"input={ground}")
print(f"expected={expected}")
print(f"output={SCRATCH / 'spec-concrete-substitution.k'}")
print(
    "explicit_result_replacement="
    + str(f"2 |-> list({expected})" in grounded)
)
