#!/usr/bin/env python3
"""Attach an audit disposition to every record in k-inventory.json."""

from __future__ import annotations

import json
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/k-inventory.json")
OUTPUT = Path("/audit-output/evidence/K-RULE-DECISIONS.md")

CANDIDATE_DECISIONS = {
    10: ("CONCERN", "Fresh result-token syntax; value-bearing through later bridges."),
    11: (
        "REJECT",
        "Unconstrained program-derived roundedCubeRoot oracle; no connection theorem.",
    ),
    14: (
        "REJECT",
        "Operational bridge preempts fixed divII and has no context/value theorem.",
    ),
    15: (
        "REJECT",
        "Operational bridge replaces mixed float power without a connection theorem.",
    ),
    16: (
        "REJECT",
        "Operational/result bridge replaces round with the opaque oracle.",
    ),
    22: ("ACCEPT", "Guarded nonnegative-cube absolute-value identity."),
    25: ("ACCEPT", "Guarded negative-cube absolute-value identity."),
    28: ("ACCEPT", "Guarded positive-magnitude absolute-value identity."),
    32: ("ACCEPT", "Guarded negative-form absolute-value identity."),
    41: (
        "REJECT-UNSOUND",
        "False at intended-domain witness N=10^15 under actual Python/fixed concrete K.",
    ),
    48: (
        "ACCEPT",
        "No integer cube lies strictly between consecutive nonnegative cubes.",
    ),
    59: (
        "ACCEPT-LIMITED",
        "Nullary definition is total, but it does not pin the submitted module.",
    ),
    60: (
        "ACCEPT-LIMITED",
        "Faithful current body literal, but a substitution rather than a load theorem.",
    ),
}

# Records on the actual submitted-program execution/proof path. Other trusted
# records remain part of the selected fixed semantics but are not reached.
USED_TRUSTED_LINES = {
    "semantics/syntax.k": {9, 12, 15, 28, 30, 32, 41, 50, 53, 57, 60, 61},
    "semantics/core.k": {
        49,
        124,
        125,
        126,
        127,
        130,
        131,
        132,
        152,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        194,
        208,
        209,
        210,
    },
    "semantics/call.k": {19, 20, 21, 31, 32, 69},
    "semantics/functions.k": {8, 14, 63, 64, 78, 80, 85},
    "semantics/controls.k": {9},
    "semantics/operators.k": {12, 15, 16, 17},
    "semantics/int.k": {17, 26},
    "semantics/builtins.k": {17, 44, 140},
    "semantics/float.k": {
        24,
        25,
        30,
        31,
        32,
        119,
        120,
        132,
        195,
        196,
        209,
        210,
        211,
        217,
        218,
        227,
    },
}


def trusted_disposition(record: dict[str, object]) -> tuple[str, str]:
    file_path = str(record["file"])
    relative = file_path.split("/reference/reference-semantics/", 1)[-1]
    line = int(record["line"])
    if line in USED_TRUSTED_LINES.get(relative, set()):
        return (
            "ACCEPT-FIXED-USED",
            "Byte-identical supplied-semantics record on the reviewed used path.",
        )
    return (
        "ACCEPT-FIXED-UNREACHED",
        "Byte-identical supplied-semantics record not reached by submitted program/proof.",
    )


def main() -> int:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    output = [
        "# Per-record K audit dispositions",
        "",
        "This file assigns a disposition to all 941 records in K-INVENTORY.md. "
        "The supplied tree is the fixed semantics selected by "
        "SUPPLIED_SEMANTICS; proof-local records receive individual judgments.",
        "",
    ]
    counts: dict[str, int] = {}
    for record in inventory["records"]:
        if record["file"] == "/candidate/verification.k":
            disposition, reason = CANDIDATE_DECISIONS[int(record["line"])]
        else:
            disposition, reason = trusted_disposition(record)
        counts[disposition] = counts.get(disposition, 0) + 1
        output.append(
            f"- `{record['file']}:{record['line']}` `{record['kind']}` "
            f"**{disposition}** — {reason}"
        )
    output.extend(["", "Disposition counts:", ""])
    for disposition, count in sorted(counts.items()):
        output.append(f"- `{disposition}`: {count}")
    OUTPUT.write_text("\n".join(output) + "\n", encoding="utf-8")
    print(f"RECORDS={len(inventory['records'])}")
    print(f"OUTPUT={OUTPUT}")
    print("COUNTS=" + json.dumps(counts, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
