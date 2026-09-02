#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT = Path("/audit-input.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def tree_files(root: Path) -> list[Path]:
    return sorted(
        (p for p in root.rglob("*") if p.is_file() and not p.is_symlink()),
        key=lambda p: p.relative_to(root).as_posix(),
    )


def tree_hash_variants(root: Path) -> dict[str, str]:
    """Report common deterministic tree-digest encodings for auditability."""
    paths = tree_files(root)
    variants: dict[str, hashlib._Hash] = {
        "relpath-nul-bytes": hashlib.sha256(),
        "relpath-newline-sha-newline": hashlib.sha256(),
        "sha-two-spaces-relpath-newline": hashlib.sha256(),
    }
    for path in paths:
        rel = path.relative_to(root).as_posix().encode()
        data = path.read_bytes()
        file_sha = hashlib.sha256(data).hexdigest().encode()
        variants["relpath-nul-bytes"].update(rel + b"\0" + data)
        variants["relpath-newline-sha-newline"].update(
            rel + b"\n" + file_sha + b"\n"
        )
        variants["sha-two-spaces-relpath-newline"].update(
            file_sha + b"  " + rel + b"\n"
        )
    return {name: state.hexdigest() for name, state in variants.items()}


def pipeline_tree_hash(root: Path) -> str:
    """Independently reimplement pipeline_contract.sha256_tree."""
    h = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise ValueError(f"symlink is not hashable: {path}")
        if path.is_dir():
            entries.append((rel, "directory", path))
        elif path.is_file():
            entries.append((rel, "file", path))
        else:
            raise ValueError(f"special entry is not hashable: {path}")
    for rel, kind, path in sorted(entries):
        encoded = rel.encode()
        h.update(len(encoded).to_bytes(4, "big"))
        h.update(encoded)
        h.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            h.update(len(data).to_bytes(8, "big"))
            h.update(data)
    return h.hexdigest()


def regular(path: Path) -> bool:
    return path.exists() and path.is_file() and not path.is_symlink()


def main() -> int:
    audit = load(AUDIT)
    hashes = audit["hashes"]
    cp = audit["container_paths"]

    required = [
        Path("/audit-input.json"),
        Path(cp["audit_campaign_lock"]),
        Path(cp["candidate"]),
        Path(cp["canonical"]),
        Path(cp["translator"]),
        Path(cp["trusted_prompt"]),
        Path(cp["run_manifest"]),
        Path(cp["task_manifest"]),
        Path(cp["stage1_result"]),
        Path(cp["generation_manifest"]),
        Path(cp["generation_metrics"]),
        Path(cp["generation_last"]),
        Path(cp["generation_output"]),
        Path(cp["generation_root"]) / "prompt.txt",
        Path(cp["generation_root"]) / "usage.json",
        Path(cp["generation_trace"]),
    ]
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    for path in required:
        ok = path.exists() and not path.is_symlink() and os.access(path, os.R_OK)
        print(f"required readable non-symlink {path}: {ok}")

    lock = load(Path(cp["audit_campaign_lock"]))
    print(f"campaign object equals lock: {audit['audit_campaign'] == lock}")

    checks = {
        "audit_campaign_lock_sha256": Path(cp["audit_campaign_lock"]),
        "canonical_sha256": Path(cp["canonical"]),
        "trusted_prompt_sha256": Path(cp["trusted_prompt"]),
        "trusted_translator_sha256": Path(cp["translator"]),
        "candidate_prompt_sha256": Path(cp["candidate"]) / "prompt.py",
        "candidate_translator_sha256": Path(cp["candidate"]) / "py2mpy.py",
        "run_manifest_sha256": Path(cp["run_manifest"]),
        "task_manifest_sha256": Path(cp["task_manifest"]),
        "stage1_result_sha256": Path(cp["stage1_result"]),
        "stage1_invocation_sha256": Path(cp["generation_manifest"]),
        "generation_metrics_sha256": Path(cp["generation_metrics"]),
        "generation_codex_last_sha256": Path(cp["generation_last"]),
        "generation_codex_output_sha256": Path(cp["generation_output"]),
        "generation_prompt_sha256": Path(cp["generation_root"]) / "prompt.txt",
        "generation_usage_sha256": Path(cp["generation_root"]) / "usage.json",
    }
    for key, path in checks.items():
        actual = digest(path) if regular(path) else "NOT_REGULAR"
        expected = hashes[key]
        print(f"{key}: expected={expected} actual={actual} match={actual == expected}")

    result = load(Path(cp["stage1_result"]))
    for rel, expected in sorted(result["outputs"]["evidence"].items()):
        path = Path(cp["generation_root"]) / rel
        actual = digest(path) if regular(path) else "NOT_REGULAR"
        print(
            "stage1 evidence "
            f"{rel}: expected={expected} actual={actual} match={actual == expected}"
        )

    candidate = Path(cp["candidate"])
    bad_entries = [
        str(path)
        for path in candidate.rglob("*")
        if path.is_symlink() or not (path.is_file() or path.is_dir())
    ]
    print(f"candidate symlink/special entries: {bad_entries}")
    print("candidate file manifest:")
    for path in tree_files(candidate):
        print(f"  {path.relative_to(candidate).as_posix()} {digest(path)}")
    print(f"recorded candidate_tree_sha256={hashes['candidate_tree_sha256']}")
    actual_tree = pipeline_tree_hash(candidate)
    print(
        "pipeline-encoding candidate tree: "
        f"actual={actual_tree} "
        f"matches_generation_workspace={actual_tree == result['outputs']['workspace_sha256']} "
        f"matches_audit_candidate_field={actual_tree == hashes['candidate_tree_sha256']}"
    )
    for name, value in tree_hash_variants(candidate).items():
        print(f"candidate tree variant {name}={value}")

    ref_sem = Path("/reference/reference-semantics")
    print(f"generated-mode reference-semantics absent: {not ref_sem.exists()}")
    print(
        "candidate prompt byte-equal trusted: "
        f"{(candidate / 'prompt.py').read_bytes() == Path(cp['trusted_prompt']).read_bytes()}"
    )
    print(
        "candidate translator byte-equal trusted: "
        f"{(candidate / 'py2mpy.py').read_bytes() == Path(cp['translator']).read_bytes()}"
    )
    embedded_task = dict(audit["manifest"])
    embedded_config = embedded_task.pop("config")
    print(f"embedded manifest config={embedded_config}")
    print(
        "task manifest equals embedded task fields: "
        f"{load(Path(cp['task_manifest'])) == embedded_task}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
