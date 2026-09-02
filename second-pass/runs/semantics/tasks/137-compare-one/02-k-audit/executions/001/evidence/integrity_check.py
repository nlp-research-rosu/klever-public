#!/usr/bin/env python3
"""Compare required candidate inputs to trusted inputs without following symlinks."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(directories + files):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                result[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[rel] = ("file", digest(path))
            else:
                result[rel] = (f"other:{stat.S_IFMT(mode):o}", None)
    return result


def compare_file(candidate: Path, trusted: Path, label: str) -> bool:
    if not candidate.exists() and not candidate.is_symlink():
        print(f"{label}: MISSING {candidate}")
        return False
    if candidate.is_symlink():
        print(f"{label}: INTEGRITY FAILURE: candidate is symlink -> {os.readlink(candidate)}")
        return False
    if not candidate.is_file():
        print(f"{label}: INTEGRITY FAILURE: candidate is not a regular file")
        return False
    same = digest(candidate) == digest(trusted)
    print(
        f"{label}: {'IDENTICAL' if same else 'CHANGED'} "
        f"candidate_sha256={digest(candidate)} trusted_sha256={digest(trusted)}"
    )
    return same


def main() -> int:
    okay = True
    print("SEMANTICS_MODE: SUPPLIED_SEMANTICS")
    trusted_semantics = REFERENCE / "reference-semantics"
    print(f"trusted_semantics_present={trusted_semantics.is_dir()}")
    if not trusted_semantics.is_dir():
        print("INFRASTRUCTURE_BREACH: required trusted semantics tree is absent")
        return 2

    okay &= compare_file(CANDIDATE / "prompt.py", REFERENCE / "prompt.py", "prompt")
    okay &= compare_file(CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py", "translator")

    for name in (
        "solution.py",
        "solution.mpy",
        "spec.k",
        "verification.k",
        "concrete.mpy",
        "prove.sh",
    ):
        path = CANDIDATE / name
        if path.is_symlink():
            okay = False
            print(f"REQUIRED_SOURCE: INTEGRITY FAILURE symlink {path} -> {os.readlink(path)}")
        elif not path.is_file():
            okay = False
            print(f"REQUIRED_SOURCE: MISSING_OR_MISTYPED {path}")
        else:
            print(f"REQUIRED_SOURCE: regular_file {path} sha256={digest(path)}")

    candidate_tree = inventory(CANDIDATE / "reference-semantics")
    trusted_tree = inventory(trusted_semantics)
    all_names = sorted(set(candidate_tree) | set(trusted_tree))
    mismatches = 0
    for name in all_names:
        left = trusted_tree.get(name)
        right = candidate_tree.get(name)
        if left != right:
            mismatches += 1
            print(f"SEMANTICS_MISMATCH {name}: trusted={left} candidate={right}")
    print(
        "semantics_tree: "
        f"trusted_entries={len(trusted_tree)} candidate_entries={len(candidate_tree)} "
        f"mismatches={mismatches}"
    )
    okay &= mismatches == 0

    for name in ("run-input.json", "metrics.json", "codex-last.txt", "codex-output.log"):
        path = CANDIDATE / name
        if not path.exists() and not path.is_symlink():
            print(f"UNTRUSTED_GENERATION_RECORD: MISSING {path}")
        else:
            kind = "symlink" if path.is_symlink() else "present"
            print(f"UNTRUSTED_GENERATION_RECORD: {kind} {path}")

    traces = sorted(
        p for p in CANDIDATE.iterdir()
        if p.is_file() and ("trace" in p.name.lower() or p.suffix in {".json", ".jsonl"})
    )
    print("structured_trace_files=" + (",".join(str(p) for p in traces) if traces else "NONE"))
    print(f"INTEGRITY_RESULT: {'PASS' if okay else 'FAIL'}")
    return 0 if okay else 1


if __name__ == "__main__":
    raise SystemExit(main())
