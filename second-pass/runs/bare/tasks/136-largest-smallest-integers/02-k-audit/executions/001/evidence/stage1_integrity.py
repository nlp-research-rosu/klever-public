#!/usr/bin/env python3
"""Independent integrity checks for the mounted pipeline-v3 audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Pipeline-v3 canonical workspace/tree hash, independently implemented."""
    if not root.is_dir() or root.is_symlink():
        raise RuntimeError(f"not a real directory: {root}")
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
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
        raise RuntimeError(f"required regular file is missing or mistyped: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise RuntimeError(f"required real directory is missing or mistyped: {path}")


def report_hash(label: str, path: Path, expected: str | None) -> None:
    actual = sha256_file(path)
    status = "MATCH" if expected == actual else "MISMATCH"
    print(f"{label}: {status} actual={actual} expected={expected} path={path}")
    if status != "MATCH":
        raise RuntimeError(f"hash mismatch for {label}")


def main() -> int:
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    if audit["record_layout"] != "pipeline-v3":
        raise RuntimeError(f"unexpected layout: {audit['record_layout']}")
    if audit["semantics_mode"] != "GENERATED_SEMANTICS":
        raise RuntimeError(f"unexpected semantics mode: {audit['semantics_mode']}")

    required_files = [
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
    required_dirs = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference"),
    ]
    for path in required_files:
        require_regular(path)
    for path in required_dirs:
        require_directory(path)
    print(f"required regular files: PASS ({len(required_files)})")
    print(f"required real directories: PASS ({len(required_dirs)})")

    all_roots = [Path("/candidate"), Path("/generation-evidence"), Path("/reference")]
    links = [path for root in all_roots for path in root.rglob("*") if path.is_symlink()]
    if links:
        raise RuntimeError("symlinks found: " + ", ".join(map(str, links)))
    print("mounted tree symlink scan: PASS (0 symlinks)")

    lock = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
    if lock != audit["audit_campaign"]:
        raise RuntimeError("campaign lock JSON differs from audit_campaign block")
    print("campaign lock block equality: PASS")

    hashes = audit["hashes"]
    fixed_hashes = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_runtime_metrics_sha256": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    }
    for label, path in fixed_hashes.items():
        report_hash(label, path, hashes[label])

    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    output_hashes = result["outputs"]["evidence"]
    for relative, expected in sorted(output_hashes.items()):
        path = Path("/generation-evidence") / relative
        if "/" not in relative or not relative.startswith("codex-trace/"):
            require_regular(path)
        report_hash(f"generation-result.outputs.evidence[{relative}]", path, expected)
    if output_hashes != invocation["outputs"]["evidence"]:
        raise RuntimeError("result and invocation evidence maps differ")
    print("result/invocation evidence-map equality: PASS")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    if len(trace_files) != 1:
        raise RuntimeError(f"expected one JSONL trace, got {len(trace_files)}")
    trace_lines = 0
    with trace_files[0].open(encoding="utf-8") as stream:
        for trace_lines, line in enumerate(stream, 1):
            json.loads(line)
    print(f"structured trace JSON parse: PASS ({trace_lines} records)")

    if Path("/reference/reference-semantics").exists() or Path(
        "/reference/reference-semantics"
    ).is_symlink():
        raise RuntimeError("reference semantics unexpectedly present")
    print("generated-semantics boundary: PASS (trusted reference semantics absent)")

    candidate_prompt = sha256_file(Path("/candidate/prompt.py"))
    candidate_translator = sha256_file(Path("/candidate/py2mpy.py"))
    if candidate_prompt != hashes["trusted_prompt_sha256"]:
        raise RuntimeError("candidate prompt differs from trusted prompt")
    if candidate_translator != hashes["trusted_translator_sha256"]:
        raise RuntimeError("candidate translator differs from trusted translator")
    print("candidate prompt versus trusted prompt: PASS")
    print("candidate translator versus trusted translator: PASS")

    candidate_tree = sha256_tree(Path("/candidate"))
    result_tree = result["outputs"]["workspace_sha256"]
    invocation_tree = invocation["outputs"]["workspace_sha256"]
    print(f"candidate canonical pipeline tree hash: {candidate_tree}")
    print(f"generation-result workspace hash: {result_tree}")
    print(f"generation-invocation workspace hash: {invocation_tree}")
    if candidate_tree != result_tree or candidate_tree != invocation_tree:
        raise RuntimeError("mounted candidate differs from recorded generated workspace")
    print("candidate versus generation workspace: PASS")

    trace_tree = sha256_tree(Path("/generation-evidence/codex-trace"))
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    print(f"trace canonical pipeline tree hash: {trace_tree}")
    print(f"usage source_trace_sha256: {usage['source_trace_sha256']}")
    if trace_tree != usage["source_trace_sha256"]:
        raise RuntimeError("trace tree differs from usage source trace")
    print("trace tree versus usage record: PASS")

    # These two launcher fields use a distinct, undeclared tree-digest
    # serialization. Print them for provenance without equating that encoding
    # with pipeline-v3's documented workspace digest.
    print(f"launcher candidate_tree_sha256 field: {hashes['candidate_tree_sha256']}")
    print(
        "launcher generation_codex_trace_sha256 field: "
        f"{hashes['generation_codex_trace_sha256']}"
    )
    print("STAGE1_INTEGRITY: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"STAGE1_INTEGRITY: FAIL: {error}", file=sys.stderr)
        raise
