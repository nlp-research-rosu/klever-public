#!/usr/bin/env python3
"""Independent launcher/candidate provenance checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GEN = Path("/generation-evidence")
TRACE = GEN / "codex-trace/2026/07/22/rollout-2026-07-22T22-37-25-019f8d0c-aa5a-7c71-bb49-106b51fa9dd0.jsonl"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe_tree(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries[relative] = ("symlink", os.readlink(path))
        elif stat.S_ISDIR(mode):
            entries[relative] = ("dir", None)
        elif stat.S_ISREG(mode):
            entries[relative] = ("file", sha256(path))
        else:
            entries[relative] = ("other", oct(mode))
    return entries


def manifest_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    """Reviewer-defined deterministic digest; individual entries remain visible."""
    serialized = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(serialized).hexdigest()


def main() -> None:
    data = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    print(f"record_layout={data['record_layout']}")
    print(f"semantics_mode={data['semantics_mode']}")
    print(f"campaign_block_exact_match={lock == data['audit_campaign']}")
    lock_hash = sha256(LOCK)
    print(f"lock_sha256={lock_hash}")
    print(
        "lock_hash_matches_recorded="
        f"{lock_hash == data['hashes']['audit_campaign_lock_sha256']}"
    )

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GEN / "invocation.json",
        GEN / "metrics.json",
        GEN / "codex-last.txt",
        GEN / "codex-output.log",
        GEN / "prompt.txt",
        TRACE,
    ]
    if (GEN / "usage.json").exists():
        required.append(GEN / "usage.json")
    for path in required:
        mode = path.lstat().st_mode if path.exists() else 0
        kind = (
            "symlink"
            if path.is_symlink()
            else "file"
            if stat.S_ISREG(mode)
            else "missing-or-not-file"
        )
        readable = os.access(path, os.R_OK)
        digest = sha256(path) if kind == "file" and readable else "-"
        print(f"required {path}: kind={kind} readable={readable} sha256={digest}")

    recorded_file_hashes = {
        LOCK: "audit_campaign_lock_sha256",
        REFERENCE / "canonical.py": "canonical_sha256",
        REFERENCE / "prompt.py": "trusted_prompt_sha256",
        REFERENCE / "py2mpy.py": "trusted_translator_sha256",
        CANDIDATE / "prompt.py": "candidate_prompt_sha256",
        CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        GEN / "invocation.json": "stage1_invocation_sha256",
        GEN / "metrics.json": "generation_metrics_sha256",
        GEN / "usage.json": "generation_usage_sha256",
        GEN / "codex-last.txt": "generation_codex_last_sha256",
        GEN / "codex-output.log": "generation_codex_output_sha256",
        GEN / "prompt.txt": "generation_prompt_sha256",
    }
    for path, key in recorded_file_hashes.items():
        actual = sha256(path)
        expected = data["hashes"][key]
        print(
            f"recorded-hash {path}: actual={actual} expected={expected} "
            f"match={actual == expected}"
        )

    invocation = json.loads((GEN / "invocation.json").read_text())
    evidence_hashes = invocation["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        path = GEN / relative
        actual = sha256(path)
        print(
            f"invocation-hash {relative}: actual={actual} expected={expected} "
            f"match={actual == expected}"
        )

    pairs = [
        (CANDIDATE / "prompt.py", REFERENCE / "prompt.py"),
        (CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py"),
    ]
    for left, right in pairs:
        print(
            f"byte-compare {left} {right}: "
            f"equal={left.read_bytes() == right.read_bytes()}"
        )

    candidate_semantics = describe_tree(CANDIDATE / "reference-semantics")
    trusted_semantics = describe_tree(REFERENCE / "reference-semantics")
    print(
        "candidate-semantics reviewer-manifest-sha256="
        f"{manifest_digest(candidate_semantics)}"
    )
    print(
        "trusted-semantics reviewer-manifest-sha256="
        f"{manifest_digest(trusted_semantics)}"
    )
    print(f"semantics_trees_exact={candidate_semantics == trusted_semantics}")
    candidate_names = set(candidate_semantics)
    trusted_names = set(trusted_semantics)
    print(f"semantics_missing={sorted(trusted_names - candidate_names)}")
    print(f"semantics_additional={sorted(candidate_names - trusted_names)}")
    for name in sorted(candidate_names & trusted_names):
        if candidate_semantics[name] != trusted_semantics[name]:
            print(
                f"semantics_difference {name}: "
                f"candidate={candidate_semantics[name]} "
                f"trusted={trusted_semantics[name]}"
            )
    for name, description in candidate_semantics.items():
        if description[0] == "symlink":
            print(f"candidate-semantics-symlink {name} -> {description[1]}")
    all_candidate = describe_tree(CANDIDATE)
    symlinks = {
        name: value for name, value in all_candidate.items() if value[0] == "symlink"
    }
    print(f"candidate_symlinks={symlinks}")
    print(
        "candidate reviewer-manifest-sha256="
        f"{manifest_digest(all_candidate)} entries={len(all_candidate)}"
    )

    outer = Counter()
    payload = Counter()
    invalid_lines: list[int] = []
    with TRACE.open() as stream:
        for number, line in enumerate(stream, 1):
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                invalid_lines.append(number)
                continue
            outer[item.get("type")] += 1
            body = item.get("payload", {})
            payload[(item.get("type"), body.get("type"), body.get("role"))] += 1
    print(f"trace_lines={sum(outer.values())} invalid_json_lines={invalid_lines}")
    print(f"trace_outer_types={dict(sorted(outer.items()))}")
    print(
        "trace_payload_types="
        + json.dumps(
            {"|".join("" if part is None else part for part in key): count
             for key, count in sorted(payload.items(), key=lambda pair: str(pair[0]))},
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
