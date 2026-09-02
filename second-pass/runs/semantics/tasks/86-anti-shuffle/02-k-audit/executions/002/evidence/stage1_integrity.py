#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_file(path: Path, expected: str | None = None) -> bool:
    ok = True
    try:
        info = path.lstat()
    except OSError as err:
        print(f"ERROR missing/unreadable: {path}: {err}")
        return False
    if stat.S_ISLNK(info.st_mode):
        print(f"ERROR symlink where regular file required: {path}")
        return False
    if not stat.S_ISREG(info.st_mode):
        print(f"ERROR wrong type (not regular file): {path}")
        return False
    try:
        actual = digest(path)
    except OSError as err:
        print(f"ERROR unreadable: {path}: {err}")
        return False
    if expected is not None and actual != expected:
        ok = False
        print(f"ERROR hash mismatch: {path}: expected={expected} actual={actual}")
    else:
        suffix = f" expected={expected}" if expected else ""
        print(f"OK regular sha256={actual} path={path}{suffix}")
    return ok


def manifest(root: Path) -> tuple[dict[str, tuple[str, int | str]], bool]:
    entries: dict[str, tuple[str, int | str]] = {}
    ok = True
    if not root.is_dir() or root.is_symlink():
        print(f"ERROR required ordinary directory absent/mistyped: {root}")
        return entries, False
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            entries[rel] = ("symlink", os.readlink(path))
            print(f"ERROR symlink in tree: {path} -> {os.readlink(path)}")
            ok = False
        elif stat.S_ISREG(info.st_mode):
            entries[rel] = ("file", digest(path))
        elif stat.S_ISDIR(info.st_mode):
            entries[rel] = ("dir", stat.S_IMODE(info.st_mode))
        else:
            entries[rel] = ("other", stat.S_IFMT(info.st_mode))
            print(f"ERROR special/mistyped entry in tree: {path}")
            ok = False
    return entries, ok


def main() -> int:
    failures = 0
    with AUDIT.open("r", encoding="utf-8") as stream:
        record = json.load(stream)
    hashes = record["hashes"]

    print(f"record_layout={record['record_layout']}")
    print(f"semantics_mode={record['semantics_mode']}")
    if record["record_layout"] != "legacy-selected-stage1":
        print("ERROR unexpected record layout for this checker")
        failures += 1
    if record["semantics_mode"] != "SUPPLIED_SEMANTICS":
        print("ERROR rendered mode is not supplied semantics")
        failures += 1

    required_hashes = {
        LOCK: hashes["audit_campaign_lock_sha256"],
        Path("/run.json"): hashes["run_manifest_sha256"],
        Path("/task.json"): hashes["task_manifest_sha256"],
        Path("/generation-result.json"): hashes["stage1_result_sha256"],
        Path("/generation-evidence/invocation.json"): hashes["stage1_invocation_sha256"],
        Path("/generation-evidence/metrics.json"): hashes["generation_metrics_sha256"],
        Path("/generation-evidence/codex-last.txt"): hashes["generation_codex_last_sha256"],
        Path("/generation-evidence/codex-output.log"): hashes[
            "generation_codex_output_sha256"
        ],
        Path("/generation-evidence/prompt.txt"): hashes["generation_prompt_sha256"],
        Path("/reference/canonical.py"): hashes["canonical_sha256"],
        Path("/reference/prompt.py"): hashes["trusted_prompt_sha256"],
        Path("/reference/py2mpy.py"): hashes["trusted_translator_sha256"],
    }
    for path, expected in required_hashes.items():
        failures += not check_file(path, expected)

    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        failures += not check_file(usage, hashes.get("generation_usage_sha256"))
    else:
        print("INFO optional usage.json absent")

    with LOCK.open("r", encoding="utf-8") as stream:
        lock_obj = json.load(stream)
    if lock_obj != record["audit_campaign"]:
        print("ERROR campaign lock JSON does not equal audit_campaign block")
        failures += 1
    else:
        print("OK campaign lock JSON equals audit_campaign block")

    with Path("/task.json").open("r", encoding="utf-8") as stream:
        task_obj = json.load(stream)
    embedded_manifest = dict(record["manifest"])
    embedded_config = embedded_manifest.pop("config", None)
    if task_obj != embedded_manifest or embedded_config != record["config"]:
        print(
            "ERROR task manifest core or launcher-enriched config does not "
            "match audit-input"
        )
        failures += 1
    else:
        print(
            "OK task manifest equals embedded manifest core; "
            f"launcher-enriched config={embedded_config}"
        )

    # The candidate's fixed inputs must exactly match the independently mounted
    # trusted copies, regardless of launcher assertions.
    pairs = [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")),
    ]
    for candidate, trusted in pairs:
        candidate_ok = check_file(candidate)
        trusted_ok = check_file(trusted)
        if not candidate_ok or not trusted_ok or candidate.read_bytes() != trusted.read_bytes():
            print(f"ERROR byte mismatch: {candidate} != {trusted}")
            failures += 1
        else:
            print(f"OK byte-identical: {candidate} == {trusted}")

    candidate_root = Path("/candidate/reference-semantics")
    trusted_root = Path("/reference/reference-semantics")
    cand_entries, cand_ok = manifest(candidate_root)
    trust_entries, trust_ok = manifest(trusted_root)
    if not cand_ok or not trust_ok:
        failures += 1
    if cand_entries != trust_entries:
        failures += 1
        cand_only = sorted(set(cand_entries) - set(trust_entries))
        trust_only = sorted(set(trust_entries) - set(cand_entries))
        changed = sorted(
            key
            for key in set(cand_entries) & set(trust_entries)
            if cand_entries[key] != trust_entries[key]
        )
        print(f"ERROR semantics trees differ candidate_only={cand_only}")
        print(f"ERROR semantics trees differ trusted_only={trust_only}")
        print(f"ERROR semantics trees changed_or_mistyped={changed}")
    else:
        file_count = sum(kind == "file" for kind, _ in cand_entries.values())
        dir_count = sum(kind == "dir" for kind, _ in cand_entries.values())
        print(
            "OK supplied semantics recursively identical "
            f"files={file_count} dirs={dir_count} symlinks=0"
        )

    candidate_entries, candidate_ok = manifest(Path("/candidate"))
    if not candidate_ok:
        failures += 1
    required_proof_artifacts = (
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
    )
    for rel in required_proof_artifacts:
        entry = candidate_entries.get(rel)
        if entry is None or entry[0] != "file":
            print(f"ERROR required candidate proof artifact missing/mistyped: {rel}")
            failures += 1
        else:
            print(f"OK candidate proof artifact regular sha256={entry[1]} path={rel}")
    manifest_bytes = json.dumps(
        candidate_entries, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    independent_candidate_manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
    print(
        "OK independently hashed complete candidate tree "
        f"entries={len(candidate_entries)} "
        f"manifest_sha256={independent_candidate_manifest_hash}"
    )
    print(
        "INFO launcher-recorded candidate_tree_sha256="
        f"{hashes['candidate_tree_sha256']} "
        "(launcher tree-hash encoding is not assumed by this independent manifest)"
    )

    # Verify every evidence hash explicitly listed by the launcher-owned result.
    with Path("/generation-result.json").open("r", encoding="utf-8") as stream:
        generation_result = json.load(stream)
    evidence_root = Path("/generation-evidence")
    for rel, expected in generation_result["outputs"]["evidence"].items():
        failures += not check_file(evidence_root / rel, expected)

    trace_root = Path(record["container_paths"]["generation_trace"])
    trace_entries, trace_ok = manifest(trace_root)
    if not trace_ok or not trace_entries:
        print("ERROR structured trace tree absent, empty, or mistyped")
        failures += 1
    else:
        trace_files = [
            rel for rel, (kind, _) in trace_entries.items() if kind == "file"
        ]
        print(f"OK structured trace files={trace_files}")

    print(f"INTEGRITY_FAILURES={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
