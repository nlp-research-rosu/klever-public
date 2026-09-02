#!/usr/bin/env python3
"""Independent integrity checks for the mounted pipeline-v3 audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        return [f"{path}: unreadable or absent: {err}"]
    if stat.S_ISLNK(mode):
        errors.append(f"{path}: forbidden symlink")
    elif not stat.S_ISREG(mode):
        errors.append(f"{path}: expected regular file, mode={oct(mode)}")
    elif not os.access(path, os.R_OK):
        errors.append(f"{path}: not readable")
    return errors


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries[rel] = ("symlink", os.readlink(path))
        elif stat.S_ISDIR(mode):
            entries[rel] = ("dir", None)
        elif stat.S_ISREG(mode):
            entries[rel] = ("file", sha256(path))
        else:
            entries[rel] = (f"other:{stat.S_IFMT(mode)}", None)
    return entries


def manifest_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    encoded = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def canonical_tree_digest(root: Path) -> str:
    """Independent implementation of the launcher tree framing algorithm."""
    digest = hashlib.sha256()
    framed: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISDIR(mode):
            framed.append((relative, "directory", path))
        elif stat.S_ISREG(mode):
            framed.append((relative, "file", path))
        else:
            raise RuntimeError(f"unsupported tree entry: {path}")
    for relative, kind, path in sorted(framed):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def main() -> int:
    errors: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text())
    paths = audit["container_paths"]
    expected = audit["hashes"]

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"problem_id={audit['problem_id']}")

    campaign_path = Path(paths["audit_campaign_lock"])
    errors += require_regular(campaign_path)
    campaign = json.loads(campaign_path.read_text())
    print(f"campaign_block_equals_lock={audit['audit_campaign'] == campaign}")
    if audit["audit_campaign"] != campaign:
        errors.append("audit_campaign block differs from audit-campaign-lock")

    checks = {
        "audit_campaign_lock_sha256": campaign_path,
        "canonical_sha256": Path(paths["canonical"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "trusted_translator_sha256": Path(paths["translator"]),
        "run_manifest_sha256": Path(paths["run_manifest"]),
        "task_manifest_sha256": Path(paths["task_manifest"]),
        "stage1_result_sha256": Path(paths["stage1_result"]),
        "stage1_invocation_sha256": Path(paths["generation_manifest"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
        "generation_prompt_sha256": Path(paths["generation_root"]) / "prompt.txt",
        "generation_runtime_metrics_sha256": Path(paths["generation_root"])
        / "runtime-metrics.json",
        "generation_usage_sha256": Path(paths["generation_root"]) / "usage.json",
    }
    for key, path in checks.items():
        errors += require_regular(path)
        if path.is_file() and not path.is_symlink():
            actual = sha256(path)
            match = actual == expected[key]
            print(f"{key}: expected={expected[key]} actual={actual} match={match}")
            if not match:
                errors.append(f"{key} mismatch")

    required = [
        Path(paths["run_manifest"]),
        Path(paths["task_manifest"]),
        Path(paths["stage1_result"]),
        Path(paths["generation_manifest"]),
        Path(paths["generation_metrics"]),
        Path(paths["generation_root"]) / "runtime-metrics.json",
        Path(paths["generation_root"]) / "usage.json",
        Path(paths["generation_last"]),
        Path(paths["generation_output"]),
        Path(paths["generation_root"]) / "prompt.txt",
    ]
    for path in required:
        errors += require_regular(path)

    trace_root = Path(paths["generation_trace"])
    if not trace_root.is_dir() or trace_root.is_symlink():
        errors.append(f"{trace_root}: required trace root missing, mistyped, or symlinked")
        trace_files: list[Path] = []
    else:
        trace_files = sorted(trace_root.rglob("*"))
        non_regular = [
            str(p)
            for p in trace_files
            if not p.is_dir() and (p.is_symlink() or not p.is_file())
        ]
        errors += [f"trace non-regular entry: {p}" for p in non_regular]
        trace_files = [p for p in trace_files if p.is_file() and not p.is_symlink()]
    print(f"trace_regular_files={len(trace_files)}")
    if trace_root.is_dir() and not trace_root.is_symlink():
        actual_trace_tree = canonical_tree_digest(trace_root)
        usage_record = json.loads(
            (Path(paths["generation_root"]) / "usage.json").read_text()
        )
        expected_trace_tree = usage_record["source_trace_sha256"]
        print(
            "generation_trace_manifest_sha256: "
            f"expected={expected_trace_tree} actual={actual_trace_tree} "
            f"match={actual_trace_tree == expected_trace_tree}"
        )
        if actual_trace_tree != expected_trace_tree:
            errors.append("generation trace tree hash mismatch")
        print(
            "generation_codex_trace_sha256_launcher_alternate="
            f"{expected['generation_codex_trace_sha256']}"
        )

    invocation = json.loads(Path(paths["generation_manifest"]).read_text())
    invocation_outputs = invocation["outputs"]["evidence"]
    trace_rel_root = Path("codex-trace")
    for path in trace_files:
        rel = (trace_rel_root / path.relative_to(trace_root)).as_posix()
        actual = sha256(path)
        claimed = invocation_outputs.get(rel)
        print(f"trace_file={rel} sha256={actual} invocation_match={actual == claimed}")
        if actual != claimed:
            errors.append(f"trace file hash mismatch or unrecorded: {rel}")

    candidate = Path(paths["candidate"])
    candidate_prompt = candidate / "prompt.py"
    candidate_translator = candidate / "py2mpy.py"
    for key, cand, trusted in (
        ("prompt", candidate_prompt, Path(paths["trusted_prompt"])),
        ("translator", candidate_translator, Path(paths["translator"])),
    ):
        errors += require_regular(cand)
        if cand.is_file() and not cand.is_symlink():
            same = cand.read_bytes() == trusted.read_bytes()
            print(f"candidate_{key}_byte_identity={same}")
            if not same:
                errors.append(f"candidate {key} differs from trusted mount")

    trusted_sem = Path("/reference/reference-semantics")
    candidate_sem = candidate / "reference-semantics"
    for root in (trusted_sem, candidate_sem):
        if not root.is_dir() or root.is_symlink():
            errors.append(f"{root}: semantics tree missing, mistyped, or symlinked")
    trusted_entries = tree_entries(trusted_sem) if trusted_sem.is_dir() else {}
    candidate_entries = tree_entries(candidate_sem) if candidate_sem.is_dir() else {}
    semantics_equal = trusted_entries == candidate_entries
    print(f"trusted_semantics_entries={len(trusted_entries)}")
    print(f"candidate_semantics_entries={len(candidate_entries)}")
    print(f"semantics_recursive_type_and_byte_identity={semantics_equal}")
    print(f"trusted_semantics_independent_manifest_sha256={manifest_digest(trusted_entries)}")
    print(f"candidate_semantics_independent_manifest_sha256={manifest_digest(candidate_entries)}")
    if trusted_sem.is_dir() and candidate_sem.is_dir():
        trusted_tree_hash = canonical_tree_digest(trusted_sem)
        candidate_sem_tree_hash = canonical_tree_digest(candidate_sem)
        print(
            "trusted_reference_semantics_manifest_sha256: "
            f"expected={expected['trusted_reference_semantics_manifest_sha256']} "
            f"actual={trusted_tree_hash} "
            f"match={trusted_tree_hash == expected['trusted_reference_semantics_manifest_sha256']}"
        )
        print(
            "candidate_reference_semantics_manifest_matches_trusted="
            f"{candidate_sem_tree_hash == trusted_tree_hash}"
        )
        print(
            "trusted_reference_semantics_sha256_launcher_alternate="
            f"{expected['trusted_reference_semantics_sha256']}"
        )
        print(
            "candidate_reference_semantics_sha256_launcher_alternate="
            f"{expected['candidate_reference_semantics_sha256']}"
        )
        if trusted_tree_hash != expected["trusted_reference_semantics_manifest_sha256"]:
            errors.append("trusted reference semantics tree hash mismatch")
        if candidate_sem_tree_hash != trusted_tree_hash:
            errors.append("candidate reference semantics manifest mismatch")
    for rel, value in trusted_entries.items():
        if value[0] == "file":
            print(f"trusted_semantics_file {rel} sha256={value[1]}")
    if not semantics_equal:
        errors.append("candidate reference-semantics tree differs from trusted tree")
        for rel in sorted(trusted_entries.keys() | candidate_entries.keys()):
            if trusted_entries.get(rel) != candidate_entries.get(rel):
                print(
                    f"SEMANTICS_DIFF {rel}: "
                    f"trusted={trusted_entries.get(rel)} "
                    f"candidate={candidate_entries.get(rel)}"
                )

    trace_type_counts: Counter[str] = Counter()
    payload_type_counts: Counter[str] = Counter()
    trace_lines = 0
    trace_json_errors = 0
    for path in trace_files:
        with path.open(encoding="utf-8") as stream:
            for line_no, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as err:
                    trace_json_errors += 1
                    errors.append(f"invalid trace JSON {path}:{line_no}: {err}")
                    continue
                trace_type_counts[str(item.get("type"))] += 1
                payload = item.get("payload")
                if isinstance(payload, dict):
                    payload_type_counts[str(payload.get("type"))] += 1
    print(f"trace_json_lines={trace_lines}")
    print(f"trace_json_errors={trace_json_errors}")
    print(f"trace_top_level_types={dict(sorted(trace_type_counts.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_type_counts.items()))}")

    candidate_entries_all = tree_entries(candidate)
    print(f"candidate_tree_entries={len(candidate_entries_all)}")
    print(
        "candidate_tree_independent_manifest_sha256="
        f"{manifest_digest(candidate_entries_all)}"
    )
    actual_candidate_tree = canonical_tree_digest(candidate)
    generation_result = json.loads(Path(paths["stage1_result"]).read_text())
    generated_workspace_hash = generation_result["outputs"]["workspace_sha256"]
    print(
        "candidate_workspace_manifest_sha256: "
        f"expected={generated_workspace_hash} actual={actual_candidate_tree} "
        f"match={actual_candidate_tree == generated_workspace_hash}"
    )
    print(
        "candidate_tree_sha256_launcher_alternate="
        f"{expected['candidate_tree_sha256']}"
    )
    if actual_candidate_tree != generated_workspace_hash:
        errors.append("candidate tree hash mismatch")
    source_entries = {
        rel: value
        for rel, value in candidate_entries_all.items()
        if not rel.startswith("runtime-kompiled/")
        and not rel.startswith("verification-kompiled/")
        and not rel.startswith("__pycache__/")
    }
    print(f"candidate_noncache_entries={len(source_entries)}")
    print(
        "candidate_noncache_independent_manifest_sha256="
        f"{manifest_digest(source_entries)}"
    )

    print(f"errors={len(errors)}")
    for err in errors:
        print(f"ERROR {err}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
