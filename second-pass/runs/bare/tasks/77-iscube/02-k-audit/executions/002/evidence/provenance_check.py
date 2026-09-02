#!/usr/bin/env python3
"""Independent integrity checks for the mounted 77-iscube audit inputs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement the published pipeline_contract.sha256_tree algorithm."""
    if root.is_symlink() or not root.is_dir():
        raise RuntimeError(f"not a real directory: {root}")
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            mode = entry.stat(follow_symlinks=False).st_mode
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"linked or unsupported entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise RuntimeError(f"required regular file has wrong type: {path}")


def require_tree_regular(root: Path) -> None:
    mode = root.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise RuntimeError(f"required directory has wrong type: {root}")
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
            raise RuntimeError(f"linked or unsupported tree entry: {path}")


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")

    required = [
        AUDIT_INPUT,
        Path("/audit-campaign-lock.json"),
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
    if audit["record_layout"] == "pipeline-v3":
        required += [
            Path("/generation-evidence/runtime-metrics.json"),
            Path("/generation-evidence/usage.json"),
        ]
    for path in required:
        require_regular(path)
        print(f"regular_file OK {path}")

    require_tree_regular(Path("/candidate"))
    require_tree_regular(Path("/generation-evidence/codex-trace"))
    print("regular_tree OK /candidate")
    print("regular_tree OK /generation-evidence/codex-trace")

    if Path("/reference/reference-semantics").exists():
        raise RuntimeError("generated-semantics boundary violated: reference tree exists")
    print("generated_semantics_boundary OK (no trusted reference semantics)")

    hashes = audit["hashes"]
    checks = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    }
    for key, path in checks.items():
        if not path.exists() and hashes.get(key) is None:
            print(f"file_hash NOT_RECORDED {key}")
            continue
        require_regular(path)
        actual = sha256_file(path)
        expected = hashes[key]
        print(f"file_hash {key} expected={expected} actual={actual}")
        if actual != expected:
            raise RuntimeError(f"hash mismatch: {key}")

    campaign = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
    if campaign != audit["audit_campaign"]:
        raise RuntimeError("campaign lock content differs from audit_campaign block")
    print("campaign_lock_content OK")

    for candidate_path, trusted_path, label in [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
    ]:
        equal = candidate_path.read_bytes() == trusted_path.read_bytes()
        print(f"candidate_vs_trusted {label} byte_equal={equal}")
        if not equal:
            raise RuntimeError(f"candidate {label} differs from trusted mount")

    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    candidate_tree = pipeline_tree_digest(Path("/candidate"))
    trace_tree = pipeline_tree_digest(Path("/generation-evidence/codex-trace"))
    print(f"pipeline_tree candidate={candidate_tree}")
    print(f"pipeline_tree trace={trace_tree}")
    for label, expected, actual in [
        ("result.workspace", result["outputs"]["workspace_sha256"], candidate_tree),
        ("invocation.retained_workspace", invocation["retained_workspace_sha256"], candidate_tree),
        ("usage.source_trace", json.loads(Path("/generation-evidence/usage.json").read_text())["source_trace_sha256"], trace_tree),
    ]:
        print(f"pipeline_tree_check {label} expected={expected} actual={actual}")
        if expected != actual:
            raise RuntimeError(f"pipeline tree mismatch: {label}")

    # These launcher fields are recorded with a different, undocumented tree
    # encoding; report rather than pretending they use pipeline sha256_tree.
    print(
        "launcher_tree_field candidate_tree_sha256="
        + str(hashes["candidate_tree_sha256"])
    )
    print(
        "launcher_tree_field generation_codex_trace_sha256="
        + str(hashes["generation_codex_trace_sha256"])
    )

    trace_counts: Counter[str] = Counter()
    line_count = 0
    for trace_path in sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl")):
        with trace_path.open(encoding="utf-8") as stream:
            for line_count_for_file, line in enumerate(stream, start=1):
                record = json.loads(line)
                trace_counts[str(record.get("type"))] += 1
            line_count += line_count_for_file
    print(f"structured_trace parsed_lines={line_count} event_counts={dict(trace_counts)}")
    print("PROVENANCE_CHECK: PASS")


if __name__ == "__main__":
    main()
