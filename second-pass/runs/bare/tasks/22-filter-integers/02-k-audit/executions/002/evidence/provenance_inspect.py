#!/usr/bin/env python3
"""Independent, read-only audit of mounted provenance inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reproduce the pipeline-v2 length-delimited tree digest."""
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
                raise RuntimeError(f"unsupported or linked entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode) or path.is_symlink():
        raise RuntimeError(f"not a non-symlink regular file: {path}")


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit_input = json.loads(AUDIT_INPUT.read_text())
    hashes = audit_input["hashes"]
    paths = audit_input["container_paths"]

    required_regular = {
        "audit_input": AUDIT_INPUT,
        "audit_campaign_lock": Path(paths["audit_campaign_lock"]),
        "run_manifest": Path(paths["run_manifest"]),
        "task_manifest": Path(paths["task_manifest"]),
        "stage1_result": Path(paths["stage1_result"]),
        "stage1_invocation": Path(paths["generation_manifest"]),
        "generation_metrics": Path(paths["generation_metrics"]),
        "generation_last": Path(paths["generation_last"]),
        "generation_output": Path(paths["generation_output"]),
        "generation_prompt": Path(paths["generation_root"]) / "prompt.txt",
        "generation_usage": Path(paths["generation_root"]) / "usage.json",
        "canonical": Path(paths["canonical"]),
        "trusted_prompt": Path(paths["trusted_prompt"]),
        "trusted_translator": Path(paths["translator"]),
        "candidate_prompt": Path(paths["candidate"]) / "prompt.py",
        "candidate_translator": Path(paths["candidate"]) / "py2mpy.py",
    }
    for label, path in required_regular.items():
        require_regular(path)
        print(f"TYPE {label}: regular non-symlink {path}")

    expected_hashes = {
        "audit_campaign_lock": "audit_campaign_lock_sha256",
        "run_manifest": "run_manifest_sha256",
        "task_manifest": "task_manifest_sha256",
        "stage1_result": "stage1_result_sha256",
        "stage1_invocation": "stage1_invocation_sha256",
        "generation_metrics": "generation_metrics_sha256",
        "generation_last": "generation_codex_last_sha256",
        "generation_output": "generation_codex_output_sha256",
        "generation_prompt": "generation_prompt_sha256",
        "generation_usage": "generation_usage_sha256",
        "canonical": "canonical_sha256",
        "trusted_prompt": "trusted_prompt_sha256",
        "trusted_translator": "trusted_translator_sha256",
        "candidate_prompt": "candidate_prompt_sha256",
        "candidate_translator": "candidate_translator_sha256",
    }
    for label, hash_key in expected_hashes.items():
        actual = sha256_file(required_regular[label])
        expected = hashes[hash_key]
        print(
            f"HASH {label}: actual={actual} expected={expected} "
            f"match={actual == expected}"
        )
        if actual != expected:
            raise RuntimeError(f"hash mismatch for {label}")

    lock = json.loads(required_regular["audit_campaign_lock"].read_text())
    print(f"CAMPAIGN_BLOCK_MATCH={lock == audit_input['audit_campaign']}")
    if lock != audit_input["audit_campaign"]:
        raise RuntimeError("audit campaign lock differs from audit-input block")

    candidate = Path(paths["candidate"])
    trace_root = Path(paths["generation_trace"])
    if candidate.is_symlink() or not candidate.is_dir():
        raise RuntimeError("candidate root is not a real directory")
    if trace_root.is_symlink() or not trace_root.is_dir():
        raise RuntimeError("trace root is not a real directory")
    reference_semantics = Path("/reference/reference-semantics")
    print(f"GENERATED_SEMANTICS_REFERENCE_ABSENT={not reference_semantics.exists()}")
    if reference_semantics.exists():
        raise RuntimeError("forbidden reference semantics mount exists")

    candidate_entries: list[str] = []
    for path in sorted(candidate.rglob("*")):
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            kind = "symlink"
        elif stat.S_ISREG(mode):
            kind = "file"
        elif stat.S_ISDIR(mode):
            kind = "directory"
        else:
            kind = "unsupported"
        candidate_entries.append(f"{kind} {path.relative_to(candidate)}")
        if kind in {"symlink", "unsupported"}:
            raise RuntimeError(f"bad candidate entry: {path}")
    print("CANDIDATE_ENTRIES:")
    for entry in candidate_entries:
        print(f"  {entry}")

    candidate_tree = pipeline_tree_sha256(candidate)
    trace_tree = pipeline_tree_sha256(trace_root)
    invocation = json.loads(required_regular["stage1_invocation"].read_text())
    result = json.loads(required_regular["stage1_result"].read_text())
    usage = json.loads(required_regular["generation_usage"].read_text())
    generation_root = Path(paths["generation_root"])
    for relative, expected in sorted(invocation["outputs"]["evidence"].items()):
        artifact = generation_root / relative
        require_regular(artifact)
        actual = sha256_file(artifact)
        print(
            f"INVOCATION_EVIDENCE {relative}: actual={actual} "
            f"expected={expected} match={actual == expected}"
        )
        if actual != expected:
            raise RuntimeError(f"invocation evidence mismatch: {relative}")
    print(
        "PIPELINE_TREE candidate="
        f"{candidate_tree} invocation={invocation['retained_workspace_sha256']} "
        f"result={result['outputs']['workspace_sha256']}"
    )
    print(
        "PIPELINE_TREE trace="
        f"{trace_tree} usage={usage['source_trace_sha256']}"
    )
    if not (
        candidate_tree
        == invocation["retained_workspace_sha256"]
        == result["outputs"]["workspace_sha256"]
    ):
        raise RuntimeError("candidate tree differs from stage-1 records")
    if trace_tree != usage["source_trace_sha256"]:
        raise RuntimeError("trace tree differs from usage record")

    trace_files = sorted(trace_root.rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    output_manifest = invocation["outputs"]["evidence"]
    trace_prefix = "codex-trace/"
    declared_trace_files = {
        name[len(trace_prefix) :]: digest
        for name, digest in output_manifest.items()
        if name.startswith(trace_prefix)
    }
    actual_trace_files = {
        path.relative_to(trace_root).as_posix(): sha256_file(path)
        for path in trace_files
    }
    print(f"TRACE_FILE_HASH_MAP_MATCH={actual_trace_files == declared_trace_files}")
    if actual_trace_files != declared_trace_files:
        raise RuntimeError("trace file set/hash mismatch")

    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    tool_names: Counter[str] = Counter()
    malformed = 0
    line_count = 0
    final_messages: list[str] = []
    for path in trace_files:
        with path.open() as stream:
            for line in stream:
                line_count += 1
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    malformed += 1
                    continue
                event_types[event.get("type", "<missing>")] += 1
                payload = event.get("payload", {})
                if isinstance(payload, dict):
                    payload_types[payload.get("type", "<missing>")] += 1
                    if payload.get("type") == "function_call":
                        tool_names[payload.get("name", "<missing>")] += 1
                    if payload.get("type") == "message" and payload.get("role") == "assistant":
                        texts = [
                            item.get("text", "")
                            for item in payload.get("content", [])
                            if isinstance(item, dict) and item.get("type") == "output_text"
                        ]
                        if texts:
                            final_messages.append("\n".join(texts))
    print(
        f"TRACE_PARSE lines={line_count} malformed={malformed} "
        f"event_types={dict(event_types)}"
    )
    print(f"TRACE_PAYLOAD_TYPES={dict(payload_types)}")
    print(f"TRACE_TOOL_NAMES={dict(tool_names)}")
    print(f"TRACE_ASSISTANT_FINAL_MESSAGES={len(final_messages)}")
    for index, message in enumerate(final_messages, 1):
        print(f"TRACE_FINAL_{index}={message[:1000]!r}")
    if malformed:
        raise RuntimeError("malformed structured trace lines")

    output_bytes = required_regular["generation_output"].read_bytes()
    print(
        "CODEX_OUTPUT_SCAN "
        f"bytes={len(output_bytes)} kprove={output_bytes.count(b'kprove')} "
        f"Top={output_bytes.count(b'#Top')} "
        f"RESULT={output_bytes.count(b'RESULT:')}"
    )
    print("PROVENANCE_CHECK=PASS")


if __name__ == "__main__":
    main()
