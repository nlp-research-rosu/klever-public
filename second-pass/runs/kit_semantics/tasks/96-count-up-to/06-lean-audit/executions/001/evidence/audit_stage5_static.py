#!/usr/bin/env python3
"""Static candidate, target, trust, and operational-binding audit."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks: list[tuple[str, bool, object]] = []


def check(label: str, condition: bool, observed: object = None) -> None:
    checks.append((label, condition, observed))


candidate = Path("/candidate")
copy = Path("/tmp/audit-work/proof-audit-source-only.k206OF")
generated = Path("/reference/klean-generation/generated")
base = copy / "Base"
proof = (candidate / "Proof.lean").read_text()
manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
trust = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
audit_input = json.loads(Path("/audit-input.json").read_text())

# The source-only audit copy and its immutable Base are byte-identical.
for name in ("Proof.lean", "lake-manifest.json", "lakefile.lean", "lean-toolchain"):
    check(
        f"candidate copy unchanged:{name}",
        digest(candidate / name) == digest(copy / name),
        (digest(candidate / name), digest(copy / name)),
    )
for source in sorted(path for path in generated.rglob("*") if path.is_file()):
    relative = source.relative_to(generated)
    check(
        f"Base unchanged:{relative.as_posix()}",
        digest(source) == digest(base / relative),
        (digest(source), digest(base / relative)),
    )

# Candidate source does not create proof trust or replace/shadow the target.
candidate_lean = [
    path
    for path in candidate.rglob("*.lean")
    if "Base" not in path.relative_to(candidate).parts
]
forbidden = {
    "sorry": re.compile(r"\bsorry\b"),
    "admit": re.compile(r"\badmit\b"),
    "unsafe": re.compile(r"\bunsafe\b"),
    "axiom": re.compile(r"(?m)^\s*axiom\b"),
    "opaque": re.compile(r"(?m)^\s*opaque\b"),
}
for path in candidate_lean:
    text = path.read_text()
    for token, pattern in forbidden.items():
        check(
            f"no candidate {token}:{path.name}",
            pattern.search(text) is None,
            pattern.findall(text),
        )
check(
    "candidate has no targetStatement definition",
    re.search(r"(?m)^\s*def\s+targetStatement\b", proof) is None,
)
check(
    "candidate does not enter generated target namespace",
    "namespace Klean96CountUpTo.Lemmas" not in proof,
)
check(
    "candidate imports exact generated target module",
    re.findall(r"(?m)^\s*import\s+(.+?)\s*$", proof)
    == ["Klean96CountUpTo.Lemmas"],
    re.findall(r"(?m)^\s*import\s+(.+?)\s*$", proof),
)

# Locate the exact one target-parameter definition and match the frozen K equations.
definition_matches = re.findall(
    r"(?ms)^def «valSeqConcat\(_,_\)_MPY-LIST_ValSeq_ValSeq_ValSeq».*?"
    r"(?=^private theorem)",
    proof,
)
check("one exact target-parameter def", len(definition_matches) == 1, len(definition_matches))
expected_definition = """def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» :
    SortValSeq → SortValSeq → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», tail => tail
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head rest, tail =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        head
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» rest tail)"""
if definition_matches:
    check(
        "candidate def exactly implements K recursive equations",
        definition_matches[0].strip() == expected_definition,
        definition_matches[0].strip(),
    )
all_defs = re.findall(r"(?m)^\s*def\s+([^\s:]+)", proof)
check(
    "candidate has exactly one def",
    all_defs == ["«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»"],
    all_defs,
)

parameter = manifest["target"]["parameters"][0]
check(
    "parameter KORE symbol",
    parameter["kore_symbol"]
    == "LblvalSeqConcat'LParUndsCommUndsRParUnds'MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq",
    parameter["kore_symbol"],
)
check(
    "KORE symbol exists in frozen compiled definition",
    parameter["kore_symbol"]
    in Path("/reference/k-proof/verification-kompiled/definition.kore").read_text(),
)
source_rules = [
    "rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97",
    "rule-1bc30aceb4ec6e423c8f79079ea7b1c195de5d88396229aa8ee74794085384fa",
]
check("parameter source-rule IDs", parameter["source_rule_ids"] == source_rules, parameter["source_rule_ids"])
list_semantics = Path(
    "/reference/k-proof/reference-semantics/semantics/list.k"
).read_text()
for exact_rule in (
    "rule valSeqConcat(.ValSeq, T:ValSeq)                => T",
    "rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => "
    "vCons(V, valSeqConcat(S, T))",
):
    check(f"frozen K equation:{exact_rule[:38]}", exact_rule in list_semantics)
check(
    "source solution uses list append",
    "primes.append(candidate)" in Path("/reference/k-proof/solution.py").read_text(),
)
check(
    "operational append uses valSeqConcat with singleton",
    "list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq)))" in list_semantics,
)

# Proof.final has exactly the fixed generated theorem as its type.
final_headers = re.findall(
    r"(?ms)^theorem\s+final\s*:\s*(.*?)\s*:=\s*by",
    proof,
)
check("one Proof.final declaration", len(final_headers) == 1, final_headers)
expected_final_type = (
    "Klean96CountUpTo.Lemmas.targetStatement "
    "«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»"
)
if final_headers:
    check(
        "Proof.final exact fixed type",
        " ".join(final_headers[0].split()) == expected_final_type,
        " ".join(final_headers[0].split()),
    )
check(
    "fixed target consistent with audit input",
    manifest["target"] == audit_input["resolution"]["target"],
)

# Exact axiom output and trust-ledger reconciliation.
axiom_log = Path("/audit-output/evidence/09b_source_only_print_axioms.log").read_text()
check(
    "Proof.final axiom set empty",
    "'Proof.final' does not depend on any axioms" in axiom_log,
    axiom_log,
)
check("no sorryAx", "sorryAx" not in axiom_log, axiom_log)
allowlist = trust["allowlist"]
allowlist_names = [entry["name"] for entry in allowlist]
check("trust inventory contains 48 generated declarations", len(allowlist) == 48, len(allowlist))
check("trust inventory names unique", len(allowlist_names) == len(set(allowlist_names)))
check(
    "no generated trust declaration is targetStatement",
    all("targetStatement" not in name for name in allowlist_names),
)
check(
    "empty dependency set needs no allowlisted assumptions",
    "does not depend on any axioms" in axiom_log,
)

failures = []
for label, passed, observed in checks:
    if not passed:
        failures.append(label)
        print(f"FAIL: {label}\n  observed={observed!r}")
print(f"CHECK_COUNT={len(checks)}")
print(f"FAILURE_COUNT={len(failures)}")
print(f"RESULT={'FAIL' if failures else 'PASS'}")
raise SystemExit(1 if failures else 0)
