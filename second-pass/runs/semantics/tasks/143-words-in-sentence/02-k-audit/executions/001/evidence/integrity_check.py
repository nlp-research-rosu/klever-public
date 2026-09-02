#!/usr/bin/env python3
"""Independent byte/type inventory for the supplied-semantics audit boundary."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other(mode={oct(mode)})"


def compare_file(candidate: Path, trusted: Path) -> list[str]:
    findings: list[str] = []
    for label, path in (("candidate", candidate), ("trusted", trusted)):
        if not path.exists() and not path.is_symlink():
            findings.append(f"MISSING {label}: {path}")
            return findings
        if kind(path) != "file":
            findings.append(f"MISTYPED {label}: {path}: {kind(path)}")
            return findings
    candidate_hash = digest(candidate)
    trusted_hash = digest(trusted)
    status = "IDENTICAL" if candidate_hash == trusted_hash else "CHANGED"
    findings.append(
        f"{status}: {candidate} <> {trusted}: "
        f"candidate_sha256={candidate_hash} trusted_sha256={trusted_hash}"
    )
    return findings


def tree_entries(root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for current, directory_names, file_names in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in directory_names + file_names:
            path = current_path / name
            result[str(path.relative_to(root))] = path
    return result


def compare_tree(candidate_root: Path, trusted_root: Path) -> list[str]:
    findings: list[str] = []
    candidate_entries = tree_entries(candidate_root)
    trusted_entries = tree_entries(trusted_root)
    for relative in sorted(set(candidate_entries) | set(trusted_entries)):
        candidate = candidate_entries.get(relative)
        trusted = trusted_entries.get(relative)
        if candidate is None:
            findings.append(f"MISSING candidate tree entry: {relative}")
            continue
        if trusted is None:
            findings.append(f"ADDITIONAL candidate tree entry: {relative}")
            continue
        candidate_kind = kind(candidate)
        trusted_kind = kind(trusted)
        if candidate_kind != trusted_kind:
            findings.append(
                f"MISTYPED candidate tree entry: {relative}: "
                f"candidate={candidate_kind} trusted={trusted_kind}"
            )
            continue
        if candidate_kind == "symlink":
            findings.append(
                f"SYMLINKED candidate tree entry: {relative}: "
                f"target={os.readlink(candidate)}"
            )
            continue
        if candidate_kind == "file" and digest(candidate) != digest(trusted):
            findings.append(
                f"CHANGED candidate tree entry: {relative}: "
                f"candidate_sha256={digest(candidate)} trusted_sha256={digest(trusted)}"
            )
    if not findings:
        findings.append(
            f"IDENTICAL TREE: {candidate_root} <> {trusted_root}; "
            f"entries={len(candidate_entries)}; no symlinks"
        )
    return findings


def main() -> int:
    print("MODE CHECK")
    trusted_semantics = REFERENCE / "reference-semantics"
    print(
        f"/reference/reference-semantics: exists={trusted_semantics.exists()} "
        f"kind={kind(trusted_semantics) if trusted_semantics.exists() else 'missing'}"
    )

    print("\nREQUIRED/CLAIMED CANDIDATE ARTIFACTS")
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
        "reference-semantics",
    ]
    for relative in required:
        path = CANDIDATE / relative
        if path.exists() or path.is_symlink():
            print(f"PRESENT: {relative}: {kind(path)}")
        else:
            print(f"MISSING: {relative}")

    print("\nCANDIDATE TOP-LEVEL INVENTORY")
    for path in sorted(CANDIDATE.iterdir(), key=lambda item: item.name):
        print(f"{kind(path)}: {path.name}")

    print("\nPROMPT COMPARISON")
    print("\n".join(compare_file(CANDIDATE / "prompt.py", REFERENCE / "prompt.py")))

    print("\nTRANSLATOR COMPARISON")
    print("\n".join(compare_file(CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py")))

    print("\nSUPPLIED SEMANTICS COMPARISON")
    if not trusted_semantics.exists() or kind(trusted_semantics) != "directory":
        print("INFRASTRUCTURE_BREACH: trusted supplied semantics absent or mistyped")
        return 2
    candidate_semantics = CANDIDATE / "reference-semantics"
    if not candidate_semantics.exists() or kind(candidate_semantics) != "directory":
        print("INTEGRITY_FAILURE: candidate supplied semantics absent or mistyped")
        return 1
    findings = compare_tree(candidate_semantics, trusted_semantics)
    print("\n".join(findings))
    return 0 if all(item.startswith("IDENTICAL TREE") for item in findings) else 1


if __name__ == "__main__":
    raise SystemExit(main())
