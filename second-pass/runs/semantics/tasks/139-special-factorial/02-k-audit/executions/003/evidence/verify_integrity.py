#!/usr/bin/env python3
"""Independent integrity checks for audit stage 1.

This script reads every required launcher record and every JSONL trace record,
computes mounted file hashes, rejects linked/unsupported tree entries, and
compares the candidate's supplied semantics byte-for-byte with the trusted
mount.  It uses pipeline_contract.sha256_tree for the recorded manifest-tree
hashes because that algorithm is installed in the audit image.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

sys.path.insert(0, "/opt/humaneval/tools")
from pipeline_contract import sha256_tree  # type: ignore  # trusted audit image


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"required regular file is mistyped or linked: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"required directory is mistyped or linked: {path}")


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    require_directory(root)
    result: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256_file(path))
            else:
                raise AssertionError(f"linked/unsupported tree entry: {path}")
    return result


def check_hash(
    label: str, path: Path, expected: str, actual: str | None = None
) -> None:
    require_regular(path)
    observed = actual if actual is not None else sha256_file(path)
    print(f"HASH {label} expected={expected} observed={observed}")
    if observed != expected:
        raise AssertionError(f"hash mismatch for {label}: {path}")


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    hashes = audit["hashes"]
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"

    required_files = [
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
        Path("/generation-evidence/usage.json"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    required_dirs = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    ]
    for path in required_files:
        require_regular(path)
        # Parse all required JSON records, rather than merely checking existence.
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
    for path in required_dirs:
        require_directory(path)
    print(f"REQUIRED_FILES_OK count={len(required_files)}")
    print(f"REQUIRED_DIRECTORIES_OK count={len(required_dirs)}")

    campaign = json.loads(
        Path("/audit-campaign-lock.json").read_text(encoding="utf-8")
    )
    assert campaign == audit["audit_campaign"]
    print("CAMPAIGN_BLOCK_EQUALS_LOCK true")
    check_hash(
        "audit_campaign_lock",
        Path("/audit-campaign-lock.json"),
        hashes["audit_campaign_lock_sha256"],
    )

    file_checks = {
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_metrics_sha256": Path(
            "/generation-evidence/metrics.json"
        ),
        "generation_prompt_sha256": Path(
            "/generation-evidence/prompt.txt"
        ),
        "generation_usage_sha256": Path(
            "/generation-evidence/usage.json"
        ),
        "run_manifest_sha256": Path("/run.json"),
        "stage1_invocation_sha256": Path(
            "/generation-evidence/invocation.json"
        ),
        "stage1_result_sha256": Path("/generation-result.json"),
        "task_manifest_sha256": Path("/task.json"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    }
    for key, path in file_checks.items():
        check_hash(key, path, hashes[key])

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("PROMPT_BYTE_IDENTITY true")
    print("TRANSLATOR_BYTE_IDENTITY true")

    candidate_semantics = tree_entries(
        Path("/candidate/reference-semantics")
    )
    trusted_semantics = tree_entries(
        Path("/reference/reference-semantics")
    )
    assert candidate_semantics == trusted_semantics
    print(
        "SEMANTICS_RECURSIVE_BYTE_IDENTITY true "
        f"entries={len(candidate_semantics)}"
    )
    manifest_candidate_semantics_hash = sha256_tree(
        Path("/candidate/reference-semantics")
    )
    manifest_trusted_semantics_hash = sha256_tree(
        Path("/reference/reference-semantics")
    )
    print(
        "MANIFEST_TREE_HASH candidate="
        f"{manifest_candidate_semantics_hash} "
        f"trusted={manifest_trusted_semantics_hash}"
    )
    assert manifest_candidate_semantics_hash == hashes[
        "trusted_reference_semantics_manifest_sha256"
    ]
    assert manifest_trusted_semantics_hash == hashes[
        "trusted_reference_semantics_manifest_sha256"
    ]

    candidate_manifest_hash = sha256_tree(Path("/candidate"))
    trace_manifest_hash = sha256_tree(
        Path("/generation-evidence/codex-trace")
    )
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(
            encoding="utf-8"
        )
    )
    result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    usage = json.loads(
        Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
    )
    assert candidate_manifest_hash == invocation["retained_workspace_sha256"]
    assert candidate_manifest_hash == result["outputs"]["workspace_sha256"]
    assert trace_manifest_hash == usage["source_trace_sha256"]
    print(f"CANDIDATE_MANIFEST_TREE_HASH {candidate_manifest_hash}")
    print(f"TRACE_MANIFEST_TREE_HASH {trace_manifest_hash}")

    trace_files = sorted(
        Path("/generation-evidence/codex-trace").rglob("*.jsonl")
    )
    assert trace_files
    trace_counts: Counter[str] = Counter()
    trace_lines = 0
    for path in trace_files:
        require_regular(path)
        expected = result["outputs"]["evidence"][path.relative_to(
            "/generation-evidence"
        ).as_posix()]
        check_hash(f"trace-file:{path.name}", path, expected)
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                event = json.loads(line)
                trace_counts[event["type"]] += 1
                trace_lines += 1
    print(
        f"TRACE_JSONL_OK files={len(trace_files)} lines={trace_lines} "
        f"event_counts={dict(trace_counts)}"
    )

    # Read all generation prose/log bytes and record their sizes. Hash checks
    # above bind the entire contents even though the review cites only relevant
    # excerpts.
    for path in (
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ):
        text = path.read_text(encoding="utf-8")
        print(
            f"TEXT_RECORD_READ path={path} chars={len(text)} "
            f"lines={len(text.splitlines())}"
        )

    print("INTEGRITY_STATUS PASS")


if __name__ == "__main__":
    main()
