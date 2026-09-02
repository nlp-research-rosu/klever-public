#!/usr/bin/env python3
"""Independent provenance and mounted-input integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{stat.S_IFMT(mode):o}"


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        entry_kind = kind(path)
        digest = sha256_file(path) if entry_kind == "file" else None
        entries[relative] = (entry_kind, digest)
    return entries


def manifest_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    digest = hashlib.sha256()
    for relative, (entry_kind, content_hash) in sorted(entries.items()):
        line = f"{entry_kind}\t{relative}\t{content_hash or '-'}\n"
        digest.update(line.encode())
    return digest.hexdigest()


def check_file(
    label: str,
    path: Path,
    expected: str | None = None,
) -> bool:
    exists = path.exists()
    readable = os.access(path, os.R_OK)
    entry_kind = kind(path) if os.path.lexists(path) else "missing"
    actual = sha256_file(path) if entry_kind == "file" else None
    match = actual == expected if expected is not None else None
    print(
        f"FILE {label}: path={path} exists={exists} readable={readable} "
        f"kind={entry_kind} sha256={actual} expected={expected} match={match}"
    )
    return exists and readable and entry_kind == "file" and (
        expected is None or match is True
    )


def main() -> int:
    launcher = json.loads(AUDIT_INPUT.read_text())
    hashes = launcher["hashes"]
    required = {
        "audit-input": AUDIT_INPUT,
        "audit-campaign-lock": CAMPAIGN_LOCK,
        "run": Path("/run.json"),
        "task": Path("/task.json"),
        "generation-result": Path("/generation-result.json"),
        "generation-invocation": GENERATION / "invocation.json",
        "generation-metrics": GENERATION / "metrics.json",
        "generation-runtime-metrics": GENERATION / "runtime-metrics.json",
        "generation-usage": GENERATION / "usage.json",
        "generation-last": GENERATION / "codex-last.txt",
        "generation-output": GENERATION / "codex-output.log",
        "generation-prompt": GENERATION / "prompt.txt",
    }
    expected = {
        "audit-campaign-lock": hashes["audit_campaign_lock_sha256"],
        "run": hashes["run_manifest_sha256"],
        "task": hashes["task_manifest_sha256"],
        "generation-result": hashes["stage1_result_sha256"],
        "generation-invocation": hashes["stage1_invocation_sha256"],
        "generation-metrics": hashes["generation_metrics_sha256"],
        "generation-runtime-metrics": hashes["generation_runtime_metrics_sha256"],
        "generation-usage": hashes["generation_usage_sha256"],
        "generation-last": hashes["generation_codex_last_sha256"],
        "generation-output": hashes["generation_codex_output_sha256"],
        "generation-prompt": hashes["generation_prompt_sha256"],
    }
    ok = True
    for label, path in required.items():
        ok &= check_file(label, path, expected.get(label))

    lock = json.loads(CAMPAIGN_LOCK.read_text())
    campaign_equal = lock == launcher["audit_campaign"]
    print(f"CAMPAIGN_JSON_EQUAL={campaign_equal}")
    ok &= campaign_equal

    mounted_sources = {
        "canonical": (
            REFERENCE / "canonical.py",
            hashes["canonical_sha256"],
        ),
        "trusted-prompt": (
            REFERENCE / "prompt.py",
            hashes["trusted_prompt_sha256"],
        ),
        "candidate-prompt": (
            CANDIDATE / "prompt.py",
            hashes["candidate_prompt_sha256"],
        ),
        "trusted-translator": (
            REFERENCE / "py2mpy.py",
            hashes["trusted_translator_sha256"],
        ),
        "candidate-translator": (
            CANDIDATE / "py2mpy.py",
            hashes["candidate_translator_sha256"],
        ),
    }
    for label, (path, digest) in mounted_sources.items():
        ok &= check_file(label, path, digest)

    prompt_equal = (CANDIDATE / "prompt.py").read_bytes() == (
        REFERENCE / "prompt.py"
    ).read_bytes()
    translator_equal = (CANDIDATE / "py2mpy.py").read_bytes() == (
        REFERENCE / "py2mpy.py"
    ).read_bytes()
    print(f"PROMPT_BYTE_EQUAL={prompt_equal}")
    print(f"TRANSLATOR_BYTE_EQUAL={translator_equal}")
    ok &= prompt_equal and translator_equal

    candidate_semantics = inventory(CANDIDATE / "reference-semantics")
    trusted_semantics = inventory(REFERENCE / "reference-semantics")
    missing = sorted(set(trusted_semantics) - set(candidate_semantics))
    additional = sorted(set(candidate_semantics) - set(trusted_semantics))
    changed = sorted(
        path
        for path in set(candidate_semantics) & set(trusted_semantics)
        if candidate_semantics[path] != trusted_semantics[path]
    )
    symlinked = sorted(
        path
        for path, (entry_kind, _) in candidate_semantics.items()
        if entry_kind == "symlink"
    )
    print(
        "SEMANTICS_COUNTS "
        f"candidate={len(candidate_semantics)} trusted={len(trusted_semantics)}"
    )
    print(f"SEMANTICS_MISSING={missing}")
    print(f"SEMANTICS_ADDITIONAL={additional}")
    print(f"SEMANTICS_CHANGED_OR_MISTYPED={changed}")
    print(f"SEMANTICS_SYMLINKED={symlinked}")
    print(
        "SEMANTICS_MANIFEST_SHA256 "
        f"candidate={manifest_digest(candidate_semantics)} "
        f"trusted={manifest_digest(trusted_semantics)}"
    )
    ok &= not (missing or additional or changed or symlinked)

    candidate_inventory = inventory(CANDIDATE)
    candidate_symlinks = sorted(
        path
        for path, (entry_kind, _) in candidate_inventory.items()
        if entry_kind == "symlink"
    )
    print(f"CANDIDATE_ENTRY_COUNT={len(candidate_inventory)}")
    print(f"CANDIDATE_SYMLINKS={candidate_symlinks}")
    print(
        f"CANDIDATE_INDEPENDENT_MANIFEST_SHA256="
        f"{manifest_digest(candidate_inventory)}"
    )

    result = json.loads(Path("/generation-result.json").read_text())
    trace_expected = result["outputs"]["evidence"]
    trace_files = sorted(
        path for path in (GENERATION / "codex-trace").rglob("*") if path.is_file()
    )
    print(f"TRACE_FILE_COUNT={len(trace_files)}")
    trace_valid = True
    for path in trace_files:
        relative = path.relative_to(GENERATION).as_posix()
        actual = sha256_file(path)
        expected_hash = trace_expected.get(relative)
        match = actual == expected_hash
        print(
            f"TRACE_FILE path={relative} sha256={actual} "
            f"expected={expected_hash} match={match}"
        )
        trace_valid &= match
    declared_trace = sorted(
        key for key in trace_expected if key.startswith("codex-trace/")
    )
    actual_trace = [
        path.relative_to(GENERATION).as_posix() for path in trace_files
    ]
    print(
        f"TRACE_DECLARED_SET_EQUAL={declared_trace == actual_trace} "
        f"declared={declared_trace} actual={actual_trace}"
    )
    trace_valid &= declared_trace == actual_trace
    ok &= trace_valid

    for path in trace_files:
        line_count = 0
        invalid_lines: list[int] = []
        record_types: Counter[str] = Counter()
        top_keys: Counter[str] = Counter()
        with path.open() as stream:
            for line_count, line in enumerate(stream, 1):
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    invalid_lines.append(line_count)
                    continue
                for key in record:
                    top_keys[key] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    record_types[str(payload.get("type", "<none>"))] += 1
                else:
                    record_types["<no-payload>"] += 1
        print(
            f"TRACE_PARSE path={path} lines={line_count} "
            f"invalid={invalid_lines} payload_types={dict(record_types)} "
            f"top_keys={dict(top_keys)}"
        )
        ok &= not invalid_lines

    print(f"OVERALL_INTEGRITY_OK={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
