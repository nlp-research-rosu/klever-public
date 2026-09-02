#!/usr/bin/env python3
"""Mechanically compare the executed constructor term and instantiate each claim."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/76-is-simple-power")
VERIFICATION = ROOT / "verification.k"
MPY = ROOT / "solution.mpy"
DEFINITION = ROOT / "fresh-semantic-kompiled"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compact(text: str) -> str:
    return "".join(text.split())


verification_text = VERIFICATION.read_text()
start = verification_text.index("  rule solutionProgram")
start = verification_text.index("=>", start) + len("=>")
end = verification_text.index("\n\n  // For P", start)
rhs_k = verification_text[start:end].strip()

# `.Stmts` is the K name of an empty generated list.  In the external .mpy
# grammar the same empty list is represented by no characters between commas.
rhs_external = rhs_k.replace(".Stmts", "")
mpy_text = MPY.read_text().strip()

file_command = [
    "kast",
    "--definition",
    str(DEFINITION),
    "--sort",
    "Program",
    "--input",
    "program",
    "--output",
    "json",
    str(MPY),
]
rhs_command = [
    "kast",
    "--definition",
    str(DEFINITION),
    "--sort",
    "Program",
    "--input",
    "program",
    "--output",
    "json",
    "--expression",
    rhs_external,
]

file_run = subprocess.run(file_command, text=True, capture_output=True, check=False)
rhs_run = subprocess.run(rhs_command, text=True, capture_output=True, check=False)
file_json = json.loads(file_run.stdout) if file_run.returncode == 0 else None
rhs_json = json.loads(rhs_run.stdout) if rhs_run.returncode == 0 else None
file_term = None if file_json is None else file_json["term"]
rhs_term = None if rhs_json is None else rhs_json["term"]


def term_hash(term) -> str | None:
    if term is None:
        return None
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def power_ceiling(p: int, x: int, n: int) -> int:
    assert p > 0 and n >= 2
    while p < x:
        p *= n
    return p


def submitted_spec(x: int, n: int) -> bool:
    return x == 1 or (x > 1 and n >= 2 and power_ceiling(n, x, n) == x)


generated = load(ROOT / "solution.py", "generated_for_witnesses")
canonical = load(Path("/reference/canonical.py"), "canonical_for_witnesses")

witnesses = [
    {
        "claim": "SPEC.emitted-tree-is-shared-tree",
        "state": {"k": "literal submitted constructor tree", "env": {}, "result": "noResult", "x": 0, "n": 0},
        "precondition": "none",
        "postcondition": "the literal tree rewrites to solutionProgram; no function result is claimed",
        "satisfiable": True,
    },
    {
        "claim": "SPEC.returns-on-one",
        "state": {"x": 1, "n": -2, "env": {}, "result": "noResult"},
        "precondition": "x = 1; n arbitrary",
        "claimed_result": submitted_spec(1, -2),
        "generated_python": generated.is_simple_power(1, -2),
        "canonical_python": canonical.is_simple_power(1, -2),
        "satisfiable": True,
    },
    {
        "claim": "SPEC.rejects-below-one",
        "state": {"x": 0, "n": 2, "env": {}, "result": "noResult"},
        "precondition": "x < 1; n arbitrary",
        "claimed_result": submitted_spec(0, 2),
        "generated_python": generated.is_simple_power(0, 2),
        "canonical_python": canonical.is_simple_power(0, 2),
        "satisfiable": True,
    },
    {
        "claim": "SPEC.rejects-small-base",
        "state": {"x": 4, "n": -2, "env": {}, "result": "noResult"},
        "precondition": "x > 1 and n < 2",
        "claimed_result": submitted_spec(4, -2),
        "generated_python": generated.is_simple_power(4, -2),
        "canonical_python": canonical.is_simple_power(4, -2),
        "satisfiable": True,
        "contract_discriminator": "canonical recognizes (-2)^2 = 4; submitted rewrite/spec reject it",
    },
    {
        "claim": "SPEC.active-path-enters-loop",
        "state": {"x": 8, "n": 2, "env": {}, "result": "noResult"},
        "precondition": "x > 1 and n >= 2",
        "postcondition": "intermediate loop-head state with power = n; no returned value yet",
        "eventual_claimed_result_via_loop_claim": submitted_spec(8, 2),
        "generated_python": generated.is_simple_power(8, 2),
        "canonical_python": canonical.is_simple_power(8, 2),
        "satisfiable": True,
    },
    {
        "claim": "SPEC.loop-correct",
        "state": {
            "x": 8,
            "n": 2,
            "power": 2,
            "env": {"x": 8, "n": 2, "power": 2},
            "result": "noResult",
        },
        "precondition": "x > 1, n >= 2, and power > 0",
        "claimed_final_power": power_ceiling(2, 8, 2),
        "claimed_result": power_ceiling(2, 8, 2) == 8,
        "generated_python_from_real_entry": generated.is_simple_power(8, 2),
        "canonical_python_from_real_entry": canonical.is_simple_power(8, 2),
        "satisfiable": True,
    },
]

print(
    json.dumps(
        {
            "pinning": {
                "verification_rhs_source_span": "verification.k rule solutionProgram through the following blank line",
                "empty_list_normalization": "replace K's .Stmts with the external grammar's empty text",
                "whitespace_compact_text_equal": compact(rhs_external) == compact(mpy_text),
                "file_kast_exit": file_run.returncode,
                "rhs_kast_exit": rhs_run.returncode,
                "constructor_terms_equal": file_term == rhs_term,
                "file_constructor_sha256": term_hash(file_term),
                "rhs_constructor_sha256": term_hash(rhs_term),
                "file_kast_stderr": file_run.stderr,
                "rhs_kast_stderr": rhs_run.stderr,
            },
            "claim_witnesses": witnesses,
        },
        indent=2,
        sort_keys=True,
    )
)

if not (file_run.returncode == rhs_run.returncode == 0 and file_term == rhs_term):
    raise SystemExit(1)
