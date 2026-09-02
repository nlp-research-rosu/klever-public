#!/usr/bin/env python3
"""Mechanical constructor-level pinning and concrete claim witnesses."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/162-string-to-md5")
DEFINITION = SCRATCH / "verification-audit-kompiled"


def parse_module(term: str) -> dict:
    # Spec claims are parsed as K terms and spell typed empty lists explicitly;
    # .mpy surface syntax spells the same list units as omitted list contents.
    surface_term = term.replace(".Stmts", "").replace(".Exprs", "")
    completed = subprocess.run(
        [
            "kast",
            "--definition",
            str(DEFINITION),
            "--module",
            "MPY-SYNTAX",
            "--sort",
            "Module",
            "--output",
            "json",
            "--expression",
            surface_term,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"kast failed with {completed.returncode}: {completed.stderr}\nTERM:\n{surface_term}"
        )
    return json.loads(completed.stdout)["term"]


def extract_solution_prefixes(spec_text: str) -> list[str]:
    marker = "#loadAll(Module("
    prefixes: list[str] = []
    offset = 0
    while True:
        marker_at = spec_text.find(marker, offset)
        if marker_at < 0:
            break
        content_at = marker_at + len(marker)
        depth = 0
        in_string = False
        escaped = False
        cursor = content_at
        assignment_at = -1
        while cursor < len(spec_text):
            char = spec_text[cursor]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                cursor += 1
                continue
            if char == '"':
                in_string = True
                cursor += 1
                continue
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif depth == 0 and spec_text.startswith("Assign(", cursor):
                assignment_at = cursor
                break
            cursor += 1
        if assignment_at < 0:
            raise RuntimeError(f"no top-level harness Assign after offset {marker_at}")
        prefixes.append("Module(" + spec_text[content_at:assignment_at] + ")")
        offset = assignment_at + len("Assign(")
    return prefixes


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_to_md5


solution_term = (SCRATCH / "regenerated-solution.mpy").read_text(encoding="utf-8")
spec_text = (SCRATCH / "spec.k").read_text(encoding="utf-8")
expected_ast = parse_module(solution_term)
claim_terms = extract_solution_prefixes(spec_text)
claim_asts = [parse_module(term) for term in claim_terms]

expected_json = json.dumps(expected_ast, sort_keys=True, separators=(",", ":"))
print("COMMAND: python3 /audit-output/evidence/stage4_pinning.py")
print(f"CLAIM_MODULE_PREFIXES={len(claim_terms)}")
print(
    "EXPECTED_CONSTRUCTOR_AST_SHA256="
    + hashlib.sha256(expected_json.encode("utf-8")).hexdigest()
)
for index, claim_ast in enumerate(claim_asts, 1):
    claim_json = json.dumps(claim_ast, sort_keys=True, separators=(",", ":"))
    print(
        f"CLAIM_{index}_CONSTRUCTOR_AST_SHA256="
        + hashlib.sha256(claim_json.encode("utf-8")).hexdigest()
    )
    print(f"CLAIM_{index}_MATCHES_REGENERATED_SOLUTION={claim_ast == expected_ast}")

assert len(claim_terms) == 2
assert all(claim_ast == expected_ast for claim_ast in claim_asts)
compact_spec = "".join(spec_text.split())
assert 'Call(Name("string_to_md5"),str(.IntSeq))' in compact_spec
assert 'Call(Name("string_to_md5"),str(CS:IntSeq))' in compact_spec
assert "requiresnotBool(CS==K.IntSeq)" in compact_spec

candidate = load_entry("pin_candidate", Path("/candidate/solution.py"))
canonical = load_entry("pin_canonical", Path("/reference/canonical.py"))
empty_candidate = candidate("")
empty_canonical = canonical("")
nonempty_candidate = candidate("a")
nonempty_canonical = canonical("a")

print("EMPTY_WITNESS_K_INPUT=str(.IntSeq)")
print(f"EMPTY_CANDIDATE_RESULT={empty_candidate!r}")
print(f"EMPTY_CANONICAL_RESULT={empty_canonical!r}")
print("EMPTY_CLAIM_RESULT=noneV")
print("NONEMPTY_WITNESS_K_INPUT=str(iCons(97,.IntSeq))")
print("NONEMPTY_PRECONDITION_NOT_EMPTY=true")
print(f"NONEMPTY_CANDIDATE_RESULT={nonempty_candidate}")
print(f"NONEMPTY_CANONICAL_RESULT={nonempty_canonical}")
print("NONEMPTY_CLAIM_RESULT=str(md5hexCodes(iCons(97,.IntSeq)))")
print("NONEMPTY_PRIMITIVE_INTERPRETATION=0cc175b9c0f1b6a831c399e269772661")

assert empty_candidate is None
assert empty_canonical is None
assert nonempty_candidate == "0cc175b9c0f1b6a831c399e269772661"
assert nonempty_canonical == nonempty_candidate
