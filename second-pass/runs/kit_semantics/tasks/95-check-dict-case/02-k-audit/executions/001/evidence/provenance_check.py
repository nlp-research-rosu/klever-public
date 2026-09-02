#!/usr/bin/env python3
"""Independent integrity checks for audit record 95-check-dict-case."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular_nonsymlink(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode) and not stat.S_ISLNK(mode)


def tree_manifest(root: Path) -> tuple[list[dict[str, object]], str]:
    entries: list[dict[str, object]] = []
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            kind = "symlink"
            content = os.readlink(path)
        elif stat.S_ISDIR(mode):
            kind = "directory"
            content = None
        elif stat.S_ISREG(mode):
            kind = "file"
            content = sha256(path)
        else:
            kind = "other"
            content = None
        entries.append(
            {
                "path": rel,
                "kind": kind,
                "sha256_or_target": content,
                "size": path.lstat().st_size,
            }
        )
    encoded = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return entries, hashlib.sha256(encoded).hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the mounted pipeline-v3 tree digest from pipeline_contract.py."""
    entries = []
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        rel = path.relative_to(root).as_posix()
        if stat.S_ISDIR(mode):
            entries.append((rel, "directory", path))
        elif stat.S_ISREG(mode):
            entries.append((rel, "file", path))
        else:
            raise RuntimeError(f"linked or unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for rel, kind, path in sorted(entries):
        encoded = rel.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.lstat().st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    hashes = audit["hashes"]
    paths = {key: Path(value) for key, value in audit["container_paths"].items()}
    checks: list[tuple[str, bool, str]] = []

    checks.append(("record layout pipeline-v3", audit["record_layout"] == "pipeline-v3", audit["record_layout"]))
    checks.append(
        (
            "semantics mode supplied",
            audit["semantics_mode"] == "SUPPLIED_SEMANTICS",
            audit["semantics_mode"],
        )
    )

    required = [
        Path("/audit-input.json"),
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    required.extend(trace_files)
    for path in required:
        checks.append((f"regular non-symlink {path}", regular_nonsymlink(path), str(path)))

    direct_hashes = {
        Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
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
        Path("/generation-evidence/runtime-metrics.json"): "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    for path, field in direct_hashes.items():
        actual = sha256(path)
        expected = hashes[field]
        checks.append((f"recorded SHA-256 {path}", actual == expected, f"actual={actual} expected={expected}"))

    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    checks.append(
        (
            "campaign lock equals embedded audit_campaign block",
            lock == audit["audit_campaign"],
            f"lock_campaign={lock.get('campaign_id')}",
        )
    )

    checks.append(
        (
            "candidate prompt byte-identical to trusted prompt",
            Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes(),
            "",
        )
    )
    checks.append(
        (
            "candidate translator byte-identical to trusted translator",
            Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes(),
            "",
        )
    )

    candidate_entries, candidate_tree_hash = tree_manifest(Path("/candidate/reference-semantics"))
    trusted_entries, trusted_tree_hash = tree_manifest(Path("/reference/reference-semantics"))
    checks.append(
        (
            "candidate supplied-semantics tree type/path/content identity",
            candidate_entries == trusted_entries,
            f"independent_manifest_sha256 candidate={candidate_tree_hash} trusted={trusted_tree_hash}",
        )
    )
    checks.append(
        (
            "candidate supplied-semantics has no symlinks/other entries",
            all(entry["kind"] in {"directory", "file"} for entry in candidate_entries),
            f"entries={len(candidate_entries)}",
        )
    )
    candidate_pipeline_hash = pipeline_tree_sha256(Path("/candidate"))
    generation_result = json.loads(Path("/generation-result.json").read_text())
    checks.append(
        (
            "mounted candidate pipeline tree hash equals stage-1 output workspace hash",
            candidate_pipeline_hash == generation_result["outputs"]["workspace_sha256"],
            f"actual={candidate_pipeline_hash} "
            f"expected={generation_result['outputs']['workspace_sha256']}",
        )
    )
    semantics_pipeline_hash = pipeline_tree_sha256(Path("/reference/reference-semantics"))
    checks.append(
        (
            "trusted semantics pipeline tree hash equals launcher manifest hash",
            semantics_pipeline_hash == hashes["trusted_reference_semantics_manifest_sha256"],
            f"actual={semantics_pipeline_hash} "
            f"expected={hashes['trusted_reference_semantics_manifest_sha256']}",
        )
    )

    proof_artifacts = [
        "solution.py",
        "solution.mpy",
        "spec.k",
        "verification.k",
        "proof-theory.k",
        "connection.k",
        "connection-spec.k",
    ]
    for name in proof_artifacts:
        path = Path("/candidate") / name
        checks.append((f"candidate proof artifact {name}", regular_nonsymlink(path), str(path)))

    trace_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    trace_lines = 0
    for trace in trace_files:
        expected = json.loads(Path("/generation-result.json").read_text())["outputs"]["evidence"].get(
            str(trace.relative_to("/generation-evidence"))
        )
        if expected:
            actual = sha256(trace)
            checks.append(
                (
                    f"recorded SHA-256 {trace}",
                    actual == expected,
                    f"actual={actual} expected={expected}",
                )
            )
        with trace.open() as stream:
            for line in stream:
                trace_lines += 1
                event = json.loads(line)
                event_type = str(event.get("type", "<missing>"))
                trace_types[event_type] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    subtype = payload.get("type")
                    if subtype is not None:
                        payload_types[str(subtype)] += 1
                    if subtype in {"function_call", "custom_tool_call"}:
                        tool_names[str(payload.get("name", "<missing>"))] += 1

    output_path = Path("/generation-evidence/codex-output.log")
    output_lines = 0
    keyword_counts = collections.Counter()
    with output_path.open(errors="replace") as stream:
        for line in stream:
            output_lines += 1
            for keyword in ("kprove", "kompile", "#Top", "WarnStuckClaimState", "FAILED", "ERROR"):
                if keyword in line:
                    keyword_counts[keyword] += 1
    trace_pipeline_hash = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    checks.append(
        (
            "structured-trace tree hash equals usage source trace hash",
            trace_pipeline_hash == usage["source_trace_sha256"],
            f"actual={trace_pipeline_hash} expected={usage['source_trace_sha256']}",
        )
    )

    print("INDEPENDENT PROVENANCE CHECK")
    for label, passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL'} | {label} | {detail}")
    print(f"TRACE_FILES: {len(trace_files)}")
    print(f"TRACE_LINES_PARSED: {trace_lines}")
    print(f"TRACE_EVENT_TYPES: {dict(sorted(trace_types.items()))}")
    print(f"TRACE_PAYLOAD_TYPES: {dict(sorted(payload_types.items()))}")
    print(f"TRACE_TOOL_NAMES: {dict(sorted(tool_names.items()))}")
    print(f"CODEX_OUTPUT_LINES_SCANNED: {output_lines}")
    print(f"CODEX_OUTPUT_KEYWORD_COUNTS: {dict(sorted(keyword_counts.items()))}")
    print(
        "LAUNCHER_OPAQUE_HASH_FIELDS: "
        f"candidate_tree_sha256={hashes['candidate_tree_sha256']} "
        f"candidate_reference_semantics_sha256="
        f"{hashes['candidate_reference_semantics_sha256']}"
    )
    failures = sum(not passed for _, passed, _ in checks)
    print(f"FAILURES: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
