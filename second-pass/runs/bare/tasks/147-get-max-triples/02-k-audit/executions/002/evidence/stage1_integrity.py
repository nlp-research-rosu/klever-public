#!/usr/bin/env python3
"""Independent provenance and mount-integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reproduce the generation record's length-prefixed tree digest."""
    digest = hashlib.sha256()
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
                raise AssertionError(f"unsupported tree entry: {path}")
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


def launcher_tree_hash(root: Path) -> str:
    """Reproduce the launcher-owned tree hashes recorded in audit-input.json."""
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            kind, content = b"directory", b""
        elif stat.S_ISREG(mode):
            kind, content = b"file", path.read_bytes()
        else:
            raise AssertionError(f"linked or unsupported tree entry: {path}")
        relative = path.relative_to(root).as_posix().encode()
        for value in (relative, kind, content):
            digest.update(len(value).to_bytes(8, "big"))
            digest.update(value)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_tree_without_links(root: Path) -> None:
    assert stat.S_ISDIR(root.lstat().st_mode), f"not a real directory: {root}"
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        assert stat.S_ISREG(mode) or stat.S_ISDIR(mode), (
            f"linked or unsupported entry: {path}"
        )


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["mount_reference_semantics"] is False
assert not Path("/reference/reference-semantics").exists()
assert lock == audit["audit_campaign"]
assert sha256_file(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]

container_paths = {
    key: Path(value) for key, value in audit["container_paths"].items()
}
for key, path in sorted(container_paths.items()):
    if key in {"candidate", "generation_root", "generation_trace"}:
        require_tree_without_links(path)
    else:
        require_regular(path)

required_layout_files = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required_layout_files:
    require_regular(path)
require_tree_without_links(Path("/generation-evidence/codex-trace"))

candidate_required = [
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
    "prove.sh",
]
for name in candidate_required:
    require_regular(Path("/candidate") / name)
require_tree_without_links(Path("/candidate"))

hash_paths = {
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
for key, path in hash_paths.items():
    require_regular(path)
    actual = sha256_file(path)
    expected = audit["hashes"][key]
    print(f"{key}: actual={actual} expected={expected} match={actual == expected}")
    assert actual == expected

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()

generation_result = json.loads(Path("/generation-result.json").read_text())
generation_invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text()
)
generation_usage = json.loads(Path("/generation-evidence/usage.json").read_text())
for relative, expected in generation_result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    require_regular(path)
    actual = sha256_file(path)
    print(
        f"generation evidence {relative}: actual={actual} "
        f"expected={expected} match={actual == expected}"
    )
    assert actual == expected

candidate_pipeline = pipeline_tree_hash(Path("/candidate"))
trace_pipeline = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
candidate_launcher = launcher_tree_hash(Path("/candidate"))
trace_launcher = launcher_tree_hash(Path("/generation-evidence/codex-trace"))
print(
    "candidate pipeline tree:",
    candidate_pipeline,
    "expected:",
    generation_invocation["outputs"]["workspace_sha256"],
)
print(
    "trace pipeline tree:",
    trace_pipeline,
    "expected:",
    generation_usage["source_trace_sha256"],
)
print(
    "candidate launcher tree:",
    candidate_launcher,
    "expected:",
    audit["hashes"]["candidate_tree_sha256"],
)
print(
    "trace launcher tree:",
    trace_launcher,
    "expected:",
    audit["hashes"]["generation_codex_trace_sha256"],
)
assert candidate_pipeline == generation_invocation["outputs"]["workspace_sha256"]
assert trace_pipeline == generation_usage["source_trace_sha256"]
assert candidate_launcher == audit["hashes"]["candidate_tree_sha256"]
assert trace_launcher == audit["hashes"]["generation_codex_trace_sha256"]

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
assert len(trace_files) == 1
trace_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
events = []
with trace_files[0].open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        event = json.loads(line)
        events.append(event)
        trace_types[event["type"]] += 1
        payload = event.get("payload")
        if isinstance(payload, dict) and isinstance(payload.get("type"), str):
            payload_types[payload["type"]] += 1
assert line_number == 339
selected = generation_usage["selected_event"]
assert selected["line_number"] == 338
assert events[337]["type"] == "event_msg"
assert events[337]["payload"]["type"] == "token_count"
assert events[-1]["type"] == "event_msg"
print("trace JSON lines:", line_number)
print("trace top-level types:", dict(sorted(trace_types.items())))
print("trace payload types:", dict(sorted(payload_types.items())))

output_text = Path("/generation-evidence/codex-output.log").read_text(
    encoding="utf-8", errors="replace"
)
print("codex-output bytes:", len(output_text.encode()))
for marker in [
    "kompile verification.k",
    "kprove spec.k",
    "#Top",
    "RESULT: KPROVE_PASSED",
]:
    print(f"codex-output marker {marker!r}: count={output_text.count(marker)}")

print("campaign block match: PASS")
print("generated-semantics mount boundary: PASS")
print("required legacy-selected-stage1 records: PASS")
print("candidate prompt/translator trusted-byte-identity: PASS")
print("all provenance checks: PASS")
