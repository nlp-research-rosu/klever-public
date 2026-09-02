#!/usr/bin/env python3
"""Independent mounted-input and legacy-selected-stage1 integrity audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def entry_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{stat.S_IFMT(mode):o}"


def walk_tree(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        names = sorted(dirs + files)
        for name in names:
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            kind = entry_kind(path)
            result[rel] = (kind, sha256(path) if kind == "file" else None)
    return result


def manifest_digest(tree: dict[str, tuple[str, str | None]]) -> str:
    """Reviewer-defined canonical digest, explicitly not launcher-specific."""
    digest = hashlib.sha256()
    for rel, (kind, content_hash) in sorted(tree.items()):
        digest.update(f"{kind}\0{rel}\0{content_hash or ''}\n".encode())
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement the recorded pipeline-v2 workspace/tree hash algorithm."""
    entries: list[tuple[str, str, Path]] = []
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in dirs + files:
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            kind = entry_kind(path)
            if kind not in {"directory", "file"}:
                raise ValueError(f"unsupported tree entry {path}: {kind}")
            entries.append((rel, kind, path))
    digest = hashlib.sha256()
    for rel, kind, path in sorted(entries):
        encoded = rel.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat().st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT.read_text())
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    if audit.get("record_layout") != "legacy-selected-stage1":
        failures.append("unexpected record layout")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("unexpected semantics mode")

    required = [
        Path("/audit-input.json"),
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/codex-trace"),
        Path("/candidate"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/reference/reference-semantics"),
    ]
    for path in required:
        exists = path.exists()
        readable = os.access(path, os.R_OK)
        kind = entry_kind(path) if exists or path.is_symlink() else "missing"
        print(f"required {path}: kind={kind} readable={readable}")
        if not exists or not readable:
            failures.append(f"missing/unreadable required path {path}")

    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    print(f"campaign_block_equal={lock == audit.get('audit_campaign')}")
    if lock != audit.get("audit_campaign"):
        failures.append("campaign lock content differs from audit campaign block")

    expected_hashes = audit["hashes"]
    direct_hashes = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "manifest_sha256": Path("/task.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    }
    for key, path in direct_hashes.items():
        actual = sha256(path)
        expected = expected_hashes.get(key)
        ok = actual == expected
        print(f"hash {key}: actual={actual} expected={expected} match={ok}")
        if not ok:
            failures.append(f"hash mismatch: {key}")

    result = json.loads(Path("/generation-result.json").read_text())
    for rel, expected in sorted(result["outputs"]["evidence"].items()):
        path = Path("/generation-evidence") / rel
        kind = entry_kind(path) if path.exists() else "missing"
        actual = sha256(path) if kind == "file" else None
        ok = kind == "file" and actual == expected
        print(
            f"generation-result evidence {rel}: kind={kind} actual={actual} "
            f"expected={expected} match={ok}"
        )
        if not ok:
            failures.append(f"generation evidence mismatch: {rel}")

    for path in [
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/generation-evidence"),
    ]:
        links = [p for p in path.rglob("*") if p.is_symlink()]
        print(f"symlinks under {path}: {[str(p) for p in links]}")
        if links:
            failures.append(f"symlink(s) found under {path}")

    trusted_semantics = walk_tree(Path("/reference/reference-semantics"))
    candidate_semantics = walk_tree(Path("/candidate/reference-semantics"))
    missing = sorted(set(trusted_semantics) - set(candidate_semantics))
    additional = sorted(set(candidate_semantics) - set(trusted_semantics))
    changed = sorted(
        rel
        for rel in set(trusted_semantics) & set(candidate_semantics)
        if trusted_semantics[rel] != candidate_semantics[rel]
    )
    print(f"semantics_missing={missing}")
    print(f"semantics_additional={additional}")
    print(f"semantics_changed_or_mistyped={changed}")
    print(
        "reviewer_manifest_digest trusted_semantics="
        + manifest_digest(trusted_semantics)
    )
    print(
        "reviewer_manifest_digest candidate_semantics="
        + manifest_digest(candidate_semantics)
    )
    if missing or additional or changed:
        failures.append("candidate semantics tree differs from trusted tree")

    pipeline_tree_checks = [
        (
            "candidate_workspace",
            Path("/candidate"),
            result["outputs"]["workspace_sha256"],
        ),
        (
            "trusted_semantics_manifest",
            Path("/reference/reference-semantics"),
            expected_hashes["trusted_reference_semantics_manifest_sha256"],
        ),
        (
            "candidate_semantics_manifest",
            Path("/candidate/reference-semantics"),
            expected_hashes["trusted_reference_semantics_manifest_sha256"],
        ),
        (
            "generation_trace_source",
            Path("/generation-evidence/codex-trace"),
            json.loads(Path("/generation-evidence/usage.json").read_text())[
                "source_trace_sha256"
            ],
        ),
    ]
    for label, path, expected in pipeline_tree_checks:
        actual = pipeline_tree_digest(path)
        ok = actual == expected
        print(
            f"pipeline_tree_hash {label}: actual={actual} expected={expected} "
            f"match={ok}"
        )
        if not ok:
            failures.append(f"pipeline tree hash mismatch: {label}")

    prompt_equal = Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    translator_equal = Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print(f"candidate_prompt_byte_equal={prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    if not prompt_equal or not translator_equal:
        failures.append("candidate prompt or translator differs from trusted")

    # Read and parse every JSONL trace record, not merely its beginning or end.
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    print(f"trace_files={[str(path) for path in trace_files]}")
    trace_types: Counter[str] = Counter()
    trace_lines = 0
    trace_parse_failures: list[str] = []
    for path in trace_files:
        print(f"trace_file_sha256 {path}={sha256(path)}")
        with path.open(errors="replace") as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    item = json.loads(line)
                    trace_types[str(item.get("type", "<missing>"))] += 1
                except Exception as err:  # evidence is untrusted
                    trace_parse_failures.append(f"{path}:{line_number}: {err}")
    print(f"trace_line_count={trace_lines}")
    print(f"trace_top_level_types={dict(sorted(trace_types.items()))}")
    print(f"trace_parse_failures={trace_parse_failures}")
    if trace_parse_failures:
        failures.append("structured trace contains malformed JSONL")

    # Read all bytes/lines of the untrusted text log and report bounded metadata.
    log_path = Path("/generation-evidence/codex-output.log")
    log_text = log_path.read_text(errors="replace")
    print(f"codex_output_line_count={len(log_text.splitlines())}")
    for token in [
        "#Top",
        "WarnStuckClaimState",
        "KPROVE_PASSED",
        "timed out",
        "Traceback",
        "[Error]",
    ]:
        print(f"codex_output_count {token!r}={log_text.count(token)}")
    last_path = Path("/generation-evidence/codex-last.txt")
    print(f"codex_last_line_count={len(last_path.read_text(errors='replace').splitlines())}")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
