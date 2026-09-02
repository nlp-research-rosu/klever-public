#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

import klean_export as producer_export


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/84-solve-proof-audit-2")
reference_base = Path("/reference/klean-generation/generated")
fresh_base = fresh / "Base"

print("## candidate source copy identity")
for relative in (
    "Proof.lean",
    "lakefile.lean",
    "lake-manifest.json",
    "lean-toolchain",
):
    print(
        f"{relative}: candidate={sha256(candidate / relative)} "
        f"fresh={sha256(fresh / relative)} "
        f"match={sha256(candidate / relative) == sha256(fresh / relative)}"
    )

print("## forbidden constructs and target shadowing")
source_paths = [
    path
    for path in candidate.rglob("*")
    if path.is_file()
    and not path.is_symlink()
    and ".lake" not in path.parts
    and "Base" not in path.parts
]
forbidden = {
    token: []
    for token in ("sorry", "admit", "unsafe", "axiom", "opaque")
}
target_declarations = []
target_namespaces = []
final_theorems = []
for path in source_paths:
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        continue
    relative = path.relative_to(candidate).as_posix()
    for token in forbidden:
        for match in re.finditer(rf"\b{token}\b", text):
            forbidden[token].append((relative, text.count("\n", 0, match.start()) + 1))
    for match in re.finditer(r"(?m)^\s*def\s+targetStatement\b", text):
        target_declarations.append((relative, text.count("\n", 0, match.start()) + 1))
    for match in re.finditer(r"(?m)^\s*namespace\s+Klean84Solve\.Lemmas\b", text):
        target_namespaces.append((relative, text.count("\n", 0, match.start()) + 1))
    for match in re.finditer(r"(?m)^\s*theorem\s+final\b", text):
        final_theorems.append((relative, text.count("\n", 0, match.start()) + 1))
print(f"source_paths={[path.relative_to(candidate).as_posix() for path in source_paths]}")
print(f"forbidden={forbidden}")
print(f"target_declarations_outside_Base={target_declarations}")
print(f"target_namespaces_outside_Base={target_namespaces}")
print(f"final_theorems={final_theorems}")

print("## generated Base source identity after clean build")
reference_files = sorted(
    path.relative_to(reference_base).as_posix()
    for path in reference_base.rglob("*")
    if path.is_file() and not path.is_symlink()
)
fresh_source_files = sorted(
    path.relative_to(fresh_base).as_posix()
    for path in fresh_base.rglob("*")
    if path.is_file()
    and not path.is_symlink()
    and ".lake" not in path.parts
)
print(f"reference_file_count={len(reference_files)}")
print(f"fresh_nonbuild_file_count={len(fresh_source_files)}")
print(f"missing={sorted(set(reference_files) - set(fresh_source_files))}")
print(f"extra={sorted(set(fresh_source_files) - set(reference_files))}")
mismatches = []
for relative in sorted(set(reference_files) & set(fresh_source_files)):
    if sha256(reference_base / relative) != sha256(fresh_base / relative):
        mismatches.append(relative)
print(f"content_mismatches={mismatches}")

computed_target = producer_export.target_statement(fresh_base)
generator_target = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)["target"]
audit_target = json.loads(Path("/audit-input.json").read_text())["resolution"]["target"]
print(f"computed_target={json.dumps(computed_target, sort_keys=True)}")
print(f"target_equals_generator={computed_target == generator_target}")
print(f"target_equals_audit_input={computed_target == audit_target}")

print("## exact candidate definitions")
proof_text = (candidate / "Proof.lean").read_text()
for line_number, line in enumerate(proof_text.splitlines(), 1):
    if re.match(r"\s*def\s+", line):
        print(f"{line_number}:{line}")
