#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Reimplement the pipeline-v2 tree digest, including directory entries."""
    digest = hashlib.sha256()
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    assert path.is_file(), f"missing/non-file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"
    path.read_bytes()


audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
run = json.loads(Path("/run.json").read_text())
task = json.loads(Path("/task.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
metrics = json.loads(Path("/generation-evidence/metrics.json").read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["audit_campaign"] == lock
lock_hash = sha256_file(Path("/audit-campaign-lock.json"))
print(f"audit_campaign_lock_sha256={lock_hash}")
assert lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]
assert not Path("/reference/reference-semantics").exists()
assert not Path("/reference/reference-semantics").is_symlink()
print("reference-semantics=absent (required)")

required_files = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/usage.json"),
]
for path in required_files:
    require_regular(path)

for root in (Path("/candidate"), Path("/generation-evidence/codex-trace")):
    assert root.is_dir() and not root.is_symlink()
    for path in root.rglob("*"):
        assert not path.is_symlink(), f"symlinked entry: {path}"
        if path.is_file():
            path.read_bytes()

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

hash_path_pairs = {
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
}
for field, path in hash_path_pairs.items():
    actual = sha256_file(path)
    expected = audit["hashes"][field]
    print(f"{field}: expected={expected} actual={actual}")
    assert actual == expected

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
assert audit["integrity"]["candidate_prompt_matches_trusted"] is True
assert audit["integrity"]["candidate_translator_matches_trusted"] is True

evidence_root = Path("/generation-evidence")
for relative, expected in result["outputs"]["evidence"].items():
    path = evidence_root / relative
    require_regular(path)
    actual = sha256_file(path)
    print(f"generation-result evidence {relative}: expected={expected} actual={actual}")
    assert actual == expected
    assert invocation["outputs"]["evidence"][relative] == expected

candidate_tree = sha256_tree(Path("/candidate"))
trace_tree = sha256_tree(Path("/generation-evidence/codex-trace"))
print(f"pipeline_candidate_tree_sha256={candidate_tree}")
print(f"pipeline_trace_tree_sha256={trace_tree}")
assert candidate_tree == result["outputs"]["workspace_sha256"]
assert candidate_tree == invocation["retained_workspace_sha256"]
assert trace_tree == usage["source_trace_sha256"]

trace_types: Counter[str] = Counter()
trace_lines = 0
for path in sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl")):
    with path.open() as stream:
        for line in stream:
            event = json.loads(line)
            trace_types[event["type"]] += 1
            trace_lines += 1
print(f"trace_lines={trace_lines}")
print(f"trace_event_types={dict(sorted(trace_types.items()))}")

output_text = Path("/generation-evidence/codex-output.log").read_text(
    errors="replace"
)
last_text = Path("/generation-evidence/codex-last.txt").read_text(errors="replace")
prompt_text = Path("/generation-evidence/prompt.txt").read_text(errors="replace")
print(f"codex_output_lines={len(output_text.splitlines())}")
print(f"codex_output_top_occurrences={output_text.count('#Top')}")
print(f"codex_last_chars={len(last_text)}")
print(f"generation_prompt_chars={len(prompt_text)}")
print(f"run_status={run['tasks'][17] if False else run['schema_version']}")
print(f"task_problem_id={task['problem_id']}")
print(f"result_marker={result['result_marker']}")
print(f"metrics_status={metrics['status']}")
print("PROVENANCE_CHECK=PASS")
