#!/usr/bin/env python3
"""Independent verification of launcher records and mounted provenance."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    return sorted(entries)


def sha256_tree_v3(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


def legacy_tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def main() -> None:
    require_regular(AUDIT_INPUT)
    require_regular(CAMPAIGN_LOCK)
    audit = json.loads(AUDIT_INPUT.read_text())
    campaign = json.loads(CAMPAIGN_LOCK.read_text())

    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["audit_campaign"] == campaign
    actual_lock_hash = file_hash(CAMPAIGN_LOCK)
    assert actual_lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]

    required = [
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

    trace_root = Path("/generation-evidence/codex-trace")
    assert trace_root.is_dir() and not trace_root.is_symlink()
    traces = sorted(trace_root.rglob("*.jsonl"))
    assert traces, "no structured trace records"
    trace_records = 0
    trace_types: dict[str, int] = {}
    for trace in traces:
        require_regular(trace)
        with trace.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                value = json.loads(line)
                assert isinstance(value, dict), (trace, line_number)
                trace_records += 1
                event_type = str(value.get("type", "<missing>"))
                trace_types[event_type] = trace_types.get(event_type, 0) + 1

    assert not Path("/reference/reference-semantics").exists()
    assert not Path("/candidate/reference-semantics").exists()
    assert Path("/candidate").is_dir() and not Path("/candidate").is_symlink()
    assert Path("/reference").is_dir() and not Path("/reference").is_symlink()
    tree_entries(Path("/candidate"))
    tree_entries(Path("/reference"))
    tree_entries(Path("/generation-evidence"))

    hashes = audit["hashes"]
    comparisons = {
        "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    }
    if usage.exists():
        comparisons[str(usage)] = "generation_usage_sha256"
    for path_string, key in comparisons.items():
        actual = file_hash(Path(path_string))
        assert actual == hashes[key], (path_string, actual, hashes[key])

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()

    trace_file_hashes = {
        trace.relative_to(Path("/generation-evidence")).as_posix(): file_hash(trace)
        for trace in traces
    }
    stage1_result = json.loads(Path("/generation-result.json").read_text())
    for relative, actual in trace_file_hashes.items():
        expected = stage1_result["outputs"]["evidence"][relative]
        assert actual == expected, (relative, actual, expected)

    candidate_v3 = sha256_tree_v3(Path("/candidate"))
    candidate_legacy = legacy_tree_digest(Path("/candidate"))
    trace_v3 = sha256_tree_v3(trace_root)
    trace_legacy = legacy_tree_digest(trace_root)

    print("record_layout=legacy-selected-stage1")
    print("semantics_mode=GENERATED_SEMANTICS")
    print("campaign_block_exact_match=true")
    print(f"campaign_lock_sha256={actual_lock_hash} (matches)")
    print("required_records=all regular and readable")
    print("candidate_prompt_byte_identity=true")
    print("candidate_translator_byte_identity=true")
    print("trusted_reference_semantics_absent=true")
    print("candidate_reference_semantics_absent=true")
    print(f"structured_trace_files={len(traces)}")
    print(f"structured_trace_records={trace_records}")
    print(f"structured_trace_types={json.dumps(trace_types, sort_keys=True)}")
    print(f"candidate_tree_sha256_v3={candidate_v3}")
    print(f"candidate_tree_sha256_legacy={candidate_legacy}")
    print(f"candidate_tree_sha256_recorded={hashes['candidate_tree_sha256']}")
    print(f"trace_tree_sha256_v3={trace_v3}")
    print(f"trace_tree_sha256_legacy={trace_legacy}")
    print(f"trace_tree_sha256_recorded={hashes['generation_codex_trace_sha256']}")
    print("PROVENANCE_CHECK=PASS")


if __name__ == "__main__":
    main()
