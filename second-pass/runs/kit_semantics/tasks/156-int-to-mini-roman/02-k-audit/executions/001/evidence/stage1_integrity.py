#!/usr/bin/env python3
"""Independent provenance and mounted-tree integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISREG(mode):
            result[relative] = ("file", sha256(path))
        elif stat.S_ISDIR(mode):
            result[relative] = ("directory", None)
        elif stat.S_ISLNK(mode):
            result[relative] = ("symlink", os.readlink(path))
        else:
            result[relative] = ("other", oct(mode))
    return result


def check_hash(
    label: str, path: Path, expected: str, failures: list[str]
) -> None:
    actual = sha256(path)
    status = "PASS" if actual == expected else "FAIL"
    print(f"{status} {label}: expected={expected} actual={actual} path={path}")
    if status == "FAIL":
        failures.append(label)


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"problem_id={audit['problem_id']}")
    print(f"condition={audit['condition']}")

    if lock == audit["audit_campaign"]:
        print("PASS campaign lock JSON exactly equals audit_campaign block")
    else:
        print("FAIL campaign lock JSON differs from audit_campaign block")
        failures.append("campaign-lock-block")

    hashes = audit["hashes"]
    direct_checks = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_metrics_sha256": Path(
            "/generation-evidence/metrics.json"
        ),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_runtime_metrics_sha256": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "run_manifest_sha256": Path("/run.json"),
        "stage1_invocation_sha256": Path(
            "/generation-evidence/invocation.json"
        ),
        "stage1_result_sha256": Path("/generation-result.json"),
        "task_manifest_sha256": Path("/task.json"),
    }
    for key, path in direct_checks.items():
        check_hash(key, path, hashes[key], failures)

    trace_files = sorted(
        Path("/generation-evidence/codex-trace").rglob("*.jsonl")
    )
    if len(trace_files) != 1:
        print(f"FAIL expected one structured trace, found {len(trace_files)}")
        failures.append("trace-file-count")
    else:
        expected = json.loads(
            Path("/generation-result.json").read_text(encoding="utf-8")
        )["outputs"]["evidence"][
            "codex-trace/2026/07/25/"
            "rollout-2026-07-25T03-48-50-"
            "019f9876-8043-7010-ab59-52e907ac9b57.jsonl"
        ]
        check_hash("structured trace file", trace_files[0], expected, failures)

    candidate_semantics = entries(
        Path("/candidate/reference-semantics")
    )
    trusted_semantics = entries(Path("/reference/reference-semantics"))
    if candidate_semantics == trusted_semantics:
        print(
            "PASS supplied semantics entry types and file hashes are "
            f"identical ({len(candidate_semantics)} entries)"
        )
    else:
        print("FAIL candidate supplied-semantics tree differs from trusted tree")
        failures.append("supplied-semantics-tree")
        for name in sorted(candidate_semantics.keys() | trusted_semantics.keys()):
            if candidate_semantics.get(name) != trusted_semantics.get(name):
                print(
                    f"  {name}: candidate={candidate_semantics.get(name)} "
                    f"trusted={trusted_semantics.get(name)}"
                )

    for root in (
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ):
        special = [
            (name, value)
            for name, value in entries(root).items()
            if value[0] in {"symlink", "other"}
        ]
        if special:
            print(f"FAIL special entries below {root}: {special}")
            failures.append(f"special-entry:{root}")
        else:
            print(f"PASS no symlink or special entries below {root}")

    required = [
        "/run.json",
        "/task.json",
        "/generation-result.json",
        "/generation-evidence/invocation.json",
        "/generation-evidence/metrics.json",
        "/generation-evidence/runtime-metrics.json",
        "/generation-evidence/usage.json",
        "/generation-evidence/codex-last.txt",
        "/generation-evidence/codex-output.log",
        "/generation-evidence/prompt.txt",
        "/generation-evidence/codex-trace",
        "/candidate/prompt.py",
        "/candidate/py2mpy.py",
        "/candidate/reference-semantics",
        "/reference/prompt.py",
        "/reference/py2mpy.py",
        "/reference/canonical.py",
        "/reference/reference-semantics",
    ]
    for raw in required:
        path = Path(raw)
        if path.exists() and os.access(path, os.R_OK):
            print(f"PASS required readable artifact: {path}")
        else:
            print(f"FAIL required missing/unreadable artifact: {path}")
            failures.append(f"required:{path}")

    if failures:
        print("OVERALL: FAIL " + ",".join(failures))
        return 1
    print("OVERALL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
