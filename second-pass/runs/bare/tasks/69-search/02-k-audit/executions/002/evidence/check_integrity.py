#!/usr/bin/env python3
import hashlib
import json
import os
import stat
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Independently reproduce the content-tree scheme used in stage records."""
    digest = hashlib.sha256()
    pending = [root]
    entries = []
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
                raise AssertionError(f"linked or unsupported entry: {path}")
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


audit_input = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
assert audit_input["record_layout"] == "legacy-selected-stage1"
assert audit_input["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit_input["audit_campaign"] == lock
assert not Path("/reference/reference-semantics").exists()

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/codex-trace"),
]
for path in required:
    assert path.exists(), path
    assert not path.is_symlink(), path

hash_checks = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
}
for name, key in hash_checks.items():
    actual = sha256_file(Path(name))
    expected = audit_input["hashes"][key]
    assert actual == expected, (name, actual, expected)
    print(f"OK file {name} {actual}")

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
assert trace_files
records = 0
for path in trace_files:
    assert not path.is_symlink()
    with path.open() as stream:
        for line in stream:
            json.loads(line)
            records += 1

invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
candidate_hash = pipeline_tree_hash(Path("/candidate"))
trace_hash = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
assert candidate_hash == invocation["outputs"]["workspace_sha256"]
assert candidate_hash == result["outputs"]["workspace_sha256"]
assert trace_hash == json.loads(Path("/generation-evidence/usage.json").read_text())[
    "source_trace_sha256"
]
print(f"OK candidate pipeline tree {candidate_hash}")
print(f"OK trace pipeline tree {trace_hash}; parsed_records={records}")

symlinks = [
    str(path)
    for root in (Path("/candidate"), Path("/generation-evidence"))
    for path in root.rglob("*")
    if path.is_symlink()
]
assert not symlinks, symlinks
print("OK no symlinks in candidate or generation evidence")
print("OK campaign lock equals audit_campaign object")
print("OK generated-semantics boundary: trusted reference-semantics absent")
