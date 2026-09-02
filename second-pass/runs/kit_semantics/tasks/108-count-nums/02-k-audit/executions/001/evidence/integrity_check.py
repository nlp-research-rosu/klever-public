#!/usr/bin/env python3
"""Independent integrity checks for audit 108-count-nums."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise RuntimeError(f"not a regular file: {path} mode={oct(info.st_mode)}")


def check_hash(label: str, path: Path, expected: str) -> bool:
    require_regular(path)
    actual = sha256_file(path)
    ok = actual == expected
    print(f"{label}: {'OK' if ok else 'MISMATCH'} {path}")
    print(f"  expected={expected}")
    print(f"  actual  ={actual}")
    return ok


def walk_tree(root: Path) -> dict[str, tuple[str, str | None]]:
    """Return path -> (kind, file hash or link target), without following links."""
    result: dict[str, tuple[str, str | None]] = {}
    root_info = root.lstat()
    if not stat.S_ISDIR(root_info.st_mode):
        raise RuntimeError(f"tree root is not a directory: {root}")
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode):
                result[rel] = ("symlink", os.readlink(path))
                if name in dirs:
                    dirs.remove(name)
            elif stat.S_ISDIR(info.st_mode):
                result[rel] = ("dir", None)
            elif stat.S_ISREG(info.st_mode):
                result[rel] = ("file", sha256_file(path))
            else:
                result[rel] = (f"special:{stat.S_IFMT(info.st_mode)}", None)
    return result


def compare_trees(left: Path, right: Path) -> bool:
    left_tree = walk_tree(left)
    right_tree = walk_tree(right)
    ok = True
    for rel in sorted(set(left_tree) | set(right_tree)):
        l_item = left_tree.get(rel)
        r_item = right_tree.get(rel)
        if l_item != r_item:
            ok = False
            print(f"TREE MISMATCH {rel}: candidate={l_item!r} trusted={r_item!r}")
    symlinks = [rel for rel, (kind, _) in left_tree.items() if kind == "symlink"]
    if symlinks:
        ok = False
        print("CANDIDATE SYMLINKS:", ", ".join(symlinks))
    print(
        f"reference-semantics recursive comparison: {'OK' if ok else 'MISMATCH'} "
        f"candidate_entries={len(left_tree)} trusted_entries={len(right_tree)}"
    )
    return ok


def manifest_digest(tree: dict[str, tuple[str, str | None]]) -> str:
    encoded = json.dumps(
        tree,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    data = json.loads(AUDIT_INPUT.read_text())
    hashes = data["hashes"]
    paths = data["container_paths"]
    ok = True

    expected_mode = "SUPPLIED_SEMANTICS"
    actual_mode = data.get("semantics_mode")
    print(f"semantics_mode={actual_mode}")
    ok &= actual_mode == expected_mode
    trusted_semantics = Path("/reference/reference-semantics")
    print(f"trusted_reference_semantics_present={trusted_semantics.is_dir()}")
    ok &= trusted_semantics.is_dir()

    required = {
        "audit_campaign_lock_sha256": Path(paths["audit_campaign_lock"]),
        "canonical_sha256": Path(paths["canonical"]),
        "candidate_prompt_sha256": Path(paths["candidate"]) / "prompt.py",
        "candidate_translator_sha256": Path(paths["candidate"]) / "py2mpy.py",
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
    for label, path in required.items():
        try:
            ok &= check_hash(label, path, hashes[label])
        except Exception as err:
            ok = False
            print(f"{label}: ERROR {path}: {err}")

    lock = json.loads(Path(paths["audit_campaign_lock"]).read_text())
    campaign = data["audit_campaign"]
    lock_ok = lock == campaign
    print(f"campaign_lock_matches_audit_input={lock_ok}")
    if not lock_ok:
        print(f"lock={json.dumps(lock, sort_keys=True)}")
        print(f"audit_campaign={json.dumps(campaign, sort_keys=True)}")
    ok &= lock_ok

    for candidate_rel, trusted in (
        ("prompt.py", Path(paths["trusted_prompt"])),
        ("py2mpy.py", Path(paths["translator"])),
    ):
        candidate = Path(paths["candidate"]) / candidate_rel
        equal = candidate.read_bytes() == trusted.read_bytes()
        print(f"byte_identity {candidate} {trusted}: {equal}")
        ok &= equal

    try:
        candidate_semantics_tree = walk_tree(
            Path(paths["candidate"]) / "reference-semantics"
        )
        trusted_semantics_tree = walk_tree(trusted_semantics)
        ok &= compare_trees(
            Path(paths["candidate"]) / "reference-semantics", trusted_semantics
        )
        print(
            "independent_candidate_semantics_manifest_sha256="
            + manifest_digest(candidate_semantics_tree)
        )
        print(
            "independent_trusted_semantics_manifest_sha256="
            + manifest_digest(trusted_semantics_tree)
        )
    except Exception as err:
        ok = False
        print(f"reference-semantics comparison ERROR: {err}")

    layout_required = [
        Path("/audit-input.json"),
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    for path in layout_required:
        try:
            require_regular(path)
            print(f"pipeline-v3 required regular file: OK {path}")
        except Exception as err:
            ok = False
            print(f"pipeline-v3 required regular file: ERROR {path}: {err}")

    stage1_result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    result_evidence = stage1_result["outputs"]["evidence"]
    invocation_evidence = invocation["outputs"]["evidence"]
    evidence_root = Path("/generation-evidence")
    for rel, expected in sorted(result_evidence.items()):
        path = evidence_root / rel
        try:
            current = sha256_file(path)
            item_ok = current == expected == invocation_evidence.get(rel)
            print(
                f"stage1 evidence output: {'OK' if item_ok else 'MISMATCH'} {rel} "
                f"expected={expected} actual={current} "
                f"invocation={invocation_evidence.get(rel)}"
            )
            ok &= item_ok
        except Exception as err:
            ok = False
            print(f"stage1 evidence output: ERROR {rel}: {err}")

    trace_root = Path(paths["generation_trace"])
    try:
        trace_tree = walk_tree(trace_root)
        trace_bad = [
            rel for rel, (kind, _) in trace_tree.items() if kind not in {"dir", "file"}
        ]
        trace_files = [
            rel for rel, (kind, _) in trace_tree.items() if kind == "file"
        ]
        trace_ok = not trace_bad and bool(trace_files)
        print(
            f"structured trace tree: {'OK' if trace_ok else 'ERROR'} "
            f"files={trace_files} bad_entries={trace_bad}"
        )
        ok &= trace_ok
        print(
            "independent_structured_trace_manifest_sha256="
            + manifest_digest(trace_tree)
        )
    except Exception as err:
        ok = False
        print(f"structured trace tree: ERROR {err}")

    candidate_tree = walk_tree(Path(paths["candidate"]))
    candidate_links = [
        rel for rel, (kind, _) in candidate_tree.items() if kind == "symlink"
    ]
    print(
        f"candidate symlink scan: {'OK' if not candidate_links else 'ERROR'} "
        f"symlinks={candidate_links}"
    )
    ok &= not candidate_links
    print(
        f"independent_candidate_tree_manifest_sha256={manifest_digest(candidate_tree)}"
    )

    print(f"OVERALL_INTEGRITY={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
