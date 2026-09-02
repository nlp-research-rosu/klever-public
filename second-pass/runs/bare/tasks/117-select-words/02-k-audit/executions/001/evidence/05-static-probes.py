#!/usr/bin/env python3
"""Operational probes for the exact-expression semantic bridge."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(command: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"EXIT: {completed.returncode}")
    print(completed.stdout.rstrip())
    return completed


def krun(root: Path, definition: str, s: str, n: int):
    return run(
        [
            "krun",
            "solution.mpy",
            "--definition",
            definition,
            f"-cS={json.dumps(s)}",
            f"-cN={n}",
        ],
        root,
    )


def main() -> int:
    root = Path("/tmp/audit-work/fresh")
    candidate = load_module("submitted_solution_probe", root / "solution.py")
    canonical = load_module(
        "trusted_canonical_probe", root / "trusted/canonical.py"
    )
    failures = 0

    print("PROBE 1: remove only the exact ListComp eval bridge")
    no_bridge = krun(root, "semantic-no-eval-kompiled", "Mary had a little lamb", 4)
    compact = re.sub(r"\s+", "", no_bridge.stdout)
    expected_residual = (
        no_bridge.returncode == 0
        and "<k>eval(" in compact
        and "~>finish~>.K</k>" in compact
        and "<result>noResult</result>" in compact
        and "<k>.K</k>" not in compact
    )
    print(f"EXPECTED_EVAL_RESIDUAL: {expected_residual}")
    if not expected_residual:
        failures += 1

    print("PROBE 2: complete bridge domain exceeds the source-contract domain")
    off_domain_s = "a\tb"
    print(f"PYTHON_RESULT: {candidate.select_words(off_domain_s, 1)!r}")
    off_domain = krun(root, "semantic-kompiled", off_domain_s, 1)
    off_compact = re.sub(r"\s+", "", off_domain.stdout)
    expected_off_domain_divergence = (
        candidate.select_words(off_domain_s, 1) == ["b"]
        and "pyList(.Words)" in off_compact
    )
    print(f"EXPECTED_OFF_DOMAIN_DIVERGENCE: {expected_off_domain_divergence}")
    if not expected_off_domain_divergence:
        failures += 1

    print("PROBE 3: non-ASCII letters are inside the stated letters/spaces domain")
    unicode_s = "é"
    print(f"CANONICAL_PYTHON_RESULT: {canonical.select_words(unicode_s, 1)!r}")
    print(f"CANDIDATE_PYTHON_RESULT: {candidate.select_words(unicode_s, 1)!r}")
    unicode_case = krun(root, "semantic-kompiled", unicode_s, 1)
    unicode_compact = re.sub(r"\s+", "", unicode_case.stdout)
    expected_unicode_divergence = (
        unicode_case.returncode == 0
        and canonical.select_words(unicode_s, 1) == ["é"]
        and candidate.select_words(unicode_s, 1) == ["é"]
        and "pyList(.Words)" in unicode_compact
    )
    print(f"EXPECTED_IN_DOMAIN_UNICODE_DIVERGENCE: {expected_unicode_divergence}")
    if not expected_unicode_divergence:
        failures += 1
    print("PROBE 4: identify the generated semantics' modeled Unicode count")
    print(f"CANONICAL_PYTHON_RESULT_N2: {canonical.select_words(unicode_s, 2)!r}")
    print(f"CANDIDATE_PYTHON_RESULT_N2: {candidate.select_words(unicode_s, 2)!r}")
    unicode_count_two = krun(root, "semantic-kompiled", unicode_s, 2)
    unicode_two_compact = re.sub(r"\s+", "", unicode_count_two.stdout)
    expected_modeled_count_two = (
        unicode_count_two.returncode == 0
        and canonical.select_words(unicode_s, 2) == []
        and candidate.select_words(unicode_s, 2) == []
        and "pyList(WCons(" in unicode_two_compact
    )
    print(f"EXPECTED_K_MODELED_COUNT_TWO: {expected_modeled_count_two}")
    if not expected_modeled_count_two:
        failures += 1

    print(f"static_probe_failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
