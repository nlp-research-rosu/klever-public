#!/usr/bin/env python3
"""Independent target-identity, candidate-gate, and axiom-accounting checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract

GENERATION = Path("/reference/klean-generation")
CANDIDATE = Path("/candidate")
FRESH = Path("/tmp/audit-work/proof-audit-base")
AUDIT_INPUT = Path("/audit-input.json")
AXIOM_LOG = Path("/audit-output/evidence/09_print_axioms.log")


def check(label: str, observed: object, expected: object) -> None:
    if observed != expected:
        raise SystemExit(f"FAIL {label}: observed={observed!r}, expected={expected!r}")
    print(f"PASS {label}: {observed!r}")


def main() -> None:
    manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
    trust = json.loads((GENERATION / "trust-inventory.json").read_text())
    audit_doc = json.loads(AUDIT_INPUT.read_text())
    resolution, _ = stage6_resolution_contract.verify_audit_input(audit_doc)
    target_generated = klean_export.target_statement(GENERATION / "generated")
    target_fresh = klean_export.target_statement(FRESH / "Base")

    print("COMMAND: PYTHONPATH=/reference python3 /audit-output/evidence/identity_and_trust_audit.py")
    check("generated target equals generator manifest", target_generated, manifest["target"])
    check("fresh Base target equals generator manifest", target_fresh, manifest["target"])
    check("generated target equals launcher audit input", target_generated, resolution["target"])
    check("candidate export digest before Base injection", klean_export.tree_digest(CANDIDATE),
          "f670251ed12214561dd2cb800ac2bc7b4bae37991fc9bdfcfcf8ee6d9814c92c")
    check("candidate pipeline tree", pipeline_contract.sha256_tree(CANDIDATE),
          resolution["hashes"]["lean_workspace_sha256"])

    candidate_sources = "\n".join(
        path.read_text() for path in sorted(CANDIDATE.rglob("*.lean"))
    )
    forbidden = re.findall(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", candidate_sources)
    check("candidate forbidden-token occurrences", forbidden, [])
    check("candidate targetStatement references (theorem type and unfold only)",
          candidate_sources.count("targetStatement"), 2)
    check("candidate definitions of targetStatement",
          len(re.findall(r"^(?:noncomputable\s+)?def\s+targetStatement\b", candidate_sources, re.MULTILINE)), 0)

    theorem_statement = manifest["target"]["statement"]
    proof_text = (CANDIDATE / "Proof.lean").read_text()
    check("Proof.final contains exact fixed statement", theorem_statement in proof_text, True)

    axiom_text = AXIOM_LOG.read_text(errors="replace")
    match = re.search(r"depends on axioms: \[([^\]]*)\]", axiom_text)
    if not match:
        raise SystemExit("FAIL could not parse exact #print axioms output")
    used = sorted(item.strip() for item in match.group(1).split(",") if item.strip())
    project_allowlist = sorted(entry["name"] for entry in trust["allowlist"])
    core_allowlist = ["Classical.choice", "Quot.sound", "propext"]
    check("used Proof.final axioms", used, sorted(core_allowlist))
    check("sorryAx absent", "sorryAx" in used, False)
    check("used generated/project trust-inventory axioms", sorted(set(used) & set(project_allowlist)), [])
    unrecorded_escape = sorted(set(used) - set(project_allowlist) - set(core_allowlist))
    check("unrecorded proof trust escapes", unrecorded_escape, [])
    print(f"PASS trust inventory entries reviewed: {len(project_allowlist)}; none are dependencies of Proof.final")


if __name__ == "__main__":
    main()
