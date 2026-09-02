#!/usr/bin/env python3
"""Independent integrity and record-layout checks for audit 28-concatenate."""

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
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def content_tree_digest(root: Path) -> str:
    """Path/type/size/content tree digest, rejecting non-file/non-directory nodes."""
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
                raise RuntimeError(f"unsupported tree node: {path}")
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


def describe(path: Path) -> str:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return "MISSING"
    if stat.S_ISLNK(info.st_mode):
        return f"SYMLINK->{os.readlink(path)}"
    if stat.S_ISREG(info.st_mode):
        return f"REGULAR mode={stat.S_IMODE(info.st_mode):04o} size={info.st_size}"
    if stat.S_ISDIR(info.st_mode):
        return f"DIRECTORY mode={stat.S_IMODE(info.st_mode):04o}"
    return f"OTHER mode={info.st_mode:o}"


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())

print(f"audit_input: {describe(AUDIT_INPUT)} sha256={sha256_file(AUDIT_INPUT)}")
print(f"campaign_lock: {describe(LOCK)} sha256={sha256_file(LOCK)}")
print(f"record_layout={audit.get('record_layout')}")
print(f"semantics_mode={audit.get('semantics_mode')}")
print(f"campaign_object_equal={audit.get('audit_campaign') == lock}")
print(
    "campaign_hash_equal="
    f"{sha256_file(LOCK) == audit['hashes']['audit_campaign_lock_sha256']}"
)

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
optional = [Path("/generation-evidence/usage.json")]
for path in required:
    print(f"required {path}: {describe(path)} readable={os.access(path, os.R_OK)}")
for path in optional:
    print(f"optional {path}: {describe(path)} readable={os.access(path, os.R_OK)}")

declared_files = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}
for name, key in declared_files.items():
    path = Path(name)
    actual = sha256_file(path)
    expected = audit["hashes"][key]
    print(
        f"hash {name}: actual={actual} expected={expected} "
        f"match={actual == expected}"
    )

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
for record_name, record in [("result", result), ("invocation", invocation)]:
    for rel, expected in sorted(record["outputs"]["evidence"].items()):
        path = Path("/generation-evidence") / rel
        actual = sha256_file(path)
        print(
            f"{record_name}-evidence {rel}: actual={actual} expected={expected} "
            f"match={actual == expected} type={describe(path)}"
        )

for root in [Path("/candidate"), Path("/reference"), Path("/generation-evidence")]:
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            print(f"recursive-symlink {path}: {describe(path)}")

trusted_semantics = Path("/reference/reference-semantics")
print(f"generated-mode trusted-semantics path: {describe(trusted_semantics)}")
print(
    "candidate_prompt_byte_equal="
    f"{Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
)
print(
    "candidate_translator_byte_equal="
    f"{Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
)

candidate_digest = content_tree_digest(Path("/candidate"))
trace_digest = content_tree_digest(Path("/generation-evidence/codex-trace"))
print(f"candidate_content_tree_digest={candidate_digest}")
print(
    "candidate_tree_matches_stage1_result="
    f"{candidate_digest == result['outputs']['workspace_sha256']}"
)
print(
    "candidate_tree_matches_invocation_retained="
    f"{candidate_digest == invocation['retained_workspace_sha256']}"
)
print(
    "audit_input_candidate_secondary_hash="
    f"{audit['hashes']['candidate_tree_sha256']}"
)
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
print(f"trace_content_tree_digest={trace_digest}")
print(
    "trace_tree_matches_usage_source="
    f"{trace_digest == usage['source_trace_sha256']}"
)
print(
    "audit_input_trace_secondary_hash="
    f"{audit['hashes']['generation_codex_trace_sha256']}"
)

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
print(f"trace_regular_file_count={len(trace_files)}")
for path in trace_files:
    counts: Counter[str] = Counter()
    malformed = 0
    with path.open() as stream:
        for line in stream:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            counts[str(item.get("type"))] += 1
    print(
        f"trace {path.relative_to('/generation-evidence')}: "
        f"sha256={sha256_file(path)} malformed_json_lines={malformed} "
        f"event_types={dict(counts)}"
    )
