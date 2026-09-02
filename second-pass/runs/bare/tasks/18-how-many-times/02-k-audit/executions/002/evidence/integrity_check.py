#!/usr/bin/env python3
import hashlib
import json
import os
import stat
from pathlib import Path

AUDIT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def sha256_tree(root: Path) -> str:
    digest = hashlib.sha256()
    entries = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            info = child.stat(follow_symlinks=False)
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(info.st_mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(info.st_mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


data = json.loads(AUDIT.read_text())
assert data["record_layout"] == "legacy-selected-stage1"
assert data["semantics_mode"] == "GENERATED_SEMANTICS"
assert data["mount_reference_semantics"] is False

lock_path = Path(data["container_paths"]["audit_campaign_lock"])
require_regular(lock_path)
lock = json.loads(lock_path.read_text())
assert lock == data["audit_campaign"], "campaign lock JSON differs from campaign block"

expected = {
    lock_path: data["hashes"]["audit_campaign_lock_sha256"],
    Path(data["container_paths"]["run_manifest"]): data["hashes"]["run_manifest_sha256"],
    Path(data["container_paths"]["task_manifest"]): data["hashes"]["task_manifest_sha256"],
    Path(data["container_paths"]["stage1_result"]): data["hashes"]["stage1_result_sha256"],
    Path(data["container_paths"]["canonical"]): data["hashes"]["canonical_sha256"],
    Path(data["container_paths"]["trusted_prompt"]): data["hashes"]["trusted_prompt_sha256"],
    Path(data["container_paths"]["translator"]): data["hashes"]["trusted_translator_sha256"],
    Path(data["container_paths"]["generation_manifest"]): data["hashes"]["stage1_invocation_sha256"],
    Path(data["container_paths"]["generation_metrics"]): data["hashes"]["generation_metrics_sha256"],
    Path(data["container_paths"]["generation_last"]): data["hashes"]["generation_codex_last_sha256"],
    Path(data["container_paths"]["generation_output"]): data["hashes"]["generation_codex_output_sha256"],
    Path(data["container_paths"]["generation_root"]) / "prompt.txt": data["hashes"]["generation_prompt_sha256"],
    Path(data["container_paths"]["generation_root"]) / "usage.json": data["hashes"]["generation_usage_sha256"],
}

for path, wanted in expected.items():
    require_regular(path)
    actual = sha256_file(path)
    print(f"HASH {path} {actual} expected={wanted} match={actual == wanted}")
    assert actual == wanted, f"hash mismatch: {path}"

candidate = Path(data["container_paths"]["candidate"])
required_candidate = [
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
    "prove.sh",
]
for name in required_candidate:
    require_regular(candidate / name)

assert os.access(candidate / "prove.sh", os.X_OK), "prove.sh is not executable"
assert (candidate / "prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert (candidate / "py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
assert not os.path.lexists("/reference/reference-semantics")
assert not os.path.lexists("/candidate/reference-semantics")

candidate_tree = sha256_tree(candidate)
result_record = json.loads(Path("/generation-result.json").read_text())
invocation_record = json.loads(Path("/generation-evidence/invocation.json").read_text())
print(
    "CANDIDATE_TREE "
    f"{candidate_tree} generation-result={result_record['outputs']['workspace_sha256']} "
    f"invocation={invocation_record['retained_workspace_sha256']}"
)
assert candidate_tree == result_record["outputs"]["workspace_sha256"]
assert candidate_tree == invocation_record["retained_workspace_sha256"]
print(f"AUDIT_LAUNCHER_CANDIDATE_TREE_RECORDED {data['hashes']['candidate_tree_sha256']}")

trace_tree = sha256_tree(Path(data["container_paths"]["generation_trace"]))
usage_record = json.loads(Path("/generation-evidence/usage.json").read_text())
print(
    "TRACE_TREE "
    f"{trace_tree} usage-source={usage_record['source_trace_sha256']} "
    f"match={trace_tree == usage_record['source_trace_sha256']}"
)
assert trace_tree == usage_record["source_trace_sha256"]
print(f"AUDIT_LAUNCHER_TRACE_TREE_RECORDED {data['hashes']['generation_codex_trace_sha256']}")

for root in [candidate, Path("/reference"), Path("/generation-evidence/codex-trace")]:
    for current, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            entry = Path(current) / name
            assert not entry.is_symlink(), f"symlink in required tree: {entry}"

result = result_record
for relative, wanted in result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    require_regular(path)
    actual = sha256_file(path)
    print(f"GENERATION_HASH {relative} {actual} expected={wanted} match={actual == wanted}")
    assert actual == wanted, f"generation-result evidence hash mismatch: {relative}"

print("CANDIDATE_FILE_HASHES")
for path in sorted(p for p in candidate.rglob("*") if p.is_file()):
    print(f"{path.relative_to(candidate)} {sha256_file(path)}")

trace_files = sorted(p for p in Path("/generation-evidence/codex-trace").rglob("*") if p.is_file())
print(f"TRACE_FILE_COUNT {len(trace_files)}")
for path in trace_files:
    print(f"TRACE_FILE {path.relative_to('/generation-evidence/codex-trace')} {sha256_file(path)}")

print("INTEGRITY_CHECK_OK")
