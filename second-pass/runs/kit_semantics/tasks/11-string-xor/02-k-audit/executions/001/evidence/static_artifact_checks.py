#!/usr/bin/env python3
"""Independent constructor-level and bridge/claim identity checks."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text)


def digest(text: str) -> str:
    return hashlib.sha256(normalized(text).encode()).hexdigest()


def main() -> int:
    failures: list[str] = []
    solution = normalized((ROOT / "solution.mpy").read_text())
    spec = (ROOT / "spec.k").read_text()
    verification = (ROOT / "verification.k").read_text()

    prefix = 'Module(FuncDef("string_xor",Params("a","b"),'
    if not solution.startswith(prefix) or not solution.endswith("))"):
        failures.append("solution.mpy is not the expected one-function Module shape")
        body = ""
    else:
        body = solution[len(prefix) : -2]

    expected_closure = f'closureVal(("a","b"),{body},0)'
    closure_occurrences = normalized(spec).count(expected_closure)
    print(
        "ENTRY_CLOSURE"
        f" exact_constructor_occurrences={closure_occurrences}"
        f" expected_hash={hashlib.sha256(expected_closure.encode()).hexdigest()}"
    )
    if closure_occurrences != 1:
        failures.append(
            f"expected exact closure once in spec.k, found {closure_occurrences}"
        )

    loop_module = spec.split("module LOOP-SPEC", 1)
    if len(loop_module) != 2:
        failures.append("missing LOOP-SPEC module")
        loop_claim = ""
    else:
        loop_claim_parts = loop_module[1].split("claim [loop-invariant]:", 1)
        if len(loop_claim_parts) != 2:
            failures.append("missing loop-invariant claim")
            loop_claim = ""
        else:
            loop_claim = loop_claim_parts[1].split("endmodule", 1)[0]

    verification_module = verification.split("module VERIFICATION\n", 1)
    if len(verification_module) != 2:
        failures.append("missing VERIFICATION module")
        bridge = ""
    else:
        bridge_parts = verification_module[1].split("\n  rule\n", 1)
        if len(bridge_parts) != 2:
            failures.append("missing operational bridge")
            bridge = ""
        else:
            bridge = bridge_parts[1].split("    [priority(40)]", 1)[0]

    bridge_match = normalized(loop_claim) == normalized(bridge)
    print(
        "LOOP_BRIDGE"
        f" exact_normalized_match={str(bridge_match).lower()}"
        f" claim_hash={digest(loop_claim)}"
        f" bridge_hash={digest(bridge)}"
    )
    if not bridge_match:
        failures.append("bridge body differs from bridge-free loop claim")

    base_module = verification.split("module VERIFICATION-BASE", 1)
    if len(base_module) != 2:
        failures.append("missing VERIFICATION-BASE module")
        base_text = ""
    else:
        base_text = base_module[1].split("endmodule", 1)[0]
    base_operational_rules = len(re.findall(r"\brule\s+<k>", base_text))
    print(f"BASE operational_k_rules={base_operational_rules}")
    if base_operational_rules:
        failures.append("VERIFICATION-BASE unexpectedly contains operational k rules")

    loop_import_ok = bool(
        re.search(
            r"module\s+LOOP-SPEC\s+imports\s+VERIFICATION-BASE",
            spec,
            flags=re.S,
        )
    )
    entry_import_ok = bool(
        re.search(r"module\s+SPEC\s+imports\s+VERIFICATION\b", spec, flags=re.S)
    )
    verification_import_ok = bool(
        re.search(
            r"module\s+VERIFICATION\s+imports\s+VERIFICATION-BASE",
            verification,
            flags=re.S,
        )
    )
    print(
        "IMPORTS"
        f" loop_uses_base={str(loop_import_ok).lower()}"
        f" entry_uses_bridge={str(entry_import_ok).lower()}"
        f" bridge_extends_base={str(verification_import_ok).lower()}"
    )
    if not all([loop_import_ok, entry_import_ok, verification_import_ok]):
        failures.append("proof module import separation is not as expected")

    bridge_count = len(
        re.findall(
            r"^\s*rule(?:\s|$)",
            verification_module[1] if len(verification_module) == 2 else "",
            flags=re.M,
        )
    )
    print(f"VERIFICATION_OPERATIONAL_RULES count={bridge_count}")
    if bridge_count != 1:
        failures.append(f"expected one operational bridge, found {bridge_count}")

    print(f"RESULT failures={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
