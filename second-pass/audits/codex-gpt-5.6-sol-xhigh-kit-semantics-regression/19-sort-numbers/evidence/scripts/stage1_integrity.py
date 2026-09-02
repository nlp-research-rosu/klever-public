#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import stat


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    return f"other({stat.S_IFMT(mode):o})"


def tree_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    manifest: dict[str, tuple[str, str | None]] = {}
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirnames + filenames):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            kind = entry_kind(path)
            digest = sha256(path) if kind == "file" else None
            manifest[rel] = (kind, digest)
    return manifest


def summarize_large_log(path: Path) -> None:
    raw = path.read_text(errors="replace")
    lines = raw.splitlines()
    patterns = {
        "kprove": r"\bkprove\b",
        "kompile": r"\bkompile\b",
        "top": r"#Top",
        "mutation": r"mutation",
        "final_result": r"RESULT:|VERDICT:|LEGITIMACY:",
    }
    print(f"{path.name}: bytes={path.stat().st_size} lines={len(lines)} sha256={sha256(path)}")
    print("  pattern_counts=" + json.dumps(
        {name: len(re.findall(pattern, raw, flags=re.IGNORECASE)) for name, pattern in patterns.items()},
        sort_keys=True,
    ))
    print("  first_lines=" + json.dumps(lines[:5]))
    print("  last_lines=" + json.dumps(lines[-8:]))


required_regular = [
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

print("REQUIRED_ARTIFACT_TYPES")
type_failures = []
for name in required_regular:
    path = CANDIDATE / name
    kind = "missing" if not path.exists() and not path.is_symlink() else entry_kind(path)
    print(f"{name}\t{kind}")
    if kind != "file":
        type_failures.append((name, kind))

trace_files = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
print(f"structured_trace_count={len(trace_files)}")
for path in trace_files:
    print(f"structured_trace={path}\ttype={entry_kind(path)}\tsha256={sha256(path)}")

print("\nTRUSTED_FILE_COMPARISONS")
for name in ("prompt.py", "py2mpy.py"):
    trusted = REFERENCE / name
    submitted = CANDIDATE / name
    same = trusted.read_bytes() == submitted.read_bytes()
    print(
        f"{name}\tbyte_identical={same}\t"
        f"trusted_sha256={sha256(trusted)}\tcandidate_sha256={sha256(submitted)}"
    )

trusted_root = REFERENCE / "reference-semantics"
candidate_root = CANDIDATE / "reference-semantics"
print(f"trusted_semantics_present={trusted_root.is_dir()}")
trusted_manifest = tree_manifest(trusted_root)
candidate_manifest = tree_manifest(candidate_root)
missing = sorted(set(trusted_manifest) - set(candidate_manifest))
additional = sorted(set(candidate_manifest) - set(trusted_manifest))
changed = sorted(
    rel
    for rel in set(trusted_manifest) & set(candidate_manifest)
    if trusted_manifest[rel] != candidate_manifest[rel]
)
symlinked = sorted(
    rel for rel, (kind, _) in candidate_manifest.items() if kind == "symlink"
)
print(f"semantics_entries_trusted={len(trusted_manifest)}")
print(f"semantics_entries_candidate={len(candidate_manifest)}")
print(f"semantics_missing={json.dumps(missing)}")
print(f"semantics_additional={json.dumps(additional)}")
print(f"semantics_changed_or_mistyped={json.dumps(changed)}")
print(f"semantics_symlinked={json.dumps(symlinked)}")

print("\nUNTRUSTED_JSON_CLAIMS")
for name in ("run-input.json", "metrics.json"):
    path = CANDIDATE / name
    print(f"{name}={json.dumps(json.loads(path.read_text()), sort_keys=True)}")

print("\nUNTRUSTED_TEXT_CLAIMS")
last = CANDIDATE / "codex-last.txt"
print(f"codex-last.txt: sha256={sha256(last)} text={json.dumps(last.read_text(errors='replace'))}")
summarize_large_log(CANDIDATE / "codex-output.log")

print("\nSTRUCTURED_TRACE_SUMMARY")
for path in trace_files:
    types: dict[str, int] = {}
    relevant = 0
    parse_errors = 0
    final_fragments: list[str] = []
    with path.open(errors="replace") as stream:
        for line in stream:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                parse_errors += 1
                continue
            event_type = str(item.get("type", "<none>"))
            types[event_type] = types.get(event_type, 0) + 1
            serialized = json.dumps(item, sort_keys=True)
            if re.search(r"kprove|kompile|#Top|spec-vacuity|VERDICT|LEGITIMACY", serialized, re.I):
                relevant += 1
            if "RESULT: KPROVE" in serialized:
                final_fragments.append(serialized[-500:])
    print(
        f"{path}: parse_errors={parse_errors} event_types={json.dumps(types, sort_keys=True)} "
        f"relevant_events={relevant} result_fragments={json.dumps(final_fragments[-2:])}"
    )

all_good = not (
    type_failures
    or missing
    or additional
    or changed
    or symlinked
)
print(f"\nSTAGE1_INTEGRITY_OK={all_good}")
raise SystemExit(0 if all_good else 1)
