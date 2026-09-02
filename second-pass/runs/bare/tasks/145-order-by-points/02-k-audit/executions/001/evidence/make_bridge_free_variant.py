#!/usr/bin/env python3
"""Remove the exact-lambda-to-PointKey operational bridge for sensitivity."""

from pathlib import Path


source = Path("/tmp/audit-work/proof145/semantic.k")
scratch_target = Path("/tmp/audit-work/proof145/semantic-no-point-bridge.k")
evidence_target = Path("/audit-output/evidence/semantic-no-point-bridge.k")
text = source.read_text(encoding="utf-8")
text = text.replace(
    "module MPY-SEMANTICS\n", "module MPY-SEMANTICS-NO-POINT-BRIDGE\n", 1
)
start_marker = "  rule eval(\n         Lambda(\n"
end_marker = "    => PointKey\n"
start = text.find(start_marker)
if start < 0:
    raise SystemExit("exact lambda bridge start not found")
end = text.find(end_marker, start)
if end < 0:
    raise SystemExit("exact lambda bridge end not found")
end += len(end_marker)
variant = text[:start] + text[end:]
for target in (scratch_target, evidence_target):
    target.write_text(variant, encoding="utf-8")
print(f"removed_bytes={end - start}")
print(f"scratch={scratch_target}")
print(f"evidence={evidence_target}")
