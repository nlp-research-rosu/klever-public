#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

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
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def report_hash(label: str, path: Path, expected: str | None) -> bool:
    actual = sha256(path)
    ok = expected is None or actual == expected
    print(f"HASH {label}: {'PASS' if ok else 'FAIL'}")
    print(f"  path={path}")
    print(f"  actual={actual}")
    if expected is not None:
        print(f"  expected={expected}")
    return ok


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs.sort()
        files.sort()
        for name in dirs + files:
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            mode = os.lstat(path).st_mode
            if stat.S_ISLNK(mode):
                result[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                result[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[rel] = ("file", sha256(path))
            else:
                result[rel] = (f"other:{stat.S_IFMT(mode):o}", None)
    return result


def main() -> int:
    data = json.loads(AUDIT_INPUT.read_text())
    hashes = data["hashes"]
    paths = data["container_paths"]
    failures: list[str] = []

    print("DECLARED")
    print(f"  record_layout={data['record_layout']}")
    print(f"  semantics_mode={data['semantics_mode']}")
    print(f"  problem_id={data['problem_id']}")

    lock_path = Path(paths["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())
    if lock == data["audit_campaign"]:
        print("LOCK block equality: PASS")
    else:
        print("LOCK block equality: FAIL")
        failures.append("audit campaign lock content differs from audit_campaign")
    if not report_hash(
        "audit_campaign_lock", lock_path, hashes["audit_campaign_lock_sha256"]
    ):
        failures.append("audit campaign lock hash")

    fixed_checks = [
        ("canonical", Path(paths["canonical"]), hashes["canonical_sha256"]),
        (
            "trusted_prompt",
            Path(paths["trusted_prompt"]),
            hashes["trusted_prompt_sha256"],
        ),
        (
            "candidate_prompt",
            Path(paths["candidate"]) / "prompt.py",
            hashes["candidate_prompt_sha256"],
        ),
        (
            "trusted_translator",
            Path(paths["translator"]),
            hashes["trusted_translator_sha256"],
        ),
        (
            "candidate_translator",
            Path(paths["candidate"]) / "py2mpy.py",
            hashes["candidate_translator_sha256"],
        ),
        (
            "run_manifest",
            Path(paths["run_manifest"]),
            hashes["run_manifest_sha256"],
        ),
        (
            "task_manifest",
            Path(paths["task_manifest"]),
            hashes["task_manifest_sha256"],
        ),
        (
            "stage1_result",
            Path(paths["stage1_result"]),
            hashes["stage1_result_sha256"],
        ),
        (
            "stage1_invocation",
            Path(paths["generation_manifest"]),
            hashes["stage1_invocation_sha256"],
        ),
        (
            "generation_metrics",
            Path(paths["generation_metrics"]),
            hashes["generation_metrics_sha256"],
        ),
        (
            "generation_last",
            Path(paths["generation_last"]),
            hashes["generation_codex_last_sha256"],
        ),
        (
            "generation_output",
            Path(paths["generation_output"]),
            hashes["generation_codex_output_sha256"],
        ),
        (
            "generation_prompt",
            Path(paths["generation_root"]) / "prompt.txt",
            hashes["generation_prompt_sha256"],
        ),
        (
            "generation_runtime_metrics",
            Path(paths["generation_root"]) / "runtime-metrics.json",
            hashes["generation_runtime_metrics_sha256"],
        ),
        (
            "generation_usage",
            Path(paths["generation_root"]) / "usage.json",
            hashes["generation_usage_sha256"],
        ),
    ]
    for label, path, expected in fixed_checks:
        if not path.exists() or not path.is_file() or path.is_symlink():
            print(f"TYPE {label}: FAIL path={path}")
            failures.append(f"{label} absent, non-file, or symlink")
        elif not report_hash(label, path, expected):
            failures.append(f"{label} hash")

    required_records = [
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
    for path in required_records:
        ok = path.exists() and path.is_file() and not path.is_symlink()
        print(f"REQUIRED {path}: {'PASS' if ok else 'FAIL'}")
        if not ok:
            failures.append(f"required record {path}")

    trace_root = Path(paths["generation_trace"])
    trace_entries = tree_entries(trace_root)
    trace_files = {k: v for k, v in trace_entries.items() if v[0] == "file"}
    trace_bad = {k: v for k, v in trace_entries.items() if v[0] not in ("directory", "file")}
    print(f"TRACE files={len(trace_files)} special_entries={len(trace_bad)}")
    if trace_bad:
        failures.append("generation trace contains symlink/special entry")
    generation_result = json.loads(Path("/generation-result.json").read_text())
    declared_outputs = generation_result["outputs"]["evidence"]
    for rel, (_, actual) in trace_files.items():
        key = f"codex-trace/{rel}"
        expected = declared_outputs.get(key)
        ok = actual == expected
        print(f"TRACE_HASH {rel}: {'PASS' if ok else 'FAIL'}")
        print(f"  actual={actual}")
        print(f"  expected={expected}")
        if not ok:
            failures.append(f"trace hash {rel}")
    declared_trace = {
        key.removeprefix("codex-trace/"): value
        for key, value in declared_outputs.items()
        if key.startswith("codex-trace/")
    }
    if set(declared_trace) != set(trace_files):
        print("TRACE file-set equality: FAIL")
        failures.append("trace file set mismatch")
    else:
        print("TRACE file-set equality: PASS")

    trusted_root = Path("/reference/reference-semantics")
    candidate_root = Path("/candidate/reference-semantics")
    trusted = tree_entries(trusted_root)
    candidate = tree_entries(candidate_root)
    print(f"SEMANTICS trusted_entries={len(trusted)} candidate_entries={len(candidate)}")
    missing = sorted(set(trusted) - set(candidate))
    additional = sorted(set(candidate) - set(trusted))
    changed = sorted(
        rel for rel in set(trusted) & set(candidate) if trusted[rel] != candidate[rel]
    )
    print(f"SEMANTICS missing={missing}")
    print(f"SEMANTICS additional={additional}")
    print(f"SEMANTICS changed_or_mistyped={changed}")
    if missing or additional or changed:
        failures.append("supplied semantics tree integrity")
    else:
        print("SEMANTICS recursive type/content equality: PASS")

    prompt_equal = (
        Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    )
    translator_equal = (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    print(f"PROMPT byte equality: {'PASS' if prompt_equal else 'FAIL'}")
    print(f"TRANSLATOR byte equality: {'PASS' if translator_equal else 'FAIL'}")
    if not prompt_equal:
        failures.append("candidate prompt differs")
    if not translator_equal:
        failures.append("candidate translator differs")

    required_candidate = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    for name in required_candidate:
        path = Path("/candidate") / name
        ok = path.exists() and path.is_file() and not path.is_symlink()
        print(f"CANDIDATE_REQUIRED {name}: {'PASS' if ok else 'FAIL'}")
        if ok:
            print(f"  sha256={sha256(path)}")
        else:
            failures.append(f"candidate required artifact {name}")

    candidate_all = tree_entries(Path("/candidate"))
    candidate_special = {
        rel: value
        for rel, value in candidate_all.items()
        if value[0] not in ("directory", "file")
    }
    independent_tree = hashlib.sha256()
    for rel, (kind, value) in sorted(candidate_all.items()):
        independent_tree.update(kind.encode())
        independent_tree.update(b"\0")
        independent_tree.update(rel.encode())
        independent_tree.update(b"\0")
        independent_tree.update((value or "").encode())
        independent_tree.update(b"\0")
    print(
        "CANDIDATE independent_inventory "
        f"entries={len(candidate_all)} special_entries={len(candidate_special)}"
    )
    print(f"CANDIDATE independent_tree_sha256={independent_tree.hexdigest()}")
    if candidate_special:
        print(f"CANDIDATE special_entries={candidate_special}")
        failures.append("candidate contains symlink/special entry")

    print(f"FINAL failures={len(failures)}")
    for failure in failures:
        print(f"  FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
