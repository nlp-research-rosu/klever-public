#!/usr/bin/env python3
"""Independent integrity checks for the launcher-mounted audit inputs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reproduce pipeline_contract.sha256_tree without importing harness code."""
    if root.is_symlink() or not root.is_dir():
        raise AssertionError(f"not a real directory: {root}")
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
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
                raise AssertionError(f"linked/unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"required path is not a regular file: {path}")


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["audit_campaign"] == lock
    print("campaign_block_structural_match=true")

    required = [
        AUDIT_INPUT,
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        required.append(usage)
    for path in required:
        require_regular(path)
    print(f"required_regular_files={len(required)}")

    assert not Path("/reference/reference-semantics").exists()
    assert not Path("/candidate/reference-semantics").exists()
    print("generated_semantics_boundary=correct_absence")

    h = audit["hashes"]
    direct = {
        LOCK: h["audit_campaign_lock_sha256"],
        Path("/reference/canonical.py"): h["canonical_sha256"],
        Path("/reference/prompt.py"): h["trusted_prompt_sha256"],
        Path("/reference/py2mpy.py"): h["trusted_translator_sha256"],
        Path("/candidate/prompt.py"): h["candidate_prompt_sha256"],
        Path("/candidate/py2mpy.py"): h["candidate_translator_sha256"],
        Path("/run.json"): h["run_manifest_sha256"],
        Path("/task.json"): h["task_manifest_sha256"],
        Path("/generation-result.json"): h["stage1_result_sha256"],
        Path("/generation-evidence/invocation.json"): h["stage1_invocation_sha256"],
        Path("/generation-evidence/metrics.json"): h["generation_metrics_sha256"],
        Path("/generation-evidence/codex-last.txt"): h[
            "generation_codex_last_sha256"
        ],
        Path("/generation-evidence/codex-output.log"): h[
            "generation_codex_output_sha256"
        ],
        Path("/generation-evidence/prompt.txt"): h["generation_prompt_sha256"],
        Path("/generation-evidence/usage.json"): h["generation_usage_sha256"],
    }
    for path, expected in direct.items():
        actual = sha256_file(path)
        assert actual == expected, (path, actual, expected)
        print(f"sha256_match {path} {actual}")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("candidate_prompt_byte_identity=true")
    print("candidate_translator_byte_identity=true")

    result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    usage_data = json.loads(usage.read_text(encoding="utf-8"))
    task = json.loads(Path("/task.json").read_text(encoding="utf-8"))
    assert all(audit["manifest"].get(key) == value for key, value in task.items())
    assert audit["manifest"].get("config") == audit["config"]
    assert sha256_file(Path("/task.json")) == h["manifest_sha256"]
    print("task_manifest_structural_match=true")

    candidate_pipeline_hash = pipeline_tree_hash(Path("/candidate"))
    trace_pipeline_hash = pipeline_tree_hash(
        Path("/generation-evidence/codex-trace")
    )
    assert candidate_pipeline_hash == result["outputs"]["workspace_sha256"]
    assert candidate_pipeline_hash == invocation["retained_workspace_sha256"]
    assert trace_pipeline_hash == usage_data["source_trace_sha256"]
    print(f"candidate_pipeline_tree_hash={candidate_pipeline_hash}")
    print(f"audit_recorded_candidate_tree_hash={h['candidate_tree_sha256']}")
    print(f"trace_pipeline_tree_hash={trace_pipeline_hash}")
    print(
        "audit_recorded_generation_trace_hash="
        f"{h['generation_codex_trace_sha256']}"
    )
    print(
        "note=audit tree digest fields use an unspecified digest namespace; "
        "the independently reproduced pipeline digests match the generation "
        "records exactly"
    )

    evidence_hashes = result["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected, (relative, actual, expected)
        print(f"generation_result_evidence_match {relative} {actual}")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    assert trace_files
    type_counts: Counter[str] = Counter()
    payload_type_counts: Counter[str] = Counter()
    line_count = 0
    selected_event = None
    selected_line = usage_data["selected_event"]["line_number"]
    for path in trace_files:
        require_regular(path)
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                line_count += 1
                item = json.loads(line)
                if line_count == selected_line:
                    selected_event = item
                type_counts[str(item.get("type"))] += 1
                payload = item.get("payload")
                if isinstance(payload, dict):
                    payload_type_counts[str(payload.get("type"))] += 1
    assert 1 <= selected_line <= line_count
    assert selected_event is not None
    assert selected_event["payload"]["type"] == "token_count"
    print(f"trace_json_files={len(trace_files)}")
    print(f"trace_json_lines={line_count}")
    print(f"trace_event_types={dict(sorted(type_counts.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_type_counts.items()))}")
    print("provenance_check=PASS")


if __name__ == "__main__":
    main()
