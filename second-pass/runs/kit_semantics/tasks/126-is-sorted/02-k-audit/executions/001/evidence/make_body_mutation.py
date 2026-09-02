#!/usr/bin/env python3
"""Create a body-sensitivity mutation that still executes the claimed closure."""

from __future__ import annotations

from pathlib import Path


SOURCE = Path("/tmp/audit-work/126-is-sorted/spec.k")
TARGET = Path("/tmp/audit-work/126-is-sorted/spec-body-mutation.k")


def main() -> int:
    text = SOURCE.read_text()
    text = text.replace("module SPEC\n", "module SPEC-BODY-MUTATION\n", 1)
    text = text.replace("endmodule\n", "endmodule\n", 1)
    old = 'Return(Name("result"))'
    new = "Return(Bool(false))"
    occurrences = text.count(old)
    if occurrences != 2:
        raise RuntimeError(
            f"expected two closure-body returns, found {occurrences}"
        )
    text = text.replace(old, new)
    TARGET.write_text(text)
    print(f"source={SOURCE}")
    print(f"target={TARGET}")
    print(f"changed_return_occurrences={occurrences}")
    print("mutation=Return(Name(\"result\")) -> Return(Bool(false))")
    print(
        "both initial and target closure bindings changed, so scope "
        "preservation is not the reason the claim must fail"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
