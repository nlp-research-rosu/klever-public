#!/usr/bin/env python3
"""Compare compiled-literal Unicode K runs with canonical Python results."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


WRAPPER_ROOT = Path("/tmp/audit-work/unicode-wrapper")
PROBE_ROOT = Path("/tmp/audit-work/string-probe")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def label(term: dict[str, Any]) -> str | None:
    raw = term.get("label")
    return raw.get("name") if isinstance(raw, dict) else None


def walk(term: Any):
    yield term
    if isinstance(term, dict):
        for value in term.values():
            yield from walk(value)
    elif isinstance(term, list):
        for value in term:
            yield from walk(value)


def wrapper_result_token(case_file: str) -> str:
    completed = subprocess.run(
        [
            "krun",
            case_file,
            "--definition",
            "unicode-wrapper-kompiled",
            '-cS=""',
            "--output",
            "json",
        ],
        cwd=WRAPPER_ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr)
    document = json.loads(completed.stdout)
    for term in walk(document):
        if (
            isinstance(term, dict)
            and term.get("node") == "KApply"
            and str(label(term)).startswith("pyStr(")
        ):
            return term["args"][0]["token"]
    raise LookupError("pyStr result")


def expected_probe_token(probe: str) -> str:
    completed = subprocess.run(
        [
            "krun",
            "/dev/stdin",
            "--definition",
            "string-probe3-kompiled",
            "--output",
            "json",
        ],
        cwd=PROBE_ROOT,
        input=probe,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr)
    document = json.loads(completed.stdout)
    for term in walk(document):
        if (
            isinstance(term, dict)
            and term.get("node") == "KToken"
            and term.get("sort", {}).get("name") == "String"
        ):
            return term["token"]
    raise LookupError("String token")


canonical = load_module("canonical_unicode_compare", Path("/reference/canonical.py"))
generated = load_module("generated_unicode_compare", Path("/candidate/solution.py"))

cases = [
    (
        "UnicodeCaseOne",
        "probeExpectedOne",
        "éα中🙂𝄞",
        "中éα🙂𝄞",
    ),
    (
        "UnicodeCaseTwo",
        "probeExpectedTwo",
        "e\u0301🙂中A",
        "🙂e\u0301中A",
    ),
]

failures = 0
for case_file, probe, source, expected_text in cases:
    actual_token = wrapper_result_token(case_file)
    expected_token = expected_probe_token(probe)
    canonical_text = canonical.decode_cyclic(source)
    generated_text = generated.decode_cyclic(source)
    token_match = actual_token == expected_token
    text_match = canonical_text == generated_text == expected_text
    print(f"CASE={case_file}")
    print(f"SOURCE={source!r}")
    print(f"ACTUAL_K_TOKEN={actual_token!r}")
    print(f"EXPECTED_K_TOKEN={expected_token!r}")
    print(f"K_TOKEN_MATCH={token_match}")
    print(f"PY_CANONICAL={canonical_text!r}")
    print(f"PY_GENERATED={generated_text!r}")
    print(f"EXPECTED_TEXT={expected_text!r}")
    print(f"PY_TEXT_MATCH={text_match}")
    failures += not (token_match and text_match)

print(f"FAILURE_COUNT: {failures}")
sys.exit(1 if failures else 0)
