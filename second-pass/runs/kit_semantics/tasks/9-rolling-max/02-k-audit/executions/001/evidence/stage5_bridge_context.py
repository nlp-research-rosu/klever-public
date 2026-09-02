#!/usr/bin/env python3
"""Compare operational bridge source domains with their connection claims."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/candidate")


def compact(text: str) -> str:
    text = re.sub(r"//[^\n]*", "", text)
    return re.sub(r"\s+", "", text)


verification = (ROOT / "verification.k").read_text()
loop_spec = (ROOT / "loop-spec.k").read_text()
bind_spec = (ROOT / "bind-spec.k").read_text()

loop_rule = verification[
    verification.index("  rule\n", verification.index("// Exact loop summary"))
    : verification.index("endmodule", verification.index("// Exact loop summary"))
]
loop_claim = loop_spec[
    loop_spec.index("  claim [rolling-loop-connection]:")
    : loop_spec.index("endmodule")
]
normalized_rule = compact(loop_rule)
normalized_rule = normalized_rule.removeprefix("rule").removesuffix("[priority(40)]")
normalized_claim = compact(loop_claim).removeprefix(
    "claim[rolling-loop-connection]:"
)

print(f"loop_complete_domain_text_equal={normalized_rule == normalized_claim}")
print(f"loop_rule_normalized_chars={len(normalized_rule)}")
print(f"loop_claim_normalized_chars={len(normalized_claim)}")

checks = {
    "bind_continuation_universal": "#bindTgt(Name(X:String),I:Int)~>CONT:K=>CONT"
    in compact(bind_spec),
    "bind_same_env": "<env>L:Int</env>" in compact(bind_spec)
    and "<env>L:Int</env>" in compact(verification),
    "bind_same_scope_update": "M:Map=>M[X<-I]" in compact(bind_spec)
    and "M:Map=>M[X<-I]" in compact(verification),
    "bind_same_guard": 'notBool("$cells"in_keys(M))' in compact(bind_spec)
    and 'notBool("$cells"in_keys(M))' in compact(verification),
    "bind_bridge_preserves_k_frame": "#bindTgt(Name(X:String),I:Int)=>.K..."
    in compact(verification),
}
for name, result in checks.items():
    print(f"{name}={result}")

scratch = Path("/tmp/audit-work/rolling-max-20260729")
bind_definition = (scratch / "audit-bind-kompiled/definition.kore").read_text()
loop_definition = (scratch / "audit-loop-kompiled/definition.kore").read_text()
verification_definition = (
    scratch / "audit-verification-kompiled/definition.kore"
).read_text()
module_checks = {
    "bind_definition_excludes_bind_bridge": "Location(56,8,61,46)"
    not in bind_definition,
    "bind_definition_excludes_loop_bridge": "Location(72,5,113,25)"
    not in bind_definition,
    "loop_definition_includes_bind_bridge": "Location(56,8,61,46)"
    in loop_definition,
    "loop_definition_excludes_loop_bridge": "Location(72,5,113,25)"
    not in loop_definition,
    "verification_definition_includes_bind_bridge": "Location(56,8,61,46)"
    in verification_definition,
    "verification_definition_includes_loop_bridge": "Location(72,5,113,25)"
    in verification_definition,
}
for name, result in module_checks.items():
    print(f"{name}={result}")

ok = (
    normalized_rule == normalized_claim
    and all(checks.values())
    and all(module_checks.values())
)
print(f"BRIDGE_CONTEXT_OK={ok}")
raise SystemExit(0 if ok else 1)
