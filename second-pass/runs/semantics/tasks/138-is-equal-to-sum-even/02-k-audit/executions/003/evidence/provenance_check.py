#!/usr/bin/env python3
"""Independent mounted-input and legacy-selected-stage1 integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_manifest_tree(root: Path) -> str:
    """Reimplement the launcher manifest-tree digest without importing its code."""
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"not a real directory: {root}")
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
                raise ValueError(f"linked or unsupported entry: {path}")
    digest = hashlib.sha256()
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


def regular_file(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except OSError:
        return False


def compare_trees(left: Path, right: Path) -> list[str]:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        out: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                out[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                out[rel] = ("file", sha256_file(path))
            elif stat.S_ISLNK(mode):
                out[rel] = ("symlink", os.readlink(path))
            else:
                out[rel] = ("special", None)
        return out

    a, b = inventory(left), inventory(right)
    findings = []
    for rel in sorted(set(a) | set(b)):
        if a.get(rel) != b.get(rel):
            findings.append(f"{rel}: candidate={a.get(rel)!r} trusted={b.get(rel)!r}")
    return findings


def check(name: str, actual: object, expected: object) -> bool:
    passed = actual == expected
    print(f"{name}: {'PASS' if passed else 'FAIL'}")
    print(f"  actual:   {actual}")
    print(f"  expected: {expected}")
    return passed


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    hashes = audit["hashes"]
    paths = audit["container_paths"]
    ok = True

    ok &= check("record_layout", audit["record_layout"], "legacy-selected-stage1")
    ok &= check("semantics_mode", audit["semantics_mode"], "SUPPLIED_SEMANTICS")
    ok &= check("reference semantics present", Path("/reference/reference-semantics").is_dir(), True)

    lock = Path(paths["audit_campaign_lock"])
    lock_doc = json.loads(lock.read_text())
    ok &= check("campaign lock object", lock_doc, audit["audit_campaign"])
    ok &= check("campaign lock sha256", sha256_file(lock), hashes["audit_campaign_lock_sha256"])

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    for path in required:
        passed = regular_file(path)
        print(f"required regular record {path}: {'PASS' if passed else 'FAIL'}")
        ok &= passed
    usage = Path("/generation-evidence/usage.json")
    print(f"optional historical usage record present: {regular_file(usage)}")

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
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    }
    for path, key in direct_hashes.items():
        ok &= check(f"sha256 {path}", sha256_file(path), hashes[key])

    trace_root = Path(paths["generation_trace"])
    trace_files = sorted(p for p in trace_root.rglob("*") if p.is_file())
    print(f"structured trace regular files: {len(trace_files)}")
    for path in trace_files:
        print(f"  {path.relative_to(trace_root)} {sha256_file(path)}")
    ok &= check(
        "structured trace manifest digest",
        sha256_manifest_tree(trace_root),
        json.loads(usage.read_text())["source_trace_sha256"],
    )

    result = json.loads(Path("/generation-result.json").read_text())
    evidence_hashes = result["outputs"]["evidence"]
    for rel, expected in sorted(evidence_hashes.items()):
        path = Path("/generation-evidence") / rel
        passed = regular_file(path)
        print(f"declared evidence record {rel}: {'PRESENT' if passed else 'MISSING/NOT-REGULAR'}")
        ok &= passed
        if passed:
            ok &= check(f"generation-result hash {rel}", sha256_file(path), expected)

    ok &= check(
        "candidate workspace manifest digest",
        sha256_manifest_tree(Path("/candidate")),
        result["outputs"]["workspace_sha256"],
    )
    ok &= check(
        "trusted semantics manifest digest",
        sha256_manifest_tree(Path("/reference/reference-semantics")),
        hashes["trusted_reference_semantics_manifest_sha256"],
    )
    ok &= check(
        "candidate semantics manifest digest",
        sha256_manifest_tree(Path("/candidate/reference-semantics")),
        hashes["trusted_reference_semantics_manifest_sha256"],
    )
    differences = compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    print(f"candidate/trusted semantics differences: {len(differences)}")
    for difference in differences:
        print(f"  {difference}")
    ok &= not differences

    ok &= check(
        "candidate prompt bytes equal trusted",
        Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes(),
        True,
    )
    ok &= check(
        "candidate translator bytes equal trusted",
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes(),
        True,
    )

    print(f"OVERALL: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
