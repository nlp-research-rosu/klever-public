#!/usr/bin/env python3
"""Independent, read-only provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    """Return relative path -> (kind, content/link hash), never following links."""
    result: dict[str, tuple[str, str | None]] = {}
    for directory, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        base = Path(directory)
        names = sorted(dirnames + filenames)
        for name in names:
            path = base / name
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[relative] = ("symlink", hashlib.sha256(os.readlink(path).encode()).hexdigest())
                if name in dirnames:
                    dirnames.remove(name)
            elif stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256_file(path))
            else:
                result[relative] = (f"special:{stat.S_IFMT(mode):o}", None)
    return result


def inventory_digest(items: dict[str, tuple[str, str | None]]) -> str:
    encoded = json.dumps(items, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def report_file(label: str, path: Path, expected: str | None = None) -> bool:
    if not path.exists() or not path.is_file() or path.is_symlink():
        print(f"{label}: INVALID path={path}")
        return False
    actual = sha256_file(path)
    verdict = "MATCH" if expected is None or actual == expected else "MISMATCH"
    print(f"{label}: {verdict} sha256={actual} expected={expected or '-'} path={path}")
    return verdict == "MATCH"


def main() -> int:
    audit_input = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    hashes = audit_input["hashes"]
    paths = audit_input["container_paths"]

    ok = True
    print(f"record_layout={audit_input['record_layout']}")
    print(f"semantics_mode={audit_input['semantics_mode']}")
    print(f"mount_reference_semantics={audit_input['mount_reference_semantics']}")

    campaign_match = lock == audit_input["audit_campaign"]
    print(f"campaign_block_exact_match={campaign_match}")
    ok &= campaign_match
    ok &= report_file("audit_campaign_lock", LOCK, hashes["audit_campaign_lock_sha256"])

    required_paths = {
        "audit_input": AUDIT_INPUT,
        "audit_campaign_lock": Path(paths["audit_campaign_lock"]),
        "candidate": Path(paths["candidate"]),
        "canonical": Path(paths["canonical"]),
        "trusted_prompt": Path(paths["trusted_prompt"]),
        "translator": Path(paths["translator"]),
        "run_manifest": Path(paths["run_manifest"]),
        "task_manifest": Path(paths["task_manifest"]),
        "stage1_result": Path(paths["stage1_result"]),
        "generation_manifest": Path(paths["generation_manifest"]),
        "generation_metrics": Path(paths["generation_metrics"]),
        "generation_last": Path(paths["generation_last"]),
        "generation_output": Path(paths["generation_output"]),
        "generation_prompt": Path(paths["generation_root"]) / "prompt.txt",
        "generation_trace": Path(paths["generation_trace"]),
    }
    for label, path in required_paths.items():
        mode = path.lstat().st_mode if path.exists() or path.is_symlink() else None
        usable = (
            mode is not None
            and not stat.S_ISLNK(mode)
            and (stat.S_ISREG(mode) or stat.S_ISDIR(mode))
            and os.access(path, os.R_OK)
        )
        print(f"required {label}: {'OK' if usable else 'INVALID'} path={path}")
        ok &= usable

    expected_file_hashes = {
        "canonical": (Path(paths["canonical"]), hashes["canonical_sha256"]),
        "trusted_prompt": (Path(paths["trusted_prompt"]), hashes["trusted_prompt_sha256"]),
        "trusted_translator": (Path(paths["translator"]), hashes["trusted_translator_sha256"]),
        "candidate_prompt": (Path(paths["candidate"]) / "prompt.py", hashes["candidate_prompt_sha256"]),
        "candidate_translator": (Path(paths["candidate"]) / "py2mpy.py", hashes["candidate_translator_sha256"]),
        "run_manifest": (Path(paths["run_manifest"]), hashes["run_manifest_sha256"]),
        "task_manifest": (Path(paths["task_manifest"]), hashes["task_manifest_sha256"]),
        "stage1_result": (Path(paths["stage1_result"]), hashes["stage1_result_sha256"]),
        "stage1_invocation": (Path(paths["generation_manifest"]), hashes["stage1_invocation_sha256"]),
        "generation_metrics": (Path(paths["generation_metrics"]), hashes["generation_metrics_sha256"]),
        "generation_last": (Path(paths["generation_last"]), hashes["generation_codex_last_sha256"]),
        "generation_output": (Path(paths["generation_output"]), hashes["generation_codex_output_sha256"]),
        "generation_prompt": (Path(paths["generation_root"]) / "prompt.txt", hashes["generation_prompt_sha256"]),
        "generation_usage": (Path(paths["generation_root"]) / "usage.json", hashes["generation_usage_sha256"]),
    }
    for label, (path, expected) in expected_file_hashes.items():
        ok &= report_file(label, path, expected)

    candidate_prompt_equal = (
        (Path(paths["candidate"]) / "prompt.py").read_bytes()
        == Path(paths["trusted_prompt"]).read_bytes()
    )
    translator_equal = (
        (Path(paths["candidate"]) / "py2mpy.py").read_bytes()
        == Path(paths["translator"]).read_bytes()
    )
    print(f"candidate_prompt_byte_equal={candidate_prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    ok &= candidate_prompt_equal and translator_equal

    candidate_tree = inventory(Path(paths["candidate"]))
    print(f"candidate_tree_entry_count={len(candidate_tree)}")
    print(f"candidate_tree_independent_digest={inventory_digest(candidate_tree)}")
    candidate_tree_bad_types = [
        (relative, value)
        for relative, value in candidate_tree.items()
        if value[0] not in {"file", "directory"}
    ]
    print(f"candidate_tree_symlink_or_special_count={len(candidate_tree_bad_types)}")
    for relative, value in candidate_tree_bad_types:
        print(f"CANDIDATE_BAD_TYPE {relative}: {value}")
    ok &= not candidate_tree_bad_types

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path(paths["candidate"]) / "reference-semantics"
    trusted = inventory(trusted_semantics)
    candidate = inventory(candidate_semantics)
    print(f"trusted_semantics_entry_count={len(trusted)}")
    print(f"candidate_semantics_entry_count={len(candidate)}")
    print(f"trusted_semantics_independent_digest={inventory_digest(trusted)}")
    print(f"candidate_semantics_independent_digest={inventory_digest(candidate)}")
    differences = []
    for relative in sorted(set(trusted) | set(candidate)):
        if trusted.get(relative) != candidate.get(relative):
            differences.append((relative, trusted.get(relative), candidate.get(relative)))
    print(f"semantics_difference_count={len(differences)}")
    for relative, expected, actual in differences:
        print(f"SEMANTICS_DIFF {relative}: trusted={expected} candidate={actual}")
    symlinks_or_special = [
        (relative, value)
        for relative, value in candidate.items()
        if value[0] not in {"file", "directory"}
    ]
    print(f"candidate_semantics_symlink_or_special_count={len(symlinks_or_special)}")
    for relative, value in symlinks_or_special:
        print(f"SEMANTICS_BAD_TYPE {relative}: {value}")
    ok &= not differences and not symlinks_or_special

    evidence_files = {
        path.relative_to(Path(paths["generation_root"])).as_posix(): sha256_file(path)
        for path in Path(paths["generation_root"]).rglob("*")
        if path.is_file() and not path.is_symlink()
    }
    print(f"generation_evidence_file_count={len(evidence_files)}")
    result = json.loads(Path(paths["stage1_result"]).read_text())
    declared_evidence = result["outputs"]["evidence"]
    for relative, expected in sorted(declared_evidence.items()):
        actual = evidence_files.get(relative)
        match = actual == expected
        print(
            f"declared_evidence {relative}: {'MATCH' if match else 'MISMATCH'} "
            f"sha256={actual} expected={expected}"
        )
        ok &= match

    trace_inventory = inventory(Path(paths["generation_trace"]))
    print(f"generation_trace_independent_digest={inventory_digest(trace_inventory)}")
    print(f"FINAL_INFRASTRUCTURE_INTEGRITY={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
