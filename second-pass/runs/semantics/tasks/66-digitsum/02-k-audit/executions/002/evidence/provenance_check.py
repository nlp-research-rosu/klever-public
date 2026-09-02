#!/usr/bin/env python3
"""Independent launcher/provenance integrity checks for the 66-digitsum audit."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GEN = Path("/generation-evidence")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{mode:o}"


def compare_trees(left: Path, right: Path) -> tuple[list[str], str]:
    problems: list[str] = []
    rows: list[str] = []
    left_entries = {
        p.relative_to(left).as_posix(): p
        for p in left.rglob("*")
    }
    right_entries = {
        p.relative_to(right).as_posix(): p
        for p in right.rglob("*")
    }
    for rel in sorted(set(left_entries) | set(right_entries)):
        lp = left_entries.get(rel)
        rp = right_entries.get(rel)
        if lp is None:
            problems.append(f"missing candidate entry: {rel}")
            continue
        if rp is None:
            problems.append(f"additional candidate entry: {rel}")
            continue
        lk, rk = kind(lp), kind(rp)
        if lk != rk:
            problems.append(f"type mismatch {rel}: candidate={lk}, trusted={rk}")
            continue
        if lk == "symlink":
            problems.append(f"symlink forbidden: {rel}")
            continue
        if lk == "file":
            lh, rh = sha256(lp), sha256(rp)
            rows.append(f"F\\0{rel}\\0{lh}")
            if lh != rh:
                problems.append(f"content mismatch: {rel}")
        elif lk == "directory":
            rows.append(f"D\\0{rel}")
    manifest_digest = hashlib.sha256("\n".join(rows).encode()).hexdigest()
    return problems, manifest_digest


def main() -> int:
    print("COMMAND: python3 /audit-output/evidence/provenance_check.py")
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_json_equal={audit['audit_campaign'] == lock}")
    print(f"audit_campaign_lock_sha256={sha256(LOCK)}")
    print(
        "audit_campaign_lock_recorded="
        f"{audit['hashes']['audit_campaign_lock_sha256']}"
    )

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GEN / "invocation.json",
        GEN / "metrics.json",
        GEN / "codex-last.txt",
        GEN / "codex-output.log",
        GEN / "prompt.txt",
        GEN / "codex-trace",
    ]
    for path in required:
        print(
            f"required {path}: exists={path.exists()} readable={os.access(path, os.R_OK)} "
            f"kind={kind(path) if path.exists() else 'absent'}"
        )
    usage = GEN / "usage.json"
    print(
        f"optional-present usage {usage}: exists={usage.exists()} "
        f"kind={kind(usage) if usage.exists() else 'absent'}"
    )

    recorded_file_hashes = {
        "audit_campaign_lock_sha256": LOCK,
        "candidate_prompt_sha256": CANDIDATE / "prompt.py",
        "candidate_translator_sha256": CANDIDATE / "py2mpy.py",
        "canonical_sha256": REFERENCE / "canonical.py",
        "generation_codex_last_sha256": GEN / "codex-last.txt",
        "generation_codex_output_sha256": GEN / "codex-output.log",
        "generation_metrics_sha256": GEN / "metrics.json",
        "generation_prompt_sha256": GEN / "prompt.txt",
        "generation_usage_sha256": GEN / "usage.json",
        "run_manifest_sha256": Path("/run.json"),
        "stage1_invocation_sha256": GEN / "invocation.json",
        "stage1_result_sha256": Path("/generation-result.json"),
        "task_manifest_sha256": Path("/task.json"),
        "trusted_prompt_sha256": REFERENCE / "prompt.py",
        "trusted_translator_sha256": REFERENCE / "py2mpy.py",
    }
    mismatch_count = 0
    for field, path in recorded_file_hashes.items():
        actual = sha256(path)
        expected = audit["hashes"][field]
        ok = actual == expected
        mismatch_count += not ok
        print(f"hash {field}: ok={ok} actual={actual} expected={expected}")

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads((GEN / "invocation.json").read_text())
    for source, record in [
        ("generation-result", result["outputs"]["evidence"]),
        ("invocation", invocation["outputs"]["evidence"]),
    ]:
        for rel, expected in sorted(record.items()):
            path = GEN / rel
            actual = sha256(path)
            ok = actual == expected
            mismatch_count += not ok
            print(
                f"{source} evidence hash {rel}: ok={ok} "
                f"actual={actual} expected={expected}"
            )

    print(
        "candidate_prompt_byte_equal="
        f"{(CANDIDATE / 'prompt.py').read_bytes() == (REFERENCE / 'prompt.py').read_bytes()}"
    )
    print(
        "candidate_translator_byte_equal="
        f"{(CANDIDATE / 'py2mpy.py').read_bytes() == (REFERENCE / 'py2mpy.py').read_bytes()}"
    )

    semantics = REFERENCE / "reference-semantics"
    candidate_semantics = CANDIDATE / "reference-semantics"
    print(
        f"trusted_semantics_present={semantics.is_dir()} "
        f"trusted_semantics_kind={kind(semantics)}"
    )
    tree_problems, tree_digest = compare_trees(candidate_semantics, semantics)
    print(f"semantics_independent_manifest_sha256={tree_digest}")
    print(f"semantics_tree_problem_count={len(tree_problems)}")
    for problem in tree_problems:
        print(f"semantics_tree_problem={problem}")

    candidate_symlinks = [
        p.relative_to(CANDIDATE).as_posix()
        for p in CANDIDATE.rglob("*")
        if p.is_symlink()
    ]
    print(f"candidate_symlink_count={len(candidate_symlinks)}")
    for rel in candidate_symlinks:
        print(f"candidate_symlink={rel}")

    trace_files = sorted((GEN / "codex-trace").rglob("*"))
    trace_files = [p for p in trace_files if p.is_file()]
    print(f"trace_file_count={len(trace_files)}")
    for path in trace_files:
        print(f"trace_file {path.relative_to(GEN)} sha256={sha256(path)}")
    parse_errors = 0
    outer_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    trace_lines = 0
    for path in trace_files:
        with path.open(encoding="utf-8") as stream:
            for lineno, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as err:
                    parse_errors += 1
                    print(f"trace_parse_error={path}:{lineno}:{err}")
                    continue
                outer_types[str(event.get("type"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
    print(f"trace_lines={trace_lines}")
    print(f"trace_parse_errors={parse_errors}")
    print(f"trace_outer_types={dict(sorted(outer_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    print(f"recorded_file_hash_mismatches={mismatch_count}")
    ok = (
        audit["record_layout"] == "legacy-selected-stage1"
        and audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
        and audit["audit_campaign"] == lock
        and mismatch_count == 0
        and not tree_problems
        and not candidate_symlinks
        and not parse_errors
        and all(path.exists() and os.access(path, os.R_OK) for path in required)
    )
    print(f"OVERALL_PROVENANCE_CHECK={'PASS' if ok else 'FAIL'}")
    print(f"EXIT_STATUS={0 if ok else 1}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
