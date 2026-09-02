#!/usr/bin/env python3
"""Independent launcher/mount integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in sorted(dirs + files):
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                result[rel] = ("symlink", os.readlink(path))
            elif path.is_dir():
                result[rel] = ("directory", None)
            elif path.is_file():
                result[rel] = ("file", sha256_file(path))
            else:
                result[rel] = ("other", None)
    return result


def print_check(label: str, actual: object, expected: object) -> bool:
    ok = actual == expected
    print(f"{label}: {'OK' if ok else 'MISMATCH'}")
    if not ok:
        print(f"  expected={expected!r}")
        print(f"  actual={actual!r}")
    return ok


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    ok = True

    ok &= print_check("campaign block equals lock JSON", audit["audit_campaign"], lock)
    ok &= print_check(
        "campaign lock SHA-256",
        sha256_file(LOCK),
        audit["hashes"]["audit_campaign_lock_sha256"],
    )
    ok &= print_check("declared record layout", audit["record_layout"], "legacy-selected-stage1")
    ok &= print_check("declared semantics mode", audit["semantics_mode"], "SUPPLIED_SEMANTICS")
    ok &= print_check("trusted semantics mount requested", audit["mount_reference_semantics"], True)

    required = {
        "run_manifest": Path("/run.json"),
        "task_manifest": Path("/task.json"),
        "stage1_result": Path("/generation-result.json"),
        "generation_manifest": Path("/generation-evidence/invocation.json"),
        "generation_metrics": Path("/generation-evidence/metrics.json"),
        "generation_last": Path("/generation-evidence/codex-last.txt"),
        "generation_output": Path("/generation-evidence/codex-output.log"),
        "generation_prompt": Path("/generation-evidence/prompt.txt"),
        "generation_trace": Path("/generation-evidence/codex-trace"),
        "candidate": Path("/candidate"),
        "canonical": Path("/reference/canonical.py"),
        "trusted_prompt": Path("/reference/prompt.py"),
        "translator": Path("/reference/py2mpy.py"),
        "trusted_reference_semantics": Path("/reference/reference-semantics"),
    }
    for name, path in required.items():
        exists = path.exists()
        regular_kind = path.is_dir() if name in {
            "generation_trace", "candidate", "trusted_reference_semantics"
        } else path.is_file()
        not_link = not path.is_symlink()
        this_ok = exists and regular_kind and not_link
        print(
            f"required {name}: {'OK' if this_ok else 'BAD'} "
            f"path={path} exists={exists} expected_kind={regular_kind} symlink={path.is_symlink()}"
        )
        ok &= this_ok

    file_hash_checks = {
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    }
    for path, key in file_hash_checks.items():
        actual = sha256_file(path) if path.is_file() and not path.is_symlink() else None
        ok &= print_check(f"recorded file hash {path}", actual, audit["hashes"][key])

    exact_files = [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")),
    ]
    for candidate, trusted in exact_files:
        same = (
            candidate.is_file()
            and trusted.is_file()
            and not candidate.is_symlink()
            and not trusted.is_symlink()
            and candidate.read_bytes() == trusted.read_bytes()
        )
        print(f"byte identity {candidate} vs {trusted}: {'OK' if same else 'MISMATCH'}")
        ok &= same

    candidate_semantics = inventory(Path("/candidate/reference-semantics"))
    trusted_semantics = inventory(Path("/reference/reference-semantics"))
    added = sorted(candidate_semantics.keys() - trusted_semantics.keys())
    missing = sorted(trusted_semantics.keys() - candidate_semantics.keys())
    changed = sorted(
        key
        for key in candidate_semantics.keys() & trusted_semantics.keys()
        if candidate_semantics[key] != trusted_semantics[key]
    )
    print(
        "reference-semantics recursive comparison: "
        f"candidate_entries={len(candidate_semantics)} trusted_entries={len(trusted_semantics)} "
        f"added={len(added)} missing={len(missing)} changed_or_mistyped={len(changed)}"
    )
    if added:
        print(f"  added={added}")
    if missing:
        print(f"  missing={missing}")
    if changed:
        print(f"  changed_or_mistyped={changed}")
    semantics_ok = not added and not missing and not changed
    ok &= semantics_ok

    candidate_links = sorted(
        rel for rel, (kind, _) in inventory(Path("/candidate")).items() if kind == "symlink"
    )
    print(f"candidate symlink entries: {candidate_links}")
    ok &= not candidate_links

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_links = [str(path) for path in trace_files if path.is_symlink()]
    trace_nonfiles = [
        str(path) for path in trace_files if not path.is_dir() and not path.is_file()
    ]
    print(f"generation trace symlinks: {trace_links}")
    print(f"generation trace special entries: {trace_nonfiles}")
    ok &= not trace_links and not trace_nonfiles

    result = json.loads(Path("/generation-result.json").read_text())
    declared_outputs: dict[str, str] = result["outputs"]["evidence"]
    for rel, expected in sorted(declared_outputs.items()):
        path = Path("/generation-evidence") / rel
        actual = sha256_file(path) if path.is_file() and not path.is_symlink() else None
        ok &= print_check(f"generation-result evidence hash {rel}", actual, expected)

    # Parse every JSONL record rather than trusting a selected trace excerpt.
    jsonl_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    total_lines = 0
    type_counts: dict[str, int] = {}
    for path in jsonl_files:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total_lines += 1
                try:
                    record = json.loads(line)
                except Exception as error:
                    print(f"BAD JSONL {path}:{line_number}: {error}")
                    ok = False
                    continue
                record_type = str(record.get("type", "<missing>"))
                type_counts[record_type] = type_counts.get(record_type, 0) + 1
    print(
        f"structured trace parse: files={len(jsonl_files)} lines={total_lines} "
        f"top_level_type_counts={dict(sorted(type_counts.items()))}"
    )

    print(f"OVERALL: {'OK' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
