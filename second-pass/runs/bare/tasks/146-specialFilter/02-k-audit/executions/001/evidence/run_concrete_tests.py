#!/usr/bin/env python3
"""Execute fresh generated semantics and compare final values with both Pythons."""

from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import subprocess


ROOT = Path("/tmp/audit-work/146-specialFilter")
DEFINITION = ROOT / "candidate/fresh-semantic-kompiled"
MANIFEST = ROOT / "concrete-inputs/manifest.json"
LOGS = Path("/audit-output/evidence/concrete-runs")


def load_function(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.specialFilter


def main() -> int:
    canonical = load_function(ROOT / "reference/canonical.py", "canonical_for_krun")
    candidate = load_function(ROOT / "candidate/solution.py", "candidate_for_krun")
    tests = json.loads(MANIFEST.read_text(encoding="utf-8"))
    LOGS.mkdir(parents=True, exist_ok=True)
    failures = []
    for test in tests:
        command = [
            "krun",
            test["path"],
            "--definition",
            str(DEFINITION),
        ]
        started = datetime.now(timezone.utc)
        result = subprocess.run(
            command,
            cwd=ROOT / "candidate",
            env=os.environ.copy(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
        )
        match = re.search(r"<k>\s*intVal \( (-?\d+) \) ~> \.K\s*</k>", result.stdout)
        k_value = int(match.group(1)) if match else None
        canonical_value = canonical(list(test["nums"]))
        candidate_value = candidate(list(test["nums"]))
        expected = test["expected"]
        ok = (
            result.returncode == 0
            and k_value == canonical_value == candidate_value == expected
            and "<env>\n    .Map\n  </env>" in result.stdout
        )
        log = LOGS / f"{test['name']}.log"
        log.write_text(
            "\n".join(
                [
                    f"started_utc: {started.isoformat()}",
                    f"cwd: {ROOT / 'candidate'}",
                    f"command: {shlex.join(command)}",
                    f"exit_status: {result.returncode}",
                    f"finished_utc: {datetime.now(timezone.utc).isoformat()}",
                    f"input: {json.dumps(test['nums'])}",
                    f"canonical_python: {canonical_value}",
                    f"candidate_python: {candidate_value}",
                    f"k_result: {k_value}",
                    f"match: {'yes' if ok else 'no'}",
                    "--- output ---",
                    result.stdout,
                ]
            ),
            encoding="utf-8",
        )
        print(
            f"case={test['name']} exit_status={result.returncode} "
            f"canonical={canonical_value} candidate={candidate_value} "
            f"k={k_value} match={'yes' if ok else 'no'} log={log}"
        )
        if not ok:
            failures.append(test["name"])
    print(f"successful_concrete_cases={len(tests) - len(failures)}/{len(tests)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
