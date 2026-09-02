#!/usr/bin/env python3
"""Create a fresh, concrete false-result mutation of the full entry claim."""

from __future__ import annotations

import pathlib


WORK = pathlib.Path("/tmp/audit-work/reconstruction")
source = (WORK / "stage4-ground.k").read_text()
first_module_end = source.index("endmodule") + len("endmodule")
mutation = source[:first_module_end]
mutation = mutation.replace(
    "module STAGE4-GROUND-PROGRAM",
    "module STAGE6-FALSE-RESULT",
    1,
)
mutation = mutation.replace(
    "claim [example-one-program]:",
    "claim [example-one-wrong-thirteen]:",
    1,
)
old = "      => 12\n    </k>"
new = "      => 13\n    </k>"
if mutation.count(old) != 1:
    raise RuntimeError("expected exactly one full-program result occurrence")
mutation = mutation.replace(old, new, 1)
output = WORK / "stage6-false-result.k"
output.write_text(mutation + "\n")
print("mutation", output)
print("satisfying_input", [5, 8, 7, 1])
print("true_result", 12)
print("mutated_result", 13)
