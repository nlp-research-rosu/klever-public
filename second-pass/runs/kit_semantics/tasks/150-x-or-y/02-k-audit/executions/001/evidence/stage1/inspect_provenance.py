#!/usr/bin/env python3
"""Independent pipeline-v3 mount, hash, and structured-trace inspection."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"tree root is not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise ValueError(f"linked or unsupported tree entry: {path}")
    return sorted(entries)


def sha256_tree(root: Path) -> str:
    """Launcher pipeline_contract.sha256_tree algorithm."""
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def tree_digest(root: Path) -> str:
    """Launcher export/content-tree algorithm used by audit-input tree fields."""
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def regular(path: Path) -> bool:
    return path.exists() and path.is_file() and not path.is_symlink()


def report_hash(label: str, path: Path, expected: str) -> bool:
    actual = sha256_file(path)
    ok = actual == expected
    print(f"HASH {label}: ok={ok} actual={actual} expected={expected} path={path}")
    return ok


def main() -> int:
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())
    hashes = audit["hashes"]
    container = audit["container_paths"]
    failures: list[str] = []

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_block_equals_lock={audit['audit_campaign'] == lock}")
    if audit["audit_campaign"] != lock:
        failures.append("campaign block mismatch")
    if not report_hash(
        "audit_campaign_lock",
        LOCK,
        hashes["audit_campaign_lock_sha256"],
    ):
        failures.append("campaign lock hash mismatch")

    required_files = {
        "audit_input": AUDIT,
        "audit_campaign_lock": LOCK,
        "run_manifest": Path(container["run_manifest"]),
        "task_manifest": Path(container["task_manifest"]),
        "stage1_result": Path(container["stage1_result"]),
        "generation_manifest": Path(container["generation_manifest"]),
        "generation_metrics": Path(container["generation_metrics"]),
        "runtime_metrics": Path(container["generation_root"]) / "runtime-metrics.json",
        "usage": Path(container["generation_root"]) / "usage.json",
        "generation_last": Path(container["generation_last"]),
        "generation_output": Path(container["generation_output"]),
        "generation_prompt": Path(container["generation_root"]) / "prompt.txt",
        "canonical": Path(container["canonical"]),
        "trusted_prompt": Path(container["trusted_prompt"]),
        "translator": Path(container["translator"]),
    }
    required_dirs = {
        "candidate": Path(container["candidate"]),
        "generation_root": Path(container["generation_root"]),
        "generation_trace": Path(container["generation_trace"]),
        "trusted_reference_semantics": Path("/reference/reference-semantics"),
    }
    for label, path in required_files.items():
        ok = regular(path)
        print(f"TYPE {label}: regular_no_symlink={ok} path={path}")
        if not ok:
            failures.append(f"bad required file {label}")
    for label, path in required_dirs.items():
        ok = path.is_dir() and not path.is_symlink()
        print(f"TYPE {label}: directory_no_symlink={ok} path={path}")
        if not ok:
            failures.append(f"bad required directory {label}")

    file_hash_cases = [
        ("run_manifest", Path("/run.json"), "run_manifest_sha256"),
        ("task_manifest", Path("/task.json"), "task_manifest_sha256"),
        ("stage1_result", Path("/generation-result.json"), "stage1_result_sha256"),
        (
            "generation_invocation",
            Path("/generation-evidence/invocation.json"),
            "stage1_invocation_sha256",
        ),
        (
            "generation_metrics",
            Path("/generation-evidence/metrics.json"),
            "generation_metrics_sha256",
        ),
        (
            "generation_runtime_metrics",
            Path("/generation-evidence/runtime-metrics.json"),
            "generation_runtime_metrics_sha256",
        ),
        (
            "generation_usage",
            Path("/generation-evidence/usage.json"),
            "generation_usage_sha256",
        ),
        (
            "generation_last",
            Path("/generation-evidence/codex-last.txt"),
            "generation_codex_last_sha256",
        ),
        (
            "generation_output",
            Path("/generation-evidence/codex-output.log"),
            "generation_codex_output_sha256",
        ),
        (
            "generation_prompt",
            Path("/generation-evidence/prompt.txt"),
            "generation_prompt_sha256",
        ),
        ("canonical", Path("/reference/canonical.py"), "canonical_sha256"),
        ("trusted_prompt", Path("/reference/prompt.py"), "trusted_prompt_sha256"),
        (
            "trusted_translator",
            Path("/reference/py2mpy.py"),
            "trusted_translator_sha256",
        ),
        ("candidate_prompt", Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
        (
            "candidate_translator",
            Path("/candidate/py2mpy.py"),
            "candidate_translator_sha256",
        ),
    ]
    for label, path, key in file_hash_cases:
        if not report_hash(label, path, hashes[key]):
            failures.append(f"hash mismatch {label}")

    opaque_recorded_tree_fields = [
        (
            "candidate",
            Path("/candidate"),
            hashes["candidate_tree_sha256"],
        ),
        (
            "generation_trace",
            Path("/generation-evidence/codex-trace"),
            hashes["generation_codex_trace_sha256"],
        ),
        (
            "trusted_reference_semantics",
            Path("/reference/reference-semantics"),
            hashes["trusted_reference_semantics_sha256"],
        ),
        (
            "candidate_reference_semantics",
            Path("/candidate/reference-semantics"),
            hashes["candidate_reference_semantics_sha256"],
        ),
    ]
    for label, path, expected in opaque_recorded_tree_fields:
        actual = tree_digest(path)
        print(
            f"OPAQUE_RECORDED_TREE_FIELD {label}: recorded={expected} "
            f"independent_content_digest={actual}"
        )

    manifest_cases = [
        (
            "candidate_workspace",
            Path("/candidate"),
            result_workspace
            if (result_workspace := json.loads(
                Path("/generation-result.json").read_text()
            )["outputs"]["workspace_sha256"])
            else "",
        ),
        (
            "generation_trace_manifest",
            Path("/generation-evidence/codex-trace"),
            json.loads(Path("/generation-evidence/usage.json").read_text())[
                "source_trace_sha256"
            ],
        ),
        (
            "trusted_reference_semantics_manifest",
            Path("/reference/reference-semantics"),
            hashes["trusted_reference_semantics_manifest_sha256"],
        ),
    ]
    for label, path, expected in manifest_cases:
        actual = sha256_tree(path)
        ok = actual == expected
        print(f"TREE_MANIFEST {label}: ok={ok} actual={actual} expected={expected}")
        if not ok:
            failures.append(f"tree manifest mismatch {label}")

    prompt_equal = (
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes()
    )
    translator_equal = (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    print(f"candidate_prompt_byte_equal={prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    if not prompt_equal:
        failures.append("candidate prompt differs")
    if not translator_equal:
        failures.append("candidate translator differs")

    trusted = {
        (relative, kind): path
        for relative, kind, path in tree_entries(Path("/reference/reference-semantics"))
    }
    candidate = {
        (relative, kind): path
        for relative, kind, path in tree_entries(Path("/candidate/reference-semantics"))
    }
    key_equal = trusted.keys() == candidate.keys()
    differing = [
        relative
        for (relative, kind), trusted_path in trusted.items()
        if kind == "file"
        and (relative, kind) in candidate
        and trusted_path.read_bytes() != candidate[(relative, kind)].read_bytes()
    ]
    print(f"semantics_entry_sets_equal={key_equal}")
    print(f"semantics_differing_file_count={len(differing)}")
    if differing:
        print("semantics_differing_files=" + ",".join(differing))
    if not key_equal or differing:
        failures.append("candidate semantics integrity mismatch")

    proof_required = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    for relative in proof_required:
        path = Path("/candidate") / relative
        ok = regular(path)
        print(f"PROOF_ARTIFACT {relative}: regular_no_symlink={ok}")
        if not ok:
            failures.append(f"missing or mistyped proof artifact {relative}")

    result = json.loads(Path("/generation-result.json").read_text())
    for relative, expected in result["outputs"]["evidence"].items():
        path = Path("/generation-evidence") / relative
        ok_type = regular(path)
        actual = sha256_file(path) if ok_type else "N/A"
        ok = ok_type and actual == expected
        print(
            f"GEN_RESULT_EVIDENCE {relative}: ok={ok} "
            f"regular_no_symlink={ok_type} actual={actual} expected={expected}"
        )
        if not ok:
            failures.append(f"generation-result evidence mismatch {relative}")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    trace_lines = 0
    malformed = 0
    for trace_file in trace_files:
        with trace_file.open() as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    malformed += 1
                    print(f"MALFORMED_TRACE {trace_file}:{line_number}")
                    continue
                top_types[str(item.get("type"))] += 1
                payload = item.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
    print(f"trace_file_count={len(trace_files)}")
    print(f"trace_line_count={trace_lines}")
    print(f"trace_malformed_count={malformed}")
    print(f"trace_top_types={dict(sorted(top_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    if not trace_files or malformed:
        failures.append("missing or malformed structured trace")

    output = Path("/generation-evidence/codex-output.log").read_text(errors="replace")
    print(f"codex_output_line_count={len(output.splitlines())}")
    for needle in [
        "#Top",
        "WarnStuckClaimState",
        "RESULT: KPROVE_PASSED",
        "VALIDATED",
    ]:
        print(f"codex_output_count[{needle}]={output.count(needle)}")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
