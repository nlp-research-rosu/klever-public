#!/usr/bin/env python3
"""Independent launcher/provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def report_file(label: str, path: Path, expected: str | None = None) -> bool:
    if not path.exists():
        print(f"FAIL {label}: missing {path}")
        return False
    if path.is_symlink():
        print(f"FAIL {label}: symlink {path} -> {os.readlink(path)}")
        return False
    if not path.is_file():
        print(f"FAIL {label}: not a regular file: {path}")
        return False
    actual = sha256(path)
    verdict = "PASS" if expected is None or actual == expected else "FAIL"
    suffix = "" if expected is None else f" expected={expected}"
    print(f"{verdict} {label}: sha256={actual}{suffix}")
    return verdict == "PASS"


def regular_tree(root: Path) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            result[relative] = ("symlink", os.readlink(path))
        elif path.is_dir():
            result[relative] = ("directory", "")
        elif path.is_file():
            result[relative] = ("file", sha256(path))
        else:
            result[relative] = ("other", "")
    return result


def main() -> int:
    ok = True
    if not report_file("launcher audit input", AUDIT_INPUT):
        return 2

    data = json.loads(AUDIT_INPUT.read_text())
    print(f"record_layout={data.get('record_layout')}")
    print(f"semantics_mode={data.get('semantics_mode')}")
    if data.get("record_layout") != "pipeline-v3":
        print("FAIL declared record layout is not pipeline-v3")
        ok = False
    if data.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        print("FAIL declared semantics mode is not SUPPLIED_SEMANTICS")
        ok = False

    paths = data["container_paths"]
    required_path_keys = {
        "audit_campaign_lock",
        "candidate",
        "canonical",
        "generation_last",
        "generation_manifest",
        "generation_metrics",
        "generation_output",
        "generation_root",
        "generation_trace",
        "run_manifest",
        "stage1_result",
        "task_manifest",
        "translator",
        "trusted_prompt",
    }
    missing_keys = sorted(required_path_keys - paths.keys())
    print(f"{'PASS' if not missing_keys else 'FAIL'} container_paths required keys: missing={missing_keys}")
    ok &= not missing_keys

    lock_path = Path(paths["audit_campaign_lock"])
    if report_file(
        "campaign lock",
        lock_path,
        data["hashes"]["audit_campaign_lock_sha256"],
    ):
        lock = json.loads(lock_path.read_text())
        match = lock == data["audit_campaign"]
        print(f"{'PASS' if match else 'FAIL'} campaign lock JSON equals audit_campaign block")
        ok &= match
    else:
        ok = False

    fixed_hashes = {
        "run manifest": (Path(paths["run_manifest"]), "run_manifest_sha256"),
        "task manifest": (Path(paths["task_manifest"]), "task_manifest_sha256"),
        "stage1 result": (Path(paths["stage1_result"]), "stage1_result_sha256"),
        "generation invocation": (
            Path(paths["generation_manifest"]),
            "stage1_invocation_sha256",
        ),
        "generation metrics": (
            Path(paths["generation_metrics"]),
            "generation_metrics_sha256",
        ),
        "generation runtime metrics": (
            Path(paths["generation_root"]) / "runtime-metrics.json",
            "generation_runtime_metrics_sha256",
        ),
        "generation usage": (
            Path(paths["generation_root"]) / "usage.json",
            "generation_usage_sha256",
        ),
        "generation last": (
            Path(paths["generation_last"]),
            "generation_codex_last_sha256",
        ),
        "generation output": (
            Path(paths["generation_output"]),
            "generation_codex_output_sha256",
        ),
        "generation prompt": (
            Path(paths["generation_root"]) / "prompt.txt",
            "generation_prompt_sha256",
        ),
        "trusted canonical": (Path(paths["canonical"]), "canonical_sha256"),
        "trusted prompt": (Path(paths["trusted_prompt"]), "trusted_prompt_sha256"),
        "trusted translator": (Path(paths["translator"]), "trusted_translator_sha256"),
    }
    for label, (path, key) in fixed_hashes.items():
        ok &= report_file(label, path, data["hashes"][key])

    result = json.loads(Path(paths["stage1_result"]).read_text())
    invocation = json.loads(Path(paths["generation_manifest"]).read_text())
    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        path = Path(paths["generation_root"]) / relative
        entry_ok = report_file(f"stage1 evidence {relative}", path, expected)
        ok &= entry_ok
        invocation_expected = invocation["outputs"]["evidence"].get(relative)
        same = invocation_expected == expected
        print(
            f"{'PASS' if same else 'FAIL'} invocation/result hash agree for "
            f"{relative}: invocation={invocation_expected}"
        )
        ok &= same

    candidate = Path(paths["candidate"])
    proof_artifacts = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    for relative in proof_artifacts:
        artifact = candidate / relative
        artifact_ok = (
            artifact.exists() and artifact.is_file() and not artifact.is_symlink()
        )
        print(
            f"{'PASS' if artifact_ok else 'FAIL'} candidate proof artifact "
            f"{relative}: regular_non_symlink={artifact_ok}"
        )
        ok &= artifact_ok

    prompt_same = (candidate / "prompt.py").read_bytes() == Path(
        paths["trusted_prompt"]
    ).read_bytes()
    translator_same = (candidate / "py2mpy.py").read_bytes() == Path(
        paths["translator"]
    ).read_bytes()
    print(f"{'PASS' if prompt_same else 'FAIL'} candidate prompt byte identity")
    print(
        f"{'PASS' if translator_same else 'FAIL'} candidate translator byte identity"
    )
    ok &= prompt_same and translator_same

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = candidate / "reference-semantics"
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        print("INFRA_FAIL trusted reference semantics missing, mistyped, or symlinked")
        return 2
    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        print("FAIL candidate reference semantics missing, mistyped, or symlinked")
        ok = False
    else:
        trusted_tree = regular_tree(trusted_semantics)
        candidate_tree = regular_tree(candidate_semantics)
        tree_same = trusted_tree == candidate_tree
        print(
            f"{'PASS' if tree_same else 'FAIL'} supplied semantics recursive "
            f"type/path/hash identity: trusted_entries={len(trusted_tree)} "
            f"candidate_entries={len(candidate_tree)}"
        )
        if not tree_same:
            for relative in sorted(trusted_tree.keys() | candidate_tree.keys()):
                if trusted_tree.get(relative) != candidate_tree.get(relative):
                    print(
                        f"  DIFF {relative}: trusted={trusted_tree.get(relative)} "
                        f"candidate={candidate_tree.get(relative)}"
                    )
        ok &= tree_same

    for root in [
        candidate,
        Path(paths["generation_root"]),
        Path("/reference"),
    ]:
        symlinks = [str(path) for path in root.rglob("*") if path.is_symlink()]
        print(f"{'PASS' if not symlinks else 'FAIL'} no symlinks under {root}: {symlinks}")
        ok &= not symlinks

    print(f"OVERALL={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
