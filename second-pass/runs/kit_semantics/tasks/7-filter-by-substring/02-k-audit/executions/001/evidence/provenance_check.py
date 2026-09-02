#!/usr/bin/env python3
"""Independent mounted-input and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def entry_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in sorted(directories + files):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                entries[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                entries[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                entries[rel] = ("file", sha256_file(path))
            else:
                entries[rel] = ("other", oct(mode))
    return entries


def canonical_manifest_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    encoded = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    data = json.loads(AUDIT.read_text())
    recorded = data["hashes"]
    checks = {
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation/invocation.json"),
        "generation_metrics_sha256": Path("/generation/metrics.json"),
        "generation_runtime_metrics_sha256": Path("/generation/runtime-metrics.json"),
        "generation_usage_sha256": Path("/generation/usage.json"),
        "generation_codex_last_sha256": Path("/generation/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation/codex-output.log"),
        "generation_prompt_sha256": Path("/generation/prompt.txt"),
    }
    failures: list[str] = []
    print("FILE_HASH_CHECKS")
    for key, path in checks.items():
        actual = sha256_file(path)
        expected = recorded[key]
        ok = actual == expected
        print(f"{key} expected={expected} actual={actual} match={ok} path={path}")
        if not ok:
            failures.append(key)

    result = json.loads(Path("/generation-result.json").read_text())
    print("GENERATION_RESULT_EVIDENCE_HASH_CHECKS")
    generation_root = Path("/generation")
    for rel, expected in sorted(result["outputs"]["evidence"].items()):
        path = generation_root / rel
        actual = sha256_file(path)
        ok = actual == expected
        print(f"{rel} expected={expected} actual={actual} match={ok}")
        if not ok:
            failures.append(f"generation-result:{rel}")

    trusted = entry_manifest(Path("/reference/reference-semantics"))
    candidate = entry_manifest(Path("/candidate/reference-semantics"))
    print("SUPPLIED_SEMANTICS_ENTRY_COUNTS")
    print(f"trusted={len(trusted)} candidate={len(candidate)}")
    print("SUPPLIED_SEMANTICS_CANONICAL_MANIFEST_DIGESTS")
    print(f"trusted={canonical_manifest_digest(trusted)}")
    print(f"candidate={canonical_manifest_digest(candidate)}")

    all_names = sorted(set(trusted) | set(candidate))
    differences = 0
    print("SUPPLIED_SEMANTICS_ENTRY_COMPARISON")
    for name in all_names:
        left = trusted.get(name)
        right = candidate.get(name)
        equal = left == right
        print(f"{name}\ttrusted={left}\tcandidate={right}\tmatch={equal}")
        if not equal:
            differences += 1
            failures.append(f"semantics:{name}")

    print("SEMANTICS_RECORDED_TREE_HASH_CLAIMS")
    for key in (
        "candidate_reference_semantics_sha256",
        "trusted_reference_semantics_sha256",
        "trusted_reference_semantics_manifest_sha256",
    ):
        print(f"{key}={recorded[key]}")
    print(
        "NOTE: launcher tree-digest serialization is not specified; "
        "the independent canonical manifest digest above is reviewer-defined."
    )
    print(f"semantics_differences={differences}")
    print(f"failures={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
