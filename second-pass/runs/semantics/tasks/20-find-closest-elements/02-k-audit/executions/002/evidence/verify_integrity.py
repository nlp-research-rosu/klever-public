#!/usr/bin/env python3
"""Independent checks for audit manifests, mounts, hashes, and supplied semantics."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def entry_map(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in sorted(dirnames + filenames):
            path = base / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                result[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[rel] = ("file", sha256(path))
            else:
                result[rel] = ("other", f"mode={mode:o}")
    return result


def report_hash(label: str, path: Path, expected: str) -> bool:
    actual = sha256(path)
    ok = actual == expected
    print(f"{label}: path={path} actual={actual} expected={expected} ok={ok}")
    return ok


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    hashes = audit["hashes"]
    container_paths = audit["container_paths"]
    failures: list[str] = []

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")

    campaign_path = Path(container_paths["audit_campaign_lock"])
    campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
    campaign_equal = campaign == audit["audit_campaign"]
    print(f"campaign_block_exact_match={campaign_equal}")
    if not campaign_equal:
        failures.append("campaign block differs")

    if not report_hash(
        "audit_campaign_lock",
        campaign_path,
        hashes["audit_campaign_lock_sha256"],
    ):
        failures.append("audit campaign lock hash")

    for key, value in sorted(container_paths.items()):
        path = Path(value)
        readable = os.access(path, os.R_OK)
        print(
            f"container_path[{key}]={path} exists={path.exists()} "
            f"readable={readable} symlink={path.is_symlink()}"
        )
        if not path.exists() or not readable:
            failures.append(f"declared mount {key}")

    direct_hashes = {
        "canonical_sha256": Path(container_paths["canonical"]),
        "trusted_prompt_sha256": Path(container_paths["trusted_prompt"]),
        "candidate_prompt_sha256": Path(container_paths["candidate"]) / "prompt.py",
        "trusted_translator_sha256": Path(container_paths["translator"]),
        "candidate_translator_sha256": Path(container_paths["candidate"]) / "py2mpy.py",
        "run_manifest_sha256": Path(container_paths["run_manifest"]),
        "task_manifest_sha256": Path(container_paths["task_manifest"]),
        "stage1_result_sha256": Path(container_paths["stage1_result"]),
        "stage1_invocation_sha256": Path(container_paths["generation_manifest"]),
        "generation_metrics_sha256": Path(container_paths["generation_metrics"]),
        "generation_codex_last_sha256": Path(container_paths["generation_last"]),
        "generation_codex_output_sha256": Path(container_paths["generation_output"]),
        "generation_prompt_sha256": Path(container_paths["generation_root"]) / "prompt.txt",
        "generation_usage_sha256": Path(container_paths["generation_root"]) / "usage.json",
    }
    for key, path in direct_hashes.items():
        if not report_hash(key, path, hashes[key]):
            failures.append(key)

    result = json.loads(Path(container_paths["stage1_result"]).read_text(encoding="utf-8"))
    generation_root = Path(container_paths["generation_root"])
    for rel, expected in sorted(result["outputs"]["evidence"].items()):
        path = generation_root / rel
        if not path.is_file():
            print(f"stage1 evidence missing_or_nonfile={path}")
            failures.append(f"stage1 evidence {rel}")
        elif not report_hash(f"stage1.outputs.evidence[{rel}]", path, expected):
            failures.append(f"stage1 evidence hash {rel}")

    layout = audit["record_layout"]
    if layout != "legacy-selected-stage1":
        failures.append(f"unexpected layout for this audit script: {layout}")
    required_records = [
        Path(container_paths["run_manifest"]),
        Path(container_paths["task_manifest"]),
        Path(container_paths["stage1_result"]),
        generation_root / "invocation.json",
        generation_root / "metrics.json",
        generation_root / "codex-last.txt",
        generation_root / "codex-output.log",
        generation_root / "prompt.txt",
        Path(container_paths["generation_trace"]),
    ]
    if (generation_root / "usage.json").exists():
        required_records.append(generation_root / "usage.json")
    for path in required_records:
        ok = path.exists() and os.access(path, os.R_OK)
        print(f"required_record={path} ok={ok}")
        if not ok:
            failures.append(f"required record {path}")

    candidate = Path(container_paths["candidate"])
    reference_semantics = Path("/reference/reference-semantics")
    candidate_semantics = candidate / "reference-semantics"
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        failures.append("rendered semantics mode mismatch")
    print(
        f"trusted_reference_semantics present={reference_semantics.is_dir()} "
        f"candidate_reference_semantics present={candidate_semantics.is_dir()}"
    )
    if not reference_semantics.is_dir() or not candidate_semantics.is_dir():
        failures.append("supplied semantics directory absent")
    else:
        trusted_entries = entry_map(reference_semantics)
        candidate_entries = entry_map(candidate_semantics)
        only_trusted = sorted(set(trusted_entries) - set(candidate_entries))
        only_candidate = sorted(set(candidate_entries) - set(trusted_entries))
        changed = sorted(
            key
            for key in set(trusted_entries) & set(candidate_entries)
            if trusted_entries[key] != candidate_entries[key]
        )
        print(f"semantics_entry_count_trusted={len(trusted_entries)}")
        print(f"semantics_entry_count_candidate={len(candidate_entries)}")
        print(f"semantics_only_trusted={only_trusted}")
        print(f"semantics_only_candidate={only_candidate}")
        print(f"semantics_changed_or_mistyped={changed}")
        print(
            "semantics_symlinks_trusted="
            f"{sorted(k for k, v in trusted_entries.items() if v[0] == 'symlink')}"
        )
        print(
            "semantics_symlinks_candidate="
            f"{sorted(k for k, v in candidate_entries.items() if v[0] == 'symlink')}"
        )
        if only_trusted or only_candidate or changed:
            failures.append("supplied semantics recursive mismatch")

    candidate_entries = entry_map(candidate)
    candidate_symlinks = sorted(
        key for key, value in candidate_entries.items() if value[0] == "symlink"
    )
    print(f"candidate_symlinks={candidate_symlinks}")
    if candidate_symlinks:
        failures.append("candidate contains symlinks")

    for left, right, label in [
        (Path(container_paths["trusted_prompt"]), candidate / "prompt.py", "prompt"),
        (Path(container_paths["translator"]), candidate / "py2mpy.py", "translator"),
    ]:
        equal = left.read_bytes() == right.read_bytes()
        print(f"{label}_byte_identical={equal}")
        if not equal:
            failures.append(f"{label} differs")

    print(f"failures={failures}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
