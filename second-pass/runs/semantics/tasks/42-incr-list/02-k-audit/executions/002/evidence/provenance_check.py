#!/usr/bin/env python3
"""Independent integrity checks for the mounted 42-incr-list audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GEN = Path("/generation-evidence")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def regular_file(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except FileNotFoundError:
        return False


def tree_entries(root: Path) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(dirpath)
        for name in sorted(dirnames + filenames):
            path = base / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                result[rel] = ("directory", "")
            elif stat.S_ISREG(mode):
                result[rel] = ("file", sha256(path))
            else:
                result[rel] = ("other", oct(mode))
    return result


def manifest_digest(entries: dict[str, tuple[str, str]]) -> str:
    digest = hashlib.sha256()
    for rel, (kind, value) in sorted(entries.items()):
        digest.update(kind.encode())
        digest.update(b"\0")
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update(value.encode())
        digest.update(b"\0")
    return digest.hexdigest()


def report_hash(label: str, path: Path, expected: str | None) -> bool:
    if not regular_file(path):
        print(f"FAIL {label}: absent or not a regular file: {path}")
        return False
    actual = sha256(path)
    status = "OK" if expected == actual else "FAIL"
    print(f"{status} {label}: {actual} expected={expected}")
    return expected == actual


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    hashes = audit["hashes"]
    ok = True

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")

    campaign_path = Path(audit["container_paths"]["audit_campaign_lock"])
    campaign = json.loads(campaign_path.read_text())
    same_campaign = campaign == audit["audit_campaign"]
    print(f"{'OK' if same_campaign else 'FAIL'} campaign JSON exact match")
    ok &= same_campaign
    ok &= report_hash(
        "campaign lock",
        campaign_path,
        hashes["audit_campaign_lock_sha256"],
    )

    required = {
        "run manifest": (Path("/run.json"), "run_manifest_sha256"),
        "task manifest": (Path("/task.json"), "task_manifest_sha256"),
        "generation result": (Path("/generation-result.json"), "stage1_result_sha256"),
        "invocation": (GEN / "invocation.json", "stage1_invocation_sha256"),
        "metrics": (GEN / "metrics.json", "generation_metrics_sha256"),
        "usage": (GEN / "usage.json", "generation_usage_sha256"),
        "generation final": (GEN / "codex-last.txt", "generation_codex_last_sha256"),
        "generation transcript": (
            GEN / "codex-output.log",
            "generation_codex_output_sha256",
        ),
        "generation prompt": (GEN / "prompt.txt", "generation_prompt_sha256"),
        "canonical": (REFERENCE / "canonical.py", "canonical_sha256"),
        "trusted prompt": (REFERENCE / "prompt.py", "trusted_prompt_sha256"),
        "trusted translator": (
            REFERENCE / "py2mpy.py",
            "trusted_translator_sha256",
        ),
    }
    for label, (path, hash_key) in required.items():
        ok &= report_hash(label, path, hashes[hash_key])

    runtime = GEN / "runtime-metrics.json"
    print(
        "OK legacy-selected-stage1 runtime-metrics is not required; "
        f"present={runtime.exists()}"
    )

    run = json.loads(Path("/run.json").read_text())
    task = json.loads(Path("/task.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads((GEN / "invocation.json").read_text())
    identities = [
        ("run_id", run.get("run_id"), audit["run_id"]),
        ("task problem", task.get("problem_id"), audit["problem_id"]),
        ("task condition", task.get("condition"), audit["manifest"]["condition"]),
        ("result stage", result.get("stage"), "01-k-proof"),
        ("invocation stage", invocation.get("stage"), "01-k-proof"),
        ("result invocation", result.get("invocation"), invocation.get("name")),
    ]
    for label, actual, expected in identities:
        same = actual == expected
        print(f"{'OK' if same else 'FAIL'} {label}: {actual!r} expected={expected!r}")
        ok &= same
    listed = audit["problem_id"] in run.get("tasks", [])
    print(f"{'OK' if listed else 'FAIL'} task listed in run")
    ok &= listed

    for evidence_rel, expected in sorted(result["outputs"]["evidence"].items()):
        evidence_path = GEN / evidence_rel
        ok &= report_hash(f"result evidence {evidence_rel}", evidence_path, expected)

    trace_files = sorted((GEN / "codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if regular_file(path)]
    print(f"trace regular files={len(trace_files)}")
    if not trace_files:
        print("FAIL structured trace has no regular files")
        ok = False
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    trace_lines = 0
    for path in trace_files:
        rel = path.relative_to(GEN / "codex-trace").as_posix()
        print(f"TRACE {rel} sha256={sha256(path)}")
        with path.open() as stream:
            for line_no, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as error:
                    print(f"FAIL invalid JSONL {rel}:{line_no}: {error}")
                    ok = False
                    continue
                top_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
    print(f"trace_lines={trace_lines}")
    print(f"trace_top_types={dict(sorted(top_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")

    candidate_types = tree_entries(CANDIDATE)
    bad_candidate_types = {
        rel: item
        for rel, item in candidate_types.items()
        if item[0] not in {"directory", "file"}
    }
    print(f"candidate_entries={len(candidate_types)}")
    print(f"candidate_manifest_sha256={manifest_digest(candidate_types)}")
    print(f"candidate_nonregular_entries={bad_candidate_types}")
    ok &= not bad_candidate_types

    cand_sem = tree_entries(CANDIDATE / "reference-semantics")
    ref_sem = tree_entries(REFERENCE / "reference-semantics")
    semantics_same = cand_sem == ref_sem
    print(f"{'OK' if semantics_same else 'FAIL'} supplied semantics exact recursive match")
    print(f"candidate_semantics_manifest_sha256={manifest_digest(cand_sem)}")
    print(f"trusted_semantics_manifest_sha256={manifest_digest(ref_sem)}")
    if not semantics_same:
        all_paths = sorted(set(cand_sem) | set(ref_sem))
        for rel in all_paths:
            if cand_sem.get(rel) != ref_sem.get(rel):
                print(
                    f"SEMANTICS_DIFF {rel}: "
                    f"candidate={cand_sem.get(rel)} trusted={ref_sem.get(rel)}"
                )
    ok &= semantics_same

    mode_ok = (
        audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
        and (REFERENCE / "reference-semantics").is_dir()
    )
    print(f"{'OK' if mode_ok else 'FAIL'} supplied-semantics mode/mount consistency")
    ok &= mode_ok

    pairs = [
        ("prompt", CANDIDATE / "prompt.py", REFERENCE / "prompt.py"),
        ("translator", CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py"),
    ]
    for label, left, right in pairs:
        same = regular_file(left) and regular_file(right) and left.read_bytes() == right.read_bytes()
        print(f"{'OK' if same else 'FAIL'} candidate {label} byte identity")
        ok &= same

    deliverables = ["solution.py", "solution.mpy", "verification.k", "spec.k", "prove.sh"]
    for name in deliverables:
        present = regular_file(CANDIDATE / name)
        print(f"{'OK' if present else 'FAIL'} required candidate artifact {name}")
        ok &= present

    print(f"OVERALL={'OK' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
