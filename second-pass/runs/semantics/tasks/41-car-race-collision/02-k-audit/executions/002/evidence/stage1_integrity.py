#!/usr/bin/env python3
"""Independent integrity and record-layout checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "other"


def tree(root: Path) -> dict[str, tuple[str, int, int, str | None]]:
    result: dict[str, tuple[str, int, int, str | None]] = {}
    for base, directories, files in os.walk(root, topdown=True, followlinks=False):
        base_path = Path(base)
        names = sorted(directories + files)
        for name in names:
            path = base_path / name
            relative = path.relative_to(root).as_posix()
            path_kind = kind(path)
            path_stat = path.lstat()
            content = sha256(path) if path_kind == "file" else None
            if path_kind == "symlink":
                content = os.readlink(path)
            result[relative] = (
                path_kind,
                stat.S_IMODE(path_stat.st_mode),
                path_stat.st_size,
                content,
            )
        directories[:] = [
            name for name in directories if not (base_path / name).is_symlink()
        ]
    return result


def independent_tree_digest(entries: dict[str, tuple[str, int, int, str | None]]) -> str:
    """Reviewer-defined digest over typed path metadata and file bytes."""
    digest = hashlib.sha256()
    for relative, record in sorted(entries.items()):
        path_kind, mode, size, content = record
        fields = [relative, path_kind, f"{mode:o}", str(size), content or ""]
        digest.update("\0".join(fields).encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def launcher_framed_tree_digest(root: Path) -> str:
    """Independent implementation of the launcher contract's framed tree hash."""
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
                raise RuntimeError(f"unsupported linked or special entry: {path}")
    for relative, path_kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(path_kind.encode() + b"\0")
        if path_kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    global failures
    failures += 1


data = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
failures = 0

print(f"record_layout={data.get('record_layout')}")
print(f"semantics_mode={data.get('semantics_mode')}")

required_files = [
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
]
if Path("/generation-evidence/usage.json").exists():
    required_files.append(Path("/generation-evidence/usage.json"))

required_directories = [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
    Path("/reference/reference-semantics"),
]

for path in required_files:
    if not path.exists() or not path.is_file() or path.is_symlink():
        fail(f"required regular file invalid: {path}")
    else:
        print(f"required_file_ok={path}")

for path in required_directories:
    if not path.exists() or not path.is_dir() or path.is_symlink():
        fail(f"required directory invalid: {path}")
    else:
        print(f"required_directory_ok={path}")

lock = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
if lock != data["audit_campaign"]:
    fail("campaign lock JSON differs from audit_input.audit_campaign")
else:
    print("campaign_lock_content_match=true")

declared_hashes = data["hashes"]
file_hash_checks = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}
for path_text, key in file_hash_checks.items():
    path = Path(path_text)
    actual = sha256(path)
    expected = declared_hashes[key]
    print(f"sha256 {path} actual={actual} expected={expected}")
    if actual != expected:
        fail(f"digest mismatch for {path}")

result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
for relative, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    if not path.exists() or not path.is_file() or path.is_symlink():
        fail(f"generation-result evidence entry invalid: {relative}")
        continue
    actual = sha256(path)
    print(f"stage1_evidence_sha256 {relative} actual={actual} expected={expected}")
    if actual != expected:
        fail(f"stage1 evidence digest mismatch: {relative}")

for label, root in [
    ("candidate", Path("/candidate")),
    ("trusted_semantics", Path("/reference/reference-semantics")),
    ("candidate_semantics", Path("/candidate/reference-semantics")),
    ("generation_trace", Path("/generation-evidence/codex-trace")),
]:
    entries = tree(root)
    print(
        f"independent_tree {label} entries={len(entries)} "
        f"digest={independent_tree_digest(entries)}"
    )
    for relative, record in sorted(entries.items()):
        print(f"tree_entry {label} {relative} {record}")

generation_result = json.loads(
    Path("/generation-result.json").read_text(encoding="utf-8")
)
generation_invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
generation_usage = json.loads(
    Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
)
tree_hash_checks = [
    (
        "candidate",
        Path("/candidate"),
        generation_result["outputs"]["workspace_sha256"],
    ),
    (
        "trusted_semantics",
        Path("/reference/reference-semantics"),
        declared_hashes["trusted_reference_semantics_manifest_sha256"],
    ),
    (
        "candidate_semantics",
        Path("/candidate/reference-semantics"),
        declared_hashes["trusted_reference_semantics_manifest_sha256"],
    ),
    (
        "generation_trace",
        Path("/generation-evidence/codex-trace"),
        generation_usage["source_trace_sha256"],
    ),
]
for label, root, expected in tree_hash_checks:
    actual = launcher_framed_tree_digest(root)
    print(f"framed_tree_sha256 {label} actual={actual} expected={expected}")
    if actual != expected:
        fail(f"framed tree digest mismatch: {label}")
if (
    generation_result["outputs"]["workspace_sha256"]
    != generation_invocation["retained_workspace_sha256"]
):
    fail("generation result and invocation disagree on retained workspace digest")
else:
    print("generation_workspace_digest_records_match=true")
print(
    "launcher_owned_content_digests_recorded="
    + json.dumps(
        {
            "candidate_tree_sha256": declared_hashes["candidate_tree_sha256"],
            "candidate_reference_semantics_sha256": declared_hashes[
                "candidate_reference_semantics_sha256"
            ],
            "trusted_reference_semantics_sha256": declared_hashes[
                "trusted_reference_semantics_sha256"
            ],
            "generation_codex_trace_sha256": declared_hashes[
                "generation_codex_trace_sha256"
            ],
        },
        sort_keys=True,
    )
)

trusted_semantics = tree(Path("/reference/reference-semantics"))
candidate_semantics = tree(Path("/candidate/reference-semantics"))
if trusted_semantics != candidate_semantics:
    fail("candidate supplied-semantics tree differs from trusted tree")
    for relative in sorted(set(trusted_semantics) | set(candidate_semantics)):
        if trusted_semantics.get(relative) != candidate_semantics.get(relative):
            print(
                f"semantics_difference {relative} "
                f"candidate={candidate_semantics.get(relative)} "
                f"trusted={trusted_semantics.get(relative)}"
            )
else:
    print("candidate_semantics_exact_typed_tree_match=true")

for candidate_path, trusted_path, label in [
    (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
    (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
]:
    if kind(candidate_path) != "file":
        fail(f"candidate {label} is not a regular file")
    elif candidate_path.read_bytes() != trusted_path.read_bytes():
        fail(f"candidate {label} differs from trusted mount")
    else:
        print(f"candidate_{label}_byte_match=true")

trace_lines = 0
for path in sorted(Path("/generation-evidence/codex-trace").rglob("*")):
    if path.is_file() and not path.is_symlink():
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    json.loads(line)
                except json.JSONDecodeError as error:
                    fail(f"invalid JSONL {path}:{line_number}: {error}")
print(f"structured_trace_json_records={trace_lines}")
print(f"FAILURES={failures}")
sys.exit(1 if failures else 0)
