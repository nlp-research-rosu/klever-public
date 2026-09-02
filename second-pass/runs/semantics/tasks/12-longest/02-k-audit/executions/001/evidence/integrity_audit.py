#!/usr/bin/env python3
"""Independent type/hash comparison for the supplied audit boundary."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def entry_kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_file():
        return "file"
    if path.is_dir():
        return "directory"
    if path.exists():
        return "special"
    return "missing"


def compare_file(candidate: Path, trusted: Path) -> list[str]:
    problems: list[str] = []
    ck = entry_kind(candidate)
    tk = entry_kind(trusted)
    if ck != "file":
        problems.append(f"{candidate}: expected regular file, got {ck}")
    if tk != "file":
        problems.append(f"{trusted}: trusted input is not a regular file ({tk})")
    if not problems:
        ch = digest(candidate)
        th = digest(trusted)
        print(f"FILE {candidate.name}: candidate_sha256={ch} trusted_sha256={th}")
        if ch != th:
            problems.append(f"{candidate}: content differs from {trusted}")
    return problems


def walk_without_following(root: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            entries[rel] = entry_kind(path)
    return entries


def compare_tree(candidate: Path, trusted: Path) -> list[str]:
    problems: list[str] = []
    if entry_kind(candidate) != "directory":
        return [f"{candidate}: expected real directory, got {entry_kind(candidate)}"]
    if entry_kind(trusted) != "directory":
        return [f"{trusted}: trusted baseline is not a real directory"]
    ce = walk_without_following(candidate)
    te = walk_without_following(trusted)
    all_names = sorted(set(ce) | set(te))
    for rel in all_names:
        if rel not in ce:
            problems.append(f"missing semantics entry: {rel}")
            continue
        if rel not in te:
            problems.append(f"additional semantics entry: {rel}")
            continue
        if ce[rel] != te[rel]:
            problems.append(
                f"mistyped semantics entry: {rel}: candidate={ce[rel]} trusted={te[rel]}"
            )
            continue
        if ce[rel] == "symlink":
            problems.append(f"symlinked semantics entry: {rel}")
        elif ce[rel] == "file":
            candidate_hash = digest(candidate / rel)
            trusted_hash = digest(trusted / rel)
            if candidate_hash != trusted_hash:
                problems.append(f"changed semantics file: {rel}")
    print(
        f"SEMANTICS_TREE: candidate_entries={len(ce)} "
        f"trusted_entries={len(te)} compared_entries={len(all_names)}"
    )
    return problems


def main() -> int:
    problems: list[str] = []
    print("MODE: SUPPLIED_SEMANTICS")
    print(
        "TRUSTED_SEMANTICS_KIND:",
        entry_kind(REFERENCE / "reference-semantics"),
    )
    problems.extend(compare_file(CANDIDATE / "prompt.py", REFERENCE / "prompt.py"))
    problems.extend(compare_file(CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py"))
    problems.extend(
        compare_tree(
            CANDIDATE / "reference-semantics",
            REFERENCE / "reference-semantics",
        )
    )

    required_candidate = [
        "solution.py",
        "solution.mpy",
        "spec.k",
        "verification.k",
        "prompt.py",
        "py2mpy.py",
    ]
    for name in required_candidate:
        kind = entry_kind(CANDIDATE / name)
        print(f"REQUIRED_ARTIFACT {name}: {kind}")
        if kind != "file":
            problems.append(f"required candidate artifact {name}: got {kind}")

    untrusted_claim_files = [
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ]
    for name in untrusted_claim_files:
        kind = entry_kind(CANDIDATE / name)
        print(f"GENERATION_METADATA {name}: {kind}")
        if kind != "file":
            problems.append(f"missing generation metadata: {name}")

    trace_names = sorted(
        path.name
        for path in CANDIDATE.iterdir()
        if "trace" in path.name.lower() and entry_kind(path) == "file"
    )
    print("STRUCTURED_TRACE_FILES:", trace_names if trace_names else "none")
    if not trace_names:
        problems.append("missing structured generation trace")

    print(f"PROBLEM_COUNT: {len(problems)}")
    for problem in problems:
        print(f"PROBLEM: {problem}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
