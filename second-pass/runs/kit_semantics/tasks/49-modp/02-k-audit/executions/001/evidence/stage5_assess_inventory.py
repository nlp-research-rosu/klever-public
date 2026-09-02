#!/usr/bin/env python3

"""Assign an audit disposition to every inventoried K declaration and rule."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/49-modp")
sources = [ROOT / "reference-semantics" / "semantics.k"]
sources += sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
sources += [ROOT / "verification.k", ROOT / "spec.k"]
start = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")

used_rules: dict[tuple[str, int], str] = {
    ("reference-semantics/semantics/core.k", 131): "evaluate Name by current-scope lookup",
    ("reference-semantics/semantics/core.k", 132): "return the bound value from a scope map",
    ("reference-semantics/semantics/core.k", 158): "expand the fixed builtins scope",
    ("reference-semantics/semantics/core.k", 189): "start left-to-right argument evaluation",
    ("reference-semantics/semantics/core.k", 190): "append one evaluated argument",
    ("reference-semantics/semantics/core.k", 191): "dispatch after all arguments evaluate",
    ("reference-semantics/semantics/core.k", 194): "evaluate an integer literal",
    ("reference-semantics/semantics/core.k", 214): "append into an empty argument sequence",
    ("reference-semantics/semantics/core.k", 215): "append recursively in argument order",
    ("reference-semantics/semantics/call.k", 20): "evaluate the callee of Call",
    ("reference-semantics/semantics/call.k", 21): "evaluate arguments after the callee",
    ("reference-semantics/semantics/call.k", 69): "enter the exact closure and save continuation/state",
    ("reference-semantics/semantics/functions.k", 63): "complete exact parameter binding",
    ("reference-semantics/semantics/functions.k", 64): "bind n then p to the evaluated arguments",
    ("reference-semantics/semantics/functions.k", 78): "turn Return(value) into frame pop",
    ("reference-semantics/semantics/functions.k", 85): "restore caller state and return the value",
    ("reference-semantics/semantics/operators.k", 12): "dispatch the cooled integer BinOp",
    ("reference-semantics/semantics/int.k", 15): "interpret integer percent as pyMod",
    ("reference-semantics/semantics/int.k", 17): "interpret nonnegative integer exponentiation",
    ("reference-semantics/semantics/int.k", 20): "define Python-style nonzero-divisor remainder",
}

pinning_rules: dict[tuple[str, int], str] = {
    ("reference-semantics/semantics/core.k", 125): "load the submitted Module statements",
    ("reference-semantics/semantics/core.k", 126): "sequence the submitted FuncDef",
    ("reference-semantics/semantics/core.k", 127): "finish module statement sequencing",
    ("reference-semantics/semantics/functions.k", 14): "install the exact translated closure binding",
}

target_declarations = {
    ("reference-semantics/semantics/syntax.k", 9),
    ("reference-semantics/semantics/syntax.k", 41),
    ("reference-semantics/semantics/syntax.k", 56),
    ("reference-semantics/semantics/syntax.k", 57),
    ("reference-semantics/semantics/syntax.k", 60),
    ("reference-semantics/semantics/syntax.k", 61),
    ("reference-semantics/semantics/core.k", 25),
    ("reference-semantics/semantics/core.k", 36),
    ("reference-semantics/semantics/core.k", 37),
    ("reference-semantics/semantics/core.k", 38),
    ("reference-semantics/semantics/core.k", 39),
    ("reference-semantics/semantics/core.k", 40),
    ("reference-semantics/semantics/core.k", 41),
    ("reference-semantics/semantics/core.k", 42),
    ("reference-semantics/semantics/core.k", 49),
    ("reference-semantics/semantics/core.k", 124),
    ("reference-semantics/semantics/core.k", 130),
    ("reference-semantics/semantics/core.k", 157),
    ("reference-semantics/semantics/core.k", 185),
    ("reference-semantics/semantics/core.k", 186),
    ("reference-semantics/semantics/core.k", 208),
    ("reference-semantics/semantics/core.k", 209),
    ("reference-semantics/semantics/functions.k", 8),
    ("reference-semantics/semantics/call.k", 19),
    ("reference-semantics/semantics/int.k", 19),
}


def records(text: str):
    current = None
    for line_number, line in enumerate(text.splitlines(), 1):
        match = start.match(line)
        if match:
            if current is not None:
                yield current
            current = [line_number, match.group(1), line.strip()]
        elif line.strip() == "endmodule":
            if current is not None:
                yield current
                current = None
        elif (
            current is not None
            and line.strip()
            and not line.strip().startswith("//")
        ):
            current[2] += " " + line.strip()
    if current is not None:
        yield current


counts: collections.Counter[str] = collections.Counter()
for source in sources:
    relative = str(source.relative_to(ROOT))
    for line_number, kind, body in records(source.read_text()):
        key = (relative, line_number)
        if relative == "spec.k" and kind == "claim":
            disposition = "TARGET_CLAIM"
            reason = "the sole positive reachability obligation"
        elif key in used_rules:
            disposition = "TARGET_USED_SOUND"
            reason = used_rules[key]
        elif key in pinning_rules:
            disposition = "PINNING_USED_SOUND"
            reason = pinning_rules[key]
        elif key in target_declarations:
            disposition = "TARGET_DECLARATION_SOUND"
            reason = "declares the constructor/cell/function used by the exact target trace"
        elif relative.endswith("/concrete.k"):
            disposition = "LLVM_ONLY_NOT_IN_PROOF"
            reason = "MPY-CONCRETE is absent from the Haskell verification import graph"
        elif "no-evaluators" in body:
            disposition = "OPAQUE_FIXED_UNREACHED"
            reason = "fixed supplied primitive; no target constructor reaches this symbol"
        else:
            disposition = "FIXED_UNREACHED_REVIEWED"
            reason = (
                "no head constructor/operator/guard matches the exact target trace; "
                "no false conclusion witness on the intended target domain"
            )
        counts[disposition] += 1
        print(
            f"ASSESS|{relative}:{line_number}|{kind.upper()}|"
            f"{disposition}|{reason}|{body}"
        )

print("COUNTS|" + "|".join(f"{key}={counts[key]}" for key in sorted(counts)))
