#!/usr/bin/env python3
"""Independent Stage 1 integrity checks for audit 9-rolling-max."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_hash(root: Path) -> str:
    """Reimplement the pipeline-v3 length-delimited tree digest."""
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise RuntimeError(f"tree root is not a real directory: {root}")
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
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


def real_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"unsupported:{stat.S_IFMT(mode):o}"


def compare_trees(left: Path, right: Path) -> list[str]:
    def manifest(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            kind = real_kind(path)
            digest = file_hash(path) if kind == "file" else None
            result[relative] = (kind, digest)
        return result

    lm = manifest(left)
    rm = manifest(right)
    differences: list[str] = []
    for relative in sorted(lm.keys() | rm.keys()):
        if relative not in lm:
            differences.append(f"missing-left {relative}")
        elif relative not in rm:
            differences.append(f"additional-left {relative}")
        elif lm[relative] != rm[relative]:
            differences.append(
                f"changed-or-mistyped {relative}: {lm[relative]} != {rm[relative]}"
            )
    return differences


def main() -> int:
    document = json.loads(AUDIT_INPUT.read_text())
    paths = {key: Path(value) for key, value in document["container_paths"].items()}
    expected = document["hashes"]

    print(f"record_layout={document['record_layout']}")
    print(f"semantics_mode={document['semantics_mode']}")

    lock = json.loads(paths["audit_campaign_lock"].read_text())
    print(f"campaign_block_equals_lock={document['audit_campaign'] == lock}")
    print(
        "audit_campaign_lock_sha256="
        f"{file_hash(paths['audit_campaign_lock'])} "
        f"expected={expected['audit_campaign_lock_sha256']}"
    )

    required = [
        AUDIT_INPUT,
        paths["audit_campaign_lock"],
        paths["candidate"],
        paths["canonical"],
        paths["translator"],
        paths["trusted_prompt"],
        paths["run_manifest"],
        paths["task_manifest"],
        paths["stage1_result"],
        paths["generation_manifest"],
        paths["generation_metrics"],
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        paths["generation_last"],
        paths["generation_output"],
        Path("/generation-evidence/prompt.txt"),
        paths["generation_trace"],
        Path("/reference/reference-semantics"),
    ]
    for path in required:
        print(
            f"required {path}: exists={path.exists()} readable={os.access(path, os.R_OK)} "
            f"kind={real_kind(path) if path.exists() or path.is_symlink() else 'missing'}"
        )

    file_expectations = {
        paths["audit_campaign_lock"]: expected["audit_campaign_lock_sha256"],
        paths["canonical"]: expected["canonical_sha256"],
        paths["trusted_prompt"]: expected["trusted_prompt_sha256"],
        paths["translator"]: expected["trusted_translator_sha256"],
        paths["run_manifest"]: expected["run_manifest_sha256"],
        paths["task_manifest"]: expected["task_manifest_sha256"],
        paths["stage1_result"]: expected["stage1_result_sha256"],
        paths["generation_manifest"]: expected["stage1_invocation_sha256"],
        paths["generation_metrics"]: expected["generation_metrics_sha256"],
        Path("/generation-evidence/runtime-metrics.json"): expected[
            "generation_runtime_metrics_sha256"
        ],
        Path("/generation-evidence/usage.json"): expected["generation_usage_sha256"],
        paths["generation_last"]: expected["generation_codex_last_sha256"],
        paths["generation_output"]: expected["generation_codex_output_sha256"],
        Path("/generation-evidence/prompt.txt"): expected["generation_prompt_sha256"],
    }
    bad_hashes = 0
    for path, wanted in file_expectations.items():
        actual = file_hash(path)
        matched = actual == wanted
        bad_hashes += not matched
        print(f"hash {path}: actual={actual} expected={wanted} match={matched}")

    invocation = json.loads(paths["generation_manifest"].read_text())
    result = json.loads(paths["stage1_result"].read_text())
    trace_files = sorted(paths["generation_trace"].rglob("*"))
    trace_files = [path for path in trace_files if real_kind(path) == "file"]
    expected_trace_outputs = {
        key: value
        for key, value in invocation["outputs"]["evidence"].items()
        if key.startswith("codex-trace/")
    }
    for relative, wanted in expected_trace_outputs.items():
        path = Path("/generation-evidence") / relative
        actual = file_hash(path)
        print(
            f"trace-file {relative}: actual={actual} expected={wanted} "
            f"match={actual == wanted}"
        )
    print(
        f"trace_file_set_matches_invocation="
        f"{set(expected_trace_outputs) == {str(p.relative_to('/generation-evidence')) for p in trace_files}}"
    )
    print(
        "trace_tree_sha256="
        f"{tree_hash(paths['generation_trace'])} "
        f"usage_source={json.loads(Path('/generation-evidence/usage.json').read_text())['source_trace_sha256']}"
    )

    trace = trace_files[0]
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    bad_json: list[int] = []
    line_count = 0
    with trace.open() as stream:
        for line_count, line in enumerate(stream, 1):
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                bad_json.append(line_count)
                continue
            top_types[entry.get("type", "<none>")] += 1
            payload = entry.get("payload")
            if isinstance(payload, dict):
                payload_types[payload.get("type", "<none>")] += 1
    print(
        f"structured_trace lines={line_count} bad_json={bad_json} "
        f"top_types={dict(top_types)} payload_types={dict(payload_types)}"
    )
    print(
        "invocation_and_result_evidence_equal="
        f"{invocation['outputs']['evidence'] == result['outputs']['evidence']}"
    )

    comparisons = [
        (
            Path("/candidate/prompt.py"),
            paths["trusted_prompt"],
            expected["candidate_prompt_sha256"],
        ),
        (
            Path("/candidate/py2mpy.py"),
            paths["translator"],
            expected["candidate_translator_sha256"],
        ),
    ]
    for candidate, trusted, recorded in comparisons:
        ch = file_hash(candidate)
        th = file_hash(trusted)
        print(
            f"candidate-input {candidate.name}: candidate={ch} trusted={th} "
            f"recorded={recorded} byte_identical={candidate.read_bytes() == trusted.read_bytes()}"
        )

    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_semantics = Path("/reference/reference-semantics")
    semantics_differences = compare_trees(candidate_semantics, trusted_semantics)
    candidate_semantics_hash = tree_hash(candidate_semantics)
    trusted_semantics_hash = tree_hash(trusted_semantics)
    print(f"semantics_differences={semantics_differences}")
    print(
        f"semantics_tree candidate={candidate_semantics_hash} "
        f"trusted={trusted_semantics_hash} "
        f"manifest_expected={expected['trusted_reference_semantics_manifest_sha256']}"
    )

    candidate_tree_hash = tree_hash(paths["candidate"])
    print(
        f"candidate_tree_sha256={candidate_tree_hash} "
        f"stage1_workspace_sha256={result['outputs']['workspace_sha256']}"
    )
    print(
        "launcher_secondary_candidate_hash="
        f"{expected['candidate_tree_sha256']} "
        "(different launcher digest scheme; recorded, not substituted for byte/tree checks)"
    )
    print(
        "launcher_secondary_semantics_hash="
        f"{expected['trusted_reference_semantics_sha256']} "
        "(different launcher digest scheme; recorded, not substituted for exact tree comparison)"
    )

    proof_artifacts = [
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
        Path("/candidate/PROOF.md"),
    ]
    proof_artifact_ok = True
    for path in proof_artifacts:
        kind = real_kind(path) if path.exists() or path.is_symlink() else "missing"
        ok = kind == "file" and os.access(path, os.R_OK)
        proof_artifact_ok &= ok
        print(f"proof-artifact {path}: kind={kind} readable={os.access(path, os.R_OK)}")

    ok = (
        document["record_layout"] == "pipeline-v3"
        and document["semantics_mode"] == "SUPPLIED_SEMANTICS"
        and document["audit_campaign"] == lock
        and not bad_hashes
        and not semantics_differences
        and candidate_semantics_hash == trusted_semantics_hash
        and not bad_json
        and proof_artifact_ok
    )
    print(f"STAGE1_OK={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
