#!/usr/bin/env python3
"""Independent provenance and mounted-tree integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


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
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{stat.S_IFMT(mode):o}"


def tree_manifest(root: Path) -> tuple[str, list[str]]:
    """Hash an independently specified, path/type/mode/content tree manifest."""
    records: list[str] = []
    for path in sorted([root, *root.rglob("*")], key=lambda p: p.as_posix()):
        rel = "." if path == root else path.relative_to(root).as_posix()
        entry_kind = kind(path)
        mode = stat.S_IMODE(path.lstat().st_mode)
        if entry_kind == "file":
            payload = sha256(path)
        elif entry_kind == "symlink":
            payload = os.readlink(path)
        else:
            payload = "-"
        records.append(f"{entry_kind}\t{mode:04o}\t{rel}\t{payload}")
    encoded = ("\n".join(records) + "\n").encode()
    return hashlib.sha256(encoded).hexdigest(), records


def compare_trees(left: Path, right: Path) -> list[str]:
    left_entries = {
        ("." if p == left else p.relative_to(left).as_posix()): p
        for p in [left, *left.rglob("*")]
    }
    right_entries = {
        ("." if p == right else p.relative_to(right).as_posix()): p
        for p in [right, *right.rglob("*")]
    }
    issues: list[str] = []
    for rel in sorted(set(left_entries) | set(right_entries)):
        lp = left_entries.get(rel)
        rp = right_entries.get(rel)
        if lp is None:
            issues.append(f"candidate missing {rel}")
            continue
        if rp is None:
            issues.append(f"candidate additional {rel}")
            continue
        lk, rk = kind(lp), kind(rp)
        if lk != rk:
            issues.append(f"type mismatch {rel}: candidate={lk} trusted={rk}")
            continue
        if lk == "symlink":
            issues.append(f"symlinked semantics entry {rel}")
        elif lk == "file" and sha256(lp) != sha256(rp):
            issues.append(f"content mismatch {rel}: {sha256(lp)} != {sha256(rp)}")
    return issues


def show_hash_check(label: str, path: Path, expected: str | None) -> bool:
    actual = sha256(path)
    ok = expected == actual if expected is not None else True
    print(
        f"HASH {label}: type={kind(path)} size={path.stat().st_size} "
        f"actual={actual} expected={expected or 'not-recorded'} ok={ok}"
    )
    return ok


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(CAMPAIGN_LOCK.read_text())

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"problem_id={audit.get('problem_id')}")
    print(f"condition={audit.get('condition')}")

    if audit.get("audit_campaign") != lock:
        failures.append("audit_campaign object does not structurally equal campaign lock")
    print(f"campaign_structural_match={audit.get('audit_campaign') == lock}")
    if not show_hash_check(
        "audit_campaign_lock",
        CAMPAIGN_LOCK,
        audit["hashes"].get("audit_campaign_lock_sha256"),
    ):
        failures.append("campaign lock hash mismatch")

    required_mounts = {
        "audit-input": AUDIT_INPUT,
        "audit-campaign-lock": CAMPAIGN_LOCK,
        "run": Path("/run.json"),
        "task": Path("/task.json"),
        "generation-result": Path("/generation-result.json"),
        "candidate": Path(audit["container_paths"]["candidate"]),
        "canonical": Path(audit["container_paths"]["canonical"]),
        "trusted-prompt": Path(audit["container_paths"]["trusted_prompt"]),
        "translator": Path(audit["container_paths"]["translator"]),
        "generation-root": Path(audit["container_paths"]["generation_root"]),
        "generation-invocation": Path(audit["container_paths"]["generation_manifest"]),
        "generation-metrics": Path(audit["container_paths"]["generation_metrics"]),
        "generation-last": Path(audit["container_paths"]["generation_last"]),
        "generation-output": Path(audit["container_paths"]["generation_output"]),
        "generation-trace": Path(audit["container_paths"]["generation_trace"]),
        "generation-prompt": Path("/generation-evidence/prompt.txt"),
    }
    for label, path in required_mounts.items():
        exists = path.exists()
        readable = os.access(path, os.R_OK)
        entry_kind = kind(path) if exists or path.is_symlink() else "missing"
        print(f"MOUNT {label}: path={path} exists={exists} readable={readable} type={entry_kind}")
        if not exists or not readable:
            failures.append(f"required mount absent/unreadable: {label} {path}")

    if audit.get("record_layout") != "legacy-selected-stage1":
        failures.append(f"unexpected record layout {audit.get('record_layout')}")

    required_records = [
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        required_records.append(usage)
    for path in required_records:
        if not path.is_file() or path.is_symlink() or not os.access(path, os.R_OK):
            failures.append(f"required generation record invalid: {path}")
        print(
            f"RECORD {path}: exists={path.exists()} type="
            f"{kind(path) if path.exists() or path.is_symlink() else 'missing'}"
        )

    file_hash_checks = [
        ("canonical", Path("/reference/canonical.py"), "canonical_sha256"),
        ("trusted-prompt", Path("/reference/prompt.py"), "trusted_prompt_sha256"),
        ("trusted-translator", Path("/reference/py2mpy.py"), "trusted_translator_sha256"),
        ("candidate-prompt", Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
        ("candidate-translator", Path("/candidate/py2mpy.py"), "candidate_translator_sha256"),
        ("run", Path("/run.json"), "run_manifest_sha256"),
        ("task", Path("/task.json"), "task_manifest_sha256"),
        ("generation-result", Path("/generation-result.json"), "stage1_result_sha256"),
        (
            "generation-invocation",
            Path("/generation-evidence/invocation.json"),
            "stage1_invocation_sha256",
        ),
        ("generation-metrics", Path("/generation-evidence/metrics.json"), "generation_metrics_sha256"),
        ("generation-last", Path("/generation-evidence/codex-last.txt"), "generation_codex_last_sha256"),
        (
            "generation-output",
            Path("/generation-evidence/codex-output.log"),
            "generation_codex_output_sha256",
        ),
        ("generation-prompt", Path("/generation-evidence/prompt.txt"), "generation_prompt_sha256"),
    ]
    if usage.exists():
        file_hash_checks.append(
            ("generation-usage", usage, "generation_usage_sha256")
        )
    for label, path, key in file_hash_checks:
        if not show_hash_check(label, path, audit["hashes"].get(key)):
            failures.append(f"recorded hash mismatch for {label}")

    candidate = Path("/candidate")
    candidate_symlinks = [p.relative_to(candidate).as_posix() for p in candidate.rglob("*") if p.is_symlink()]
    print(f"candidate_symlinks={candidate_symlinks}")
    if candidate_symlinks:
        failures.append(f"candidate has symlinked entries: {candidate_symlinks}")

    required_candidate = [
        "prompt.py",
        "py2mpy.py",
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "reference-semantics",
    ]
    for rel in required_candidate:
        path = candidate / rel
        valid = path.exists() and not path.is_symlink()
        print(f"CANDIDATE_REQUIRED {rel}: valid={valid} type={kind(path) if path.exists() else 'missing'}")
        if not valid:
            failures.append(f"candidate required artifact missing/mistyped/symlinked: {rel}")

    if Path("/candidate/prompt.py").read_bytes() != Path("/reference/prompt.py").read_bytes():
        failures.append("candidate prompt differs from trusted prompt")
    if Path("/candidate/py2mpy.py").read_bytes() != Path("/reference/py2mpy.py").read_bytes():
        failures.append("candidate translator differs from trusted translator")
    print(
        "candidate_prompt_matches_trusted="
        f"{Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
    )
    print(
        "candidate_translator_matches_trusted="
        f"{Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
    )

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    mode_ok = audit.get("semantics_mode") == "SUPPLIED_SEMANTICS" and trusted_semantics.is_dir()
    print(f"semantics_mode_mount_consistent={mode_ok}")
    if not mode_ok:
        failures.append("semantics mode contradicts trusted reference-semantics mount")
    semantics_issues = compare_trees(candidate_semantics, trusted_semantics)
    print(f"semantics_recursive_issues={semantics_issues}")
    if semantics_issues:
        failures.extend(semantics_issues)

    for label, root in [
        ("candidate-reference-semantics", candidate_semantics),
        ("trusted-reference-semantics", trusted_semantics),
        ("candidate-full-tree", candidate),
    ]:
        digest, records = tree_manifest(root)
        print(f"TREE {label}: independent_manifest_sha256={digest} entries={len(records)}")
        for record in records:
            print(f"TREE_ENTRY {label}: {record}")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    output_hashes = generation_result["outputs"]["evidence"]
    invocation_hashes = invocation["outputs"]["evidence"]
    evidence_root = Path("/generation-evidence")
    for rel, expected in sorted(output_hashes.items()):
        path = evidence_root / rel
        if not path.is_file() or path.is_symlink():
            failures.append(f"generation-result evidence entry invalid: {rel}")
            continue
        actual = sha256(path)
        same_invocation = invocation_hashes.get(rel) == expected
        print(
            f"GEN_OUTPUT {rel}: actual={actual} result_expected={expected} "
            f"invocation_expected={invocation_hashes.get(rel)} "
            f"result_invocation_agree={same_invocation} ok={actual == expected and same_invocation}"
        )
        if actual != expected or not same_invocation:
            failures.append(f"generation output hash mismatch: {rel}")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [p for p in trace_files if p.is_file()]
    print(f"trace_files={[str(p) for p in trace_files]}")
    trace_counts: Counter[tuple[str | None, str | None]] = Counter()
    trace_lines = 0
    for path in trace_files:
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    event = json.loads(line)
                except Exception as err:
                    failures.append(f"invalid JSON trace line {path}:{line_number}: {err}")
                    continue
                payload = event.get("payload") or {}
                trace_counts[(event.get("type"), payload.get("type"))] += 1
    print(f"trace_lines_parsed={trace_lines}")
    for key, count in sorted(trace_counts.items(), key=lambda item: str(item[0])):
        print(f"TRACE_COUNT outer={key[0]} payload={key[1]} count={count}")

    for path in [
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
    ]:
        show_hash_check(f"candidate-source:{path.name}", path, None)

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
