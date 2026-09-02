#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(path: Path) -> str:
    """Independently implement the pipeline-v2 manifest tree digest."""
    if path.is_symlink() or not path.is_dir():
        raise AssertionError(f"tree root is not a real directory: {path}")
    pending = [path]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            child_path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = child_path.relative_to(path).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", child_path))
                pending.append(child_path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", child_path))
            else:
                raise AssertionError(
                    f"linked or unsupported tree entry: {child_path}"
                )
    digest = hashlib.sha256()
    for relative, kind, child_path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = child_path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with child_path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"
    next(os.scandir(path), None)


def compare_trees(candidate: Path, trusted: Path) -> None:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        pending = [root]
        while pending:
            directory = pending.pop()
            for child in os.scandir(directory):
                path = Path(child.path)
                relative = path.relative_to(root).as_posix()
                mode = child.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    result[relative] = ("directory", None)
                    pending.append(path)
                elif stat.S_ISREG(mode):
                    result[relative] = ("file", sha256_file(path))
                elif stat.S_ISLNK(mode):
                    result[relative] = ("symlink", None)
                else:
                    result[relative] = ("unsupported", None)
        return result

    left = inventory(candidate)
    right = inventory(trusted)
    assert left == right, "candidate and trusted reference-semantics inventories differ"
    print(f"reference_semantics_entries={len(left)}")
    print("reference_semantics_exact_inventory_match=True")


audit = json.loads(AUDIT_INPUT.read_text())
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["mount_reference_semantics"] is True

required_files = [
    AUDIT_INPUT,
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
required_dirs = [
    Path("/candidate"),
    Path("/reference/reference-semantics"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
]
for path in required_files:
    require_regular(path)
for path in required_dirs:
    require_directory(path)
print(f"required_regular_files={len(required_files)}")
print(f"required_real_directories={len(required_dirs)}")

campaign = json.loads(Path("/audit-campaign-lock.json").read_text())
assert campaign == audit["audit_campaign"]
assert (
    sha256_file(Path("/audit-campaign-lock.json"))
    == audit["hashes"]["audit_campaign_lock_sha256"]
)
print("campaign_lock_exact_json_match=True")
print("campaign_lock_sha256_match=True")

direct_hashes = {
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
}
for path, key in direct_hashes.items():
    observed = sha256_file(path)
    expected = audit["hashes"][key]
    assert observed == expected, f"{path}: {observed} != recorded {expected}"
    print(f"{key}={observed}")

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
print("candidate_prompt_byte_identity=True")
print("candidate_translator_byte_identity=True")

compare_trees(
    Path("/candidate/reference-semantics"),
    Path("/reference/reference-semantics"),
)
candidate_semantics_manifest = sha256_tree(
    Path("/candidate/reference-semantics")
)
trusted_semantics_manifest = sha256_tree(
    Path("/reference/reference-semantics")
)
assert (
    candidate_semantics_manifest
    == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
)
assert candidate_semantics_manifest == trusted_semantics_manifest
print(f"reference_semantics_manifest_sha256={candidate_semantics_manifest}")

candidate_workspace_manifest = sha256_tree(Path("/candidate"))
generation_result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text()
)
assert candidate_workspace_manifest == generation_result["outputs"]["workspace_sha256"]
assert candidate_workspace_manifest == invocation["outputs"]["workspace_sha256"]
print(f"candidate_workspace_manifest_sha256={candidate_workspace_manifest}")
print("candidate_workspace_matches_generation_records=True")

trace_root = Path("/generation-evidence/codex-trace")
trace_manifest = sha256_tree(trace_root)
assert trace_manifest == json.loads(
    Path("/generation-evidence/usage.json").read_text()
)["source_trace_sha256"]
print(f"generation_trace_manifest_sha256={trace_manifest}")

result_evidence = generation_result["outputs"]["evidence"]
for relative, expected in sorted(result_evidence.items()):
    path = Path("/generation-evidence") / relative
    require_regular(path)
    observed = sha256_file(path)
    assert observed == expected, f"{relative}: evidence hash mismatch"
    print(f"generation_result_evidence_sha256[{relative}]={observed}")

trace_files = sorted(trace_root.rglob("*"))
jsonl_count = 0
jsonl_records = 0
for path in trace_files:
    if path.is_file():
        require_regular(path)
        if path.suffix == ".jsonl":
            jsonl_count += 1
            with path.open() as stream:
                for line_no, line in enumerate(stream, 1):
                    json.loads(line)
                    jsonl_records += 1
assert jsonl_count > 0
print(f"trace_jsonl_files={jsonl_count}")
print(f"trace_valid_json_records={jsonl_records}")

assert audit["integrity"] == {
    "candidate_prompt_matches_trusted": True,
    "candidate_reference_semantics_matches_trusted": True,
    "candidate_translator_matches_trusted": True,
    "manifest_prompt_hash_matches_trusted": True,
    "manifest_reference_semantics_hash_matches_trusted": True,
    "manifest_translator_hash_matches_trusted": True,
}
print("launcher_integrity_fields_consistent=True")
print("STAGE1_INTEGRITY=PASS")
