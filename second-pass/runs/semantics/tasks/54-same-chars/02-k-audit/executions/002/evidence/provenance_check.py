#!/usr/bin/env python3
"""Independent provenance and mounted-input integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def reviewer_tree_digest(root: Path) -> str:
    """Hash entry kind, relative path, mode, and regular-file bytes."""
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode()
        st = path.lstat()
        if stat.S_ISLNK(st.st_mode):
            kind = b"L"
            payload = os.readlink(path).encode()
        elif stat.S_ISDIR(st.st_mode):
            kind = b"D"
            payload = b""
        elif stat.S_ISREG(st.st_mode):
            kind = b"F"
            payload = path.read_bytes()
        else:
            kind = b"O"
            payload = b""
        digest.update(kind + b"\0" + relative + b"\0")
        digest.update(f"{stat.S_IMODE(st.st_mode):04o}".encode() + b"\0")
        digest.update(len(payload).to_bytes(8, "big") + payload)
    return digest.hexdigest()


def launcher_tree_digest(root: Path) -> str:
    """Reimplement the recorded pipeline tree-hash format."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        st = path.lstat()
        relative = path.relative_to(root).as_posix()
        if stat.S_ISDIR(st.st_mode):
            entries.append((relative, "directory", path))
        elif stat.S_ISREG(st.st_mode):
            entries.append((relative, "file", path))
        else:
            raise AssertionError(f"unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            payload = path.read_bytes()
            digest.update(len(payload).to_bytes(8, "big"))
            digest.update(payload)
    return digest.hexdigest()


def legacy_tree_digest(root: Path) -> str:
    """Reimplement the historical path/kind/content tree-hash format."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        st = path.lstat()
        relative = path.relative_to(root).as_posix()
        if stat.S_ISDIR(st.st_mode):
            entries.append((relative, "directory", path))
        elif stat.S_ISREG(st.st_mode):
            entries.append((relative, "file", path))
        else:
            raise AssertionError(f"unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    print(("PASS " if condition else "FAIL ") + message)
    if not condition:
        failures.append(message)


def compare_trees(left: Path, right: Path) -> None:
    left_entries = {
        p.relative_to(left).as_posix(): p
        for p in left.rglob("*")
    }
    right_entries = {
        p.relative_to(right).as_posix(): p
        for p in right.rglob("*")
    }
    require(set(left_entries) == set(right_entries), "candidate/trusted semantics entry sets match")
    for rel in sorted(set(left_entries) | set(right_entries)):
        if rel not in left_entries or rel not in right_entries:
            continue
        lp, rp = left_entries[rel], right_entries[rel]
        ls, rs = lp.lstat(), rp.lstat()
        lkind = stat.S_IFMT(ls.st_mode)
        rkind = stat.S_IFMT(rs.st_mode)
        require(lkind == rkind, f"entry kind matches: {rel}")
        require(not stat.S_ISLNK(ls.st_mode), f"candidate semantics entry is not symlink: {rel}")
        if stat.S_ISREG(ls.st_mode) and stat.S_ISREG(rs.st_mode):
            require(lp.read_bytes() == rp.read_bytes(), f"file bytes match: {rel}")


failures: list[str] = []
audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())

require(audit["record_layout"] == "legacy-selected-stage1", "declared record layout is legacy-selected-stage1")
require(audit["semantics_mode"] == "SUPPLIED_SEMANTICS", "declared semantics mode is SUPPLIED_SEMANTICS")
require((REFERENCE / "reference-semantics").is_dir(), "trusted supplied semantics mount is present")
require(lock == audit["audit_campaign"], "campaign lock structurally equals audit-input campaign block")
require(
    sha256_file(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"],
    "campaign lock byte hash matches audit-input",
)

fixed_hashes = {
    REFERENCE / "canonical.py": "canonical_sha256",
    REFERENCE / "prompt.py": "trusted_prompt_sha256",
    REFERENCE / "py2mpy.py": "trusted_translator_sha256",
    CANDIDATE / "prompt.py": "candidate_prompt_sha256",
    CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    GENERATION / "invocation.json": "stage1_invocation_sha256",
    GENERATION / "metrics.json": "generation_metrics_sha256",
    GENERATION / "usage.json": "generation_usage_sha256",
    GENERATION / "codex-last.txt": "generation_codex_last_sha256",
    GENERATION / "codex-output.log": "generation_codex_output_sha256",
    GENERATION / "prompt.txt": "generation_prompt_sha256",
}
for path, key in fixed_hashes.items():
    require(path.is_file() and not path.is_symlink(), f"required regular record exists: {path}")
    if path.is_file():
        require(sha256_file(path) == audit["hashes"][key], f"record hash matches {key}")

for path in [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "usage.json",
]:
    try:
        json.loads(path.read_text())
        require(True, f"JSON parses: {path}")
    except Exception as error:
        require(False, f"JSON parses: {path}: {error}")

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads((GENERATION / "invocation.json").read_text())
for record_name, expected in result["outputs"]["evidence"].items():
    path = GENERATION / record_name
    require(path.is_file() and not path.is_symlink(), f"generation-result output exists as regular file: {record_name}")
    if path.is_file():
        require(sha256_file(path) == expected, f"generation-result hash matches: {record_name}")
        require(
            invocation["outputs"]["evidence"].get(record_name) == expected,
            f"invocation and result agree on evidence hash: {record_name}",
        )

trace_entries = sorted((GENERATION / "codex-trace").rglob("*"))
trace_files = [path for path in trace_entries if path.is_file()]
require(bool(trace_files), "structured trace is nonempty")
require(
    all((p.is_file() or p.is_dir()) and not p.is_symlink() for p in trace_entries),
    "structured trace contains only regular files and directories, with no symlinks",
)
trace_lines = 0
for path in trace_files:
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        trace_lines += 1
        try:
            json.loads(line)
        except Exception as error:
            require(False, f"trace JSON parses at {path}:{line_number}: {error}")
require(trace_lines == 132, f"structured trace has expected 132 parseable JSONL records (actual {trace_lines})")

for rel in ["solution.py", "solution.mpy", "verification.k", "spec.k", "prove.sh"]:
    path = CANDIDATE / rel
    require(path.is_file() and not path.is_symlink(), f"required candidate proof artifact is a regular file: {rel}")

require((CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes(), "candidate prompt bytes equal trusted prompt")
require((CANDIDATE / "py2mpy.py").read_bytes() == (REFERENCE / "py2mpy.py").read_bytes(), "candidate translator bytes equal trusted translator")
compare_trees(CANDIDATE / "reference-semantics", REFERENCE / "reference-semantics")

require(
    launcher_tree_digest(CANDIDATE) == result["outputs"]["workspace_sha256"],
    "mounted candidate pipeline tree hash matches generation-result",
)
require(
    launcher_tree_digest(CANDIDATE / "reference-semantics")
    == audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
    "candidate semantics pipeline tree hash matches recorded semantics manifest hash",
)
require(
    launcher_tree_digest(REFERENCE / "reference-semantics")
    == audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
    "trusted semantics pipeline tree hash matches recorded semantics manifest hash",
)
require(
    launcher_tree_digest(GENERATION / "codex-trace")
    == json.loads((GENERATION / "usage.json").read_text())["source_trace_sha256"],
    "structured trace pipeline tree hash matches usage source-trace hash",
)
print(f"recorded candidate secure digest: {audit['hashes']['candidate_tree_sha256']}")
print(f"recorded semantics secure digest: {audit['hashes']['trusted_reference_semantics_sha256']}")
print(f"recorded trace secure digest: {audit['hashes']['generation_codex_trace_sha256']}")
print(f"reviewer candidate-semantics digest: {reviewer_tree_digest(CANDIDATE / 'reference-semantics')}")
print(f"reviewer trusted-semantics digest:   {reviewer_tree_digest(REFERENCE / 'reference-semantics')}")
print(f"failure_count={len(failures)}")
sys.exit(1 if failures else 0)
