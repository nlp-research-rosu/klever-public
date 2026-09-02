#!/usr/bin/env python3
"""Condition-aware provenance and supplied-semantics integrity check."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def kind(path: Path) -> str:
    mode = os.lstat(path).st_mode
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    return "other"


def manifest(root: Path):
    result = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in sorted(dirs + files):
            path = base_path / name
            rel = str(path.relative_to(root))
            entry_kind = kind(path)
            item = {"kind": entry_kind}
            if entry_kind == "file":
                item["sha256"] = sha256(path)
                item["size"] = path.stat().st_size
            elif entry_kind == "symlink":
                item["target"] = os.readlink(path)
            result[rel] = item
    return result


required_candidate = [
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "spec.k",
    "verification.k",
    "reference-semantics",
]
provenance = [
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
]

candidate_semantics = manifest(CANDIDATE / "reference-semantics")
trusted_semantics = manifest(REFERENCE / "reference-semantics")
candidate_paths = set(candidate_semantics)
trusted_paths = set(trusted_semantics)
common = candidate_paths & trusted_paths

report = {
    "rendered_mode": "SUPPLIED_SEMANTICS",
    "trusted_reference_semantics_present": (
        REFERENCE / "reference-semantics"
    ).is_dir(),
    "required_candidate_artifacts": {
        name: (
            {"present": True, "kind": kind(CANDIDATE / name)}
            if os.path.lexists(CANDIDATE / name)
            else {"present": False}
        )
        for name in required_candidate
    },
    "provenance_artifacts": {
        name: (
            {"present": True, "kind": kind(CANDIDATE / name)}
            if os.path.lexists(CANDIDATE / name)
            else {"present": False}
        )
        for name in provenance
    },
    "structured_trace_candidates": sorted(
        str(path.relative_to(CANDIDATE))
        for path in CANDIDATE.rglob("*")
        if path.is_file()
        and (
            "trace" in path.name.lower()
            or path.suffix.lower() in {".jsonl", ".trace"}
        )
    ),
    "prompt_byte_equal": (
        (CANDIDATE / "prompt.py").read_bytes()
        == (REFERENCE / "prompt.py").read_bytes()
    ),
    "translator_byte_equal": (
        (CANDIDATE / "py2mpy.py").read_bytes()
        == (REFERENCE / "py2mpy.py").read_bytes()
    ),
    "semantics": {
        "trusted_entry_count": len(trusted_semantics),
        "candidate_entry_count": len(candidate_semantics),
        "missing_paths": sorted(trusted_paths - candidate_paths),
        "additional_paths": sorted(candidate_paths - trusted_paths),
        "type_mismatches": sorted(
            rel
            for rel in common
            if trusted_semantics[rel]["kind"] != candidate_semantics[rel]["kind"]
        ),
        "content_mismatches": sorted(
            rel
            for rel in common
            if trusted_semantics[rel]["kind"] == "file"
            and candidate_semantics[rel]["kind"] == "file"
            and trusted_semantics[rel]["sha256"]
            != candidate_semantics[rel]["sha256"]
        ),
        "candidate_symlinks": sorted(
            rel
            for rel, item in candidate_semantics.items()
            if item["kind"] == "symlink"
        ),
    },
}
report["semantics"]["exact"] = not any(
    report["semantics"][key]
    for key in (
        "missing_paths",
        "additional_paths",
        "type_mismatches",
        "content_mismatches",
        "candidate_symlinks",
    )
)
print(json.dumps(report, indent=2))

required_ok = all(
    item.get("present") and item.get("kind") in {"file", "directory"}
    for item in report["required_candidate_artifacts"].values()
)
raise SystemExit(
    0
    if (
        report["trusted_reference_semantics_present"]
        and required_ok
        and report["prompt_byte_equal"]
        and report["translator_byte_equal"]
        and report["semantics"]["exact"]
    )
    else 1
)
