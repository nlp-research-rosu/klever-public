#!/usr/bin/env python3
"""Independent candidate/trusted-input integrity checks for the audit."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import stat


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


@dataclass(frozen=True)
class Entry:
    kind: str
    digest: str | None = None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe_tree(root: Path) -> dict[str, Entry]:
    entries: dict[str, Entry] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(dirpath)
        for name in sorted(dirnames + filenames):
            path = base / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                entries[rel] = Entry("symlink")
            elif stat.S_ISDIR(mode):
                entries[rel] = Entry("directory")
            elif stat.S_ISREG(mode):
                entries[rel] = Entry("file", sha256(path))
            else:
                entries[rel] = Entry(f"other:{stat.S_IFMT(mode):o}")
    return entries


def regular_file_status(path: Path) -> str:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return "MISSING"
    if stat.S_ISLNK(mode):
        return "SYMLINK"
    if not stat.S_ISREG(mode):
        return f"MISTYPED:{stat.S_IFMT(mode):o}"
    return f"REGULAR sha256={sha256(path)}"


def main() -> int:
    failures: list[str] = []
    required = [
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
        "prompt.py",
        "py2mpy.py",
        "solution.py",
        "solution.mpy",
        "spec.k",
        "verification.k",
    ]
    print("TOP_LEVEL_REQUIRED_ARTIFACTS")
    for rel in required:
        status = regular_file_status(CANDIDATE / rel)
        print(f"{rel}: {status}")
        if not status.startswith("REGULAR"):
            failures.append(f"{rel}: {status}")

    trace_root = CANDIDATE / "codex-trace"
    trace_entries = describe_tree(trace_root) if trace_root.is_dir() else {}
    trace_files = [
        rel for rel, entry in trace_entries.items() if entry.kind == "file"
    ]
    bad_trace_types = [
        f"{rel}:{entry.kind}"
        for rel, entry in trace_entries.items()
        if entry.kind not in {"file", "directory"}
    ]
    print(f"STRUCTURED_TRACE_FILES: {len(trace_files)}")
    for rel in trace_files:
        print(f"trace/{rel}: {trace_entries[rel].digest}")
    for item in bad_trace_types:
        print(f"TRACE_TYPE_FAILURE: {item}")
        failures.append(f"trace type {item}")
    if not trace_files:
        failures.append("structured trace missing")

    print("TRUSTED_FILE_COMPARISONS")
    for rel in ("prompt.py", "py2mpy.py"):
        candidate = CANDIDATE / rel
        trusted = REFERENCE / rel
        if candidate.is_file() and trusted.is_file():
            same = candidate.read_bytes() == trusted.read_bytes()
            print(f"{rel}: byte_identical={same}")
            if not same:
                failures.append(f"{rel}: content changed")
        else:
            print(f"{rel}: comparison unavailable")
            failures.append(f"{rel}: comparison unavailable")

    trusted_semantics = REFERENCE / "reference-semantics"
    candidate_semantics = CANDIDATE / "reference-semantics"
    print("SEMANTICS_MODE_CHECK")
    print(f"trusted_reference_semantics_present={trusted_semantics.is_dir()}")
    print(f"candidate_reference_semantics_present={candidate_semantics.is_dir()}")
    if not trusted_semantics.is_dir():
        failures.append("SUPPLIED_SEMANTICS trusted tree missing")
    if not candidate_semantics.is_dir():
        failures.append("candidate semantics tree missing")
    if trusted_semantics.is_dir() and candidate_semantics.is_dir():
        trusted_tree = describe_tree(trusted_semantics)
        candidate_tree = describe_tree(candidate_semantics)
        all_paths = sorted(set(trusted_tree) | set(candidate_tree))
        for rel in all_paths:
            t_entry = trusted_tree.get(rel)
            c_entry = candidate_tree.get(rel)
            if t_entry is None:
                print(f"SEMANTICS_EXTRA: {rel} candidate={c_entry}")
                failures.append(f"semantics extra {rel}")
            elif c_entry is None:
                print(f"SEMANTICS_MISSING: {rel} trusted={t_entry}")
                failures.append(f"semantics missing {rel}")
            elif c_entry.kind == "symlink":
                print(f"SEMANTICS_SYMLINK: {rel}")
                failures.append(f"semantics symlink {rel}")
            elif t_entry.kind != c_entry.kind:
                print(
                    f"SEMANTICS_MISTYPED: {rel} "
                    f"trusted={t_entry.kind} candidate={c_entry.kind}"
                )
                failures.append(f"semantics mistyped {rel}")
            elif t_entry != c_entry:
                print(
                    f"SEMANTICS_CHANGED: {rel} "
                    f"trusted={t_entry.digest} candidate={c_entry.digest}"
                )
                failures.append(f"semantics changed {rel}")
        print(
            "SEMANTICS_TREE_SUMMARY: "
            f"trusted_entries={len(trusted_tree)} "
            f"candidate_entries={len(candidate_tree)}"
        )

    print(f"INTEGRITY_FAILURE_COUNT: {len(failures)}")
    for failure in failures:
        print(f"INTEGRITY_FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
