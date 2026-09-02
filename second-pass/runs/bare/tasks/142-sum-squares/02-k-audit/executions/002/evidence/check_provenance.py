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
    root = root.resolve(strict=True)
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


audit_input = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
assert audit_input["record_layout"] == "legacy-selected-stage1"
assert audit_input["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit_input["audit_campaign"] == lock
assert not Path("/reference/reference-semantics").exists()

required_regular = [
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
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
for path in required_regular:
    require_regular(path)
for path in [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
]:
    require_directory(path)

expected_files = {
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
if Path("/generation-evidence/usage.json").exists():
    require_regular(Path("/generation-evidence/usage.json"))
    expected_files["/generation-evidence/usage.json"] = "generation_usage_sha256"

hashes = audit_input["hashes"]
for name, key in expected_files.items():
    actual = sha256_file(Path(name))
    expected = hashes[key]
    print(f"{name}: {actual} expected={expected} match={actual == expected}")
    assert actual == expected

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()

result = json.loads(Path("/generation-result.json").read_text())
for relative, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    require_regular(path)
    actual = sha256_file(path)
    print(f"result evidence {relative}: {actual} expected={expected} match={actual == expected}")
    assert actual == expected

candidate_tree = pipeline_tree_hash(Path("/candidate"))
trace_tree = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
print(f"pipeline tree hash /candidate: {candidate_tree}")
print(f"retained workspace hash: {result['outputs']['workspace_sha256']}")
print(f"pipeline tree hash /generation-evidence/codex-trace: {trace_tree}")
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
print(f"usage source trace hash: {usage['source_trace_sha256']}")
assert candidate_tree == result["outputs"]["workspace_sha256"]
assert trace_tree == usage["source_trace_sha256"]

for root in [Path("/candidate"), Path("/reference"), Path("/generation-evidence")]:
    linked = [str(path) for path in root.rglob("*") if path.is_symlink()]
    print(f"symlinks below {root}: {linked}")
    assert not linked

print("PROVENANCE_CHECK: PASS")
