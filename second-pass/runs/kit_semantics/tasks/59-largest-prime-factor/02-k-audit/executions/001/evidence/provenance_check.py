#!/usr/bin/env python3
"""Independent checks of launcher-owned provenance mounts."""

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path):
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise AssertionError(f"required regular file has wrong type: {path}")


def tree_manifest(root: Path, output: Path) -> str:
    rows = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            kind = "symlink"
            value = os.readlink(path)
        elif stat.S_ISDIR(info.st_mode):
            kind = "directory"
            value = "-"
        elif stat.S_ISREG(info.st_mode):
            kind = "file"
            value = sha256(path)
        else:
            kind = "other"
            value = "-"
        rows.append(
            {
                "path": rel,
                "type": kind,
                "mode": stat.S_IMODE(info.st_mode),
                "sha256_or_target": value,
            }
        )
    encoded = (json.dumps(rows, indent=2, sort_keys=True) + "\n").encode()
    output.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def compare_trees(left: Path, right: Path):
    def entries(root: Path):
        result = {}
        for path in root.rglob("*"):
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode):
                result[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(info.st_mode):
                result[rel] = ("directory", None)
            elif stat.S_ISREG(info.st_mode):
                result[rel] = ("file", sha256(path))
            else:
                result[rel] = ("other", None)
        return result

    left_entries = entries(left)
    right_entries = entries(right)
    if left_entries != right_entries:
        only_left = sorted(set(left_entries) - set(right_entries))
        only_right = sorted(set(right_entries) - set(left_entries))
        changed = sorted(
            key
            for key in set(left_entries) & set(right_entries)
            if left_entries[key] != right_entries[key]
        )
        raise AssertionError(
            f"tree mismatch only_left={only_left} only_right={only_right} "
            f"changed={changed}"
        )


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["audit_campaign"] == lock
    assert sha256(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"audit_input_sha256 {sha256(AUDIT_INPUT)}")
    print(f"audit_campaign_lock_sha256 {sha256(LOCK)}")
    print("audit_campaign_content_match yes")

    expected_files = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/runtime-metrics.json"):
            "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"):
            "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"):
            "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    for path, hash_key in expected_files.items():
        require_regular(path)
        actual = sha256(path)
        expected = audit["hashes"][hash_key]
        assert actual == expected, (path, actual, expected)
        print(f"hash_ok {path} {actual}")

    required_trace = Path("/generation-evidence/codex-trace")
    assert required_trace.is_dir() and not required_trace.is_symlink()
    trace_files = sorted(required_trace.rglob("*"))
    assert trace_files
    assert all(not path.is_symlink() for path in trace_files)

    result = json.loads(Path("/generation-result.json").read_text())
    output_hashes = result["outputs"]["evidence"]
    evidence_root = Path("/generation-evidence")
    for rel, expected in sorted(output_hashes.items()):
        path = evidence_root / rel
        require_regular(path)
        actual = sha256(path)
        assert actual == expected, (path, actual, expected)
        print(f"stage1_output_hash_ok {rel} {actual}")

    candidate = Path("/candidate")
    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = candidate / "reference-semantics"
    assert trusted_semantics.is_dir() and not trusted_semantics.is_symlink()
    assert candidate_semantics.is_dir() and not candidate_semantics.is_symlink()
    compare_trees(candidate_semantics, trusted_semantics)
    assert (candidate / "prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert (candidate / "py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("candidate_prompt_byte_match yes")
    print("candidate_translator_byte_match yes")
    print("candidate_supplied_semantics_recursive_match yes")

    output_dir = Path("/audit-output/evidence")
    for root, name in (
        (candidate, "candidate-tree-manifest.json"),
        (trusted_semantics, "trusted-semantics-tree-manifest.json"),
        (required_trace, "generation-trace-tree-manifest.json"),
    ):
        manifest_hash = tree_manifest(root, output_dir / name)
        print(f"independent_tree_manifest_sha256 {root} {manifest_hash}")

    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    mounted_trace = next(required_trace.rglob("*.jsonl"))
    print(
        "usage_source_trace_sha256 "
        f"{usage['source_trace_sha256']} mounted_final_trace_sha256 "
        f"{sha256(mounted_trace)}"
    )
    print("provenance_integrity=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
