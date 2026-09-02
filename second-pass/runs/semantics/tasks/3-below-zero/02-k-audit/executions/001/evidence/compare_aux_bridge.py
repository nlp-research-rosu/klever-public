#!/usr/bin/env python3
"""Verify that the admitted loop rule is exactly the bridge-free AUX claim."""

from __future__ import annotations

import re
from pathlib import Path


SPEC = Path("/tmp/audit-work/rebuild/candidate/spec.k")
VERIFICATION = Path("/tmp/audit-work/rebuild/candidate/verification.k")


def module_body(text: str, name: str) -> str:
    match = re.search(
        rf"(?ms)^module {re.escape(name)}\s*$" r"(.*?)^endmodule\s*$", text
    )
    if match is None:
        raise RuntimeError(f"module not found: {name}")
    return match.group(1)


def normalize_claim_or_rule(body: str, keyword: str) -> str:
    index = body.find(keyword)
    if index < 0:
        raise RuntimeError(f"{keyword} not found")
    value = body[index + len(keyword) :]
    value = re.sub(r"\[priority\(40\)\]\s*$", "", value.strip())
    return " ".join(value.split())


def main() -> int:
    spec_text = SPEC.read_text(encoding="utf-8")
    verification_text = VERIFICATION.read_text(encoding="utf-8")
    aux_module = module_body(spec_text, "AUX-SPEC")
    bridge_module = module_body(verification_text, "MPY-VERIFICATION-LEMMA")
    aux_imports = re.findall(r"(?m)^\s*imports\s+(\S+)", aux_module)
    aux = normalize_claim_or_rule(aux_module, "claim")
    bridge = normalize_claim_or_rule(bridge_module, "rule")
    print(f"aux_imports={aux_imports}")
    print("bridge_free=" + str(aux_imports == ["MPY-VERIFICATION"]).lower())
    print(f"normalized_aux_chars={len(aux)}")
    print(f"normalized_bridge_chars={len(bridge)}")
    print("exact_match=" + str(aux == bridge).lower())
    if aux != bridge:
        print("AUX=" + aux)
        print("BRIDGE=" + bridge)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
