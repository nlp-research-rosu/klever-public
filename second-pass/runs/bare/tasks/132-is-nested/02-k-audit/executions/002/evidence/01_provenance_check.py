#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reproduce the stage record's deterministic sha256_tree algorithm."""
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
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    assert not path.is_symlink(), f"symlink not permitted: {path}"


def check_hash(label: str, path: Path, expected: str) -> None:
    require_regular(path)
    actual = sha256_file(path)
    print(f"HASH {label}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected


def main() -> None:
    require_regular(AUDIT_INPUT)
    require_regular(CAMPAIGN_LOCK)
    document = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(CAMPAIGN_LOCK.read_text())

    print(f"record_layout={document['record_layout']}")
    print(f"semantics_mode={document['semantics_mode']}")
    assert document["record_layout"] == "legacy-selected-stage1"
    assert document["semantics_mode"] == "GENERATED_SEMANTICS"
    assert document["audit_campaign"] == lock
    print("campaign_block_equals_lock=True")

    required = [
        AUDIT_INPUT,
        CAMPAIGN_LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "usage.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
        REFERENCE / "canonical.py",
        REFERENCE / "prompt.py",
        REFERENCE / "py2mpy.py",
    ]
    for path in required:
        require_regular(path)
    trace_files = sorted((GENERATION / "codex-trace").rglob("*"))
    assert trace_files
    for path in trace_files:
        mode = path.lstat().st_mode
        assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), path
        assert not path.is_symlink(), path
    print(f"required_regular_records={len(required)} trace_entries={len(trace_files)}")

    proof_artifacts = [
        "prompt.py",
        "py2mpy.py",
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for name in proof_artifacts:
        require_regular(CANDIDATE / name)
    for path in sorted(CANDIDATE.rglob("*")):
        mode = path.lstat().st_mode
        assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), path
        assert not path.is_symlink(), path
    print(f"candidate_required_proof_artifacts={len(proof_artifacts)} all_real_entries=True")

    assert not (REFERENCE / "reference-semantics").exists()
    assert not (REFERENCE / "reference-semantics").is_symlink()
    print("generated_semantics_boundary_reference_semantics_absent=True")

    hashes = document["hashes"]
    print(f"launcher_recorded_candidate_tree_sha256={hashes['candidate_tree_sha256']}")
    print(
        "launcher_recorded_generation_codex_trace_sha256="
        f"{hashes['generation_codex_trace_sha256']}"
    )
    direct = {
        "audit_campaign_lock_sha256": CAMPAIGN_LOCK,
        "candidate_prompt_sha256": CANDIDATE / "prompt.py",
        "candidate_translator_sha256": CANDIDATE / "py2mpy.py",
        "canonical_sha256": REFERENCE / "canonical.py",
        "generation_codex_last_sha256": GENERATION / "codex-last.txt",
        "generation_codex_output_sha256": GENERATION / "codex-output.log",
        "generation_metrics_sha256": GENERATION / "metrics.json",
        "generation_prompt_sha256": GENERATION / "prompt.txt",
        "generation_usage_sha256": GENERATION / "usage.json",
        "run_manifest_sha256": Path("/run.json"),
        "stage1_invocation_sha256": GENERATION / "invocation.json",
        "stage1_result_sha256": Path("/generation-result.json"),
        "task_manifest_sha256": Path("/task.json"),
        "trusted_prompt_sha256": REFERENCE / "prompt.py",
        "trusted_translator_sha256": REFERENCE / "py2mpy.py",
    }
    for label, path in direct.items():
        check_hash(label, path, hashes[label])
    assert hashes["manifest_sha256"] == hashes["task_manifest_sha256"]

    assert (CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes()
    assert (CANDIDATE / "py2mpy.py").read_bytes() == (REFERENCE / "py2mpy.py").read_bytes()
    print("candidate_prompt_byte_equal_trusted=True")
    print("candidate_translator_byte_equal_trusted=True")

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads((GENERATION / "invocation.json").read_text())
    for record_name, record in [("result", result), ("invocation", invocation)]:
        for relative, expected in sorted(record["outputs"]["evidence"].items()):
            check_hash(f"{record_name}.outputs.evidence.{relative}", GENERATION / relative, expected)

    candidate_tree = pipeline_tree_digest(CANDIDATE)
    trace_tree = pipeline_tree_digest(GENERATION / "codex-trace")
    print(f"pipeline_tree_digest(candidate)={candidate_tree}")
    print(f"stage_record_workspace_sha256={result['outputs']['workspace_sha256']}")
    print(f"candidate_tree_matches_stage_record={candidate_tree == result['outputs']['workspace_sha256']}")
    assert candidate_tree == result["outputs"]["workspace_sha256"]
    assert candidate_tree == invocation["outputs"]["workspace_sha256"]

    usage = json.loads((GENERATION / "usage.json").read_text())
    print(f"pipeline_tree_digest(codex-trace)={trace_tree}")
    print(f"usage.source_trace_sha256={usage['source_trace_sha256']}")
    print(f"trace_tree_matches_usage_record={trace_tree == usage['source_trace_sha256']}")
    assert trace_tree == usage["source_trace_sha256"]

    for path in sorted(CANDIDATE.rglob("*")):
        if path.is_file():
            print(
                "CANDIDATE_FILE "
                f"{path.relative_to(CANDIDATE).as_posix()} size={path.stat().st_size} "
                f"sha256={sha256_file(path)}"
            )

    top_level = Counter()
    payload_types = Counter()
    line_count = 0
    for path in sorted((GENERATION / "codex-trace").rglob("*.jsonl")):
        with path.open() as stream:
            for line_count, line in enumerate(stream, 1):
                event = json.loads(line)
                top_level[event.get("type")] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_types[payload.get("type")] += 1
    print(f"structured_trace_json_lines={line_count}")
    print(f"structured_trace_top_level_types={dict(sorted(top_level.items(), key=str))}")
    print(f"structured_trace_payload_types={dict(sorted(payload_types.items(), key=str))}")

    output_text = (GENERATION / "codex-output.log").read_text(errors="replace")
    claims = {
        "#Top": output_text.count("#Top"),
        "kprove": output_text.count("kprove"),
        "kompile": output_text.count("kompile"),
        "krun": output_text.count("krun"),
        "8191": output_text.count("8191"),
        "RESULT: KPROVE_PASSED": output_text.count("RESULT: KPROVE_PASSED"),
    }
    print(f"untrusted_generation_log_marker_counts={claims}")
    print("PROVENANCE_CHECKS_OK")


if __name__ == "__main__":
    main()
