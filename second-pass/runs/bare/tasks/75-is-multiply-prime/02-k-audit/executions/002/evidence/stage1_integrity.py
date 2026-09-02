#!/usr/bin/env python3
"""Independent launcher/provenance integrity checks for this audit."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reimplement tools.pipeline_contract.sha256_tree independently."""
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
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
                raise RuntimeError(f"linked or unsupported entry: {path}")
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise RuntimeError(f"not a real regular file: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise RuntimeError(f"not a real directory: {path}")


def result(label: str, ok: bool, detail: str = "") -> None:
    suffix = f" -- {detail}" if detail else ""
    print(f"{'PASS' if ok else 'FAIL'} {label}{suffix}")
    if not ok:
        global FAILURES
        FAILURES += 1


FAILURES = 0
audit = json.loads(AUDIT_INPUT.read_text())
lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
lock = json.loads(lock_path.read_text())

result("record layout", audit["record_layout"] == "legacy-selected-stage1")
result("semantics mode", audit["semantics_mode"] == "GENERATED_SEMANTICS")
result("campaign object equality", audit["audit_campaign"] == lock)
actual_lock_hash = sha256_file(lock_path)
result(
    "campaign byte hash",
    actual_lock_hash == audit["hashes"]["audit_campaign_lock_sha256"],
    actual_lock_hash,
)

directory_keys = {"candidate", "generation_root", "generation_trace"}
for key, raw_path in sorted(audit["container_paths"].items()):
    path = Path(raw_path)
    try:
        if key in directory_keys:
            require_directory(path)
        else:
            require_regular(path)
        result(f"container path {key}", True, str(path))
    except (OSError, RuntimeError) as error:
        result(f"container path {key}", False, str(error))

required_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required_records:
    try:
        require_regular(path)
        result(f"required record {path}", True)
    except (OSError, RuntimeError) as error:
        result(f"required record {path}", False, str(error))

usage = Path("/generation-evidence/usage.json")
result("optional usage.json present and regular", usage.exists() and not usage.is_symlink() and usage.is_file())
result(
    "legacy runtime-metrics absence allowed",
    not Path("/generation-evidence/runtime-metrics.json").exists(),
)

candidate_deliverables = [
    Path("/candidate/solution.py"),
    Path("/candidate/solution.mpy"),
    Path("/candidate/semantic.k"),
    Path("/candidate/solution-program.k"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
    Path("/candidate/definition.k"),
    Path("/candidate/prove.sh"),
]
for path in candidate_deliverables:
    try:
        require_regular(path)
        result(f"candidate proof artifact {path.name}", True)
    except (OSError, RuntimeError) as error:
        result(f"candidate proof artifact {path.name}", False, str(error))

file_hash_checks = {
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_usage_sha256": usage,
}
for key, path in file_hash_checks.items():
    actual = sha256_file(path)
    result(f"recorded hash {key}", actual == audit["hashes"][key], actual)

generation_result = json.loads(Path("/generation-result.json").read_text())
invocation_record = json.loads(Path("/generation-evidence/invocation.json").read_text())
result(
    "result/invocation evidence maps agree",
    generation_result["outputs"]["evidence"] == invocation_record["outputs"]["evidence"],
)
for relative, expected in sorted(generation_result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    try:
        require_regular(path)
        actual = sha256_file(path)
        result(f"generation result leaf {relative}", actual == expected, actual)
    except (OSError, RuntimeError) as error:
        result(f"generation result leaf {relative}", False, str(error))

result(
    "candidate prompt byte identity",
    Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes(),
)
result(
    "candidate translator byte identity",
    Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes(),
)
task_manifest = json.loads(Path("/task.json").read_text())
embedded_manifest = dict(audit["manifest"])
embedded_config = embedded_manifest.pop("config", None)
result(
    "task manifest equals embedded manifest fields",
    task_manifest == embedded_manifest,
)
result(
    "launcher-added embedded config cross-check",
    embedded_config == audit["config"] == audit["manifest_config"],
)
result(
    "GENERATED_SEMANTICS trusted baseline absent",
    not Path("/reference/reference-semantics").exists(),
)
result(
    "candidate reference-semantics absent",
    not Path("/candidate/reference-semantics").exists(),
)

candidate_hash = pipeline_tree_hash(Path("/candidate"))
trace_hash = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
usage_record = json.loads(usage.read_text())
result(
    "candidate pipeline tree hash matches retained workspace",
    candidate_hash == invocation["retained_workspace_sha256"],
    candidate_hash,
)
result(
    "trace pipeline tree hash matches usage source trace",
    trace_hash == usage_record["source_trace_sha256"],
    trace_hash,
)
print(f"INFO launcher candidate_tree_sha256={audit['hashes']['candidate_tree_sha256']}")
print(f"INFO launcher generation_codex_trace_sha256={audit['hashes']['generation_codex_trace_sha256']}")
print("INFO those launcher directory digests use an undeclared scheme; pipeline hashes above independently bind all entries")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
result("structured trace file count", len(trace_files) == 1, str(len(trace_files)))
event_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
trace_lines = 0
for trace_file in trace_files:
    require_regular(trace_file)
    with trace_file.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            trace_lines += 1
            event_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
result("all structured trace lines parse as JSON", trace_lines == 127, f"lines={trace_lines}")
print("INFO trace top-level types", dict(sorted(event_types.items())))
print("INFO trace payload types", dict(sorted(payload_types.items())))

print(f"SUMMARY failures={FAILURES}")
sys.exit(1 if FAILURES else 0)
