#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    root = root.resolve(strict=True)
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
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


def real_regular(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except OSError:
        return False


def real_directory(path: Path) -> bool:
    try:
        return stat.S_ISDIR(path.lstat().st_mode)
    except OSError:
        return False


audit_input_path = Path("/audit-input.json")
campaign_lock_path = Path("/audit-campaign-lock.json")
audit_input = json.loads(audit_input_path.read_text())
campaign_lock = json.loads(campaign_lock_path.read_text())
hashes = audit_input["hashes"]
paths = audit_input["container_paths"]

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(f"audit_input_real_regular={real_regular(audit_input_path)}")
print(f"campaign_lock_real_regular={real_regular(campaign_lock_path)}")
print(f"candidate_real_directory={real_directory(Path(paths['candidate']))}")
print(f"generation_root_real_directory={real_directory(Path(paths['generation_root']))}")
print(f"generation_trace_real_directory={real_directory(Path(paths['generation_trace']))}")
print(f"campaign_object_exact_match={campaign_lock == audit_input['audit_campaign']}")

file_checks = {
    "audit_campaign_lock_sha256": campaign_lock_path,
    "canonical_sha256": Path(paths["canonical"]),
    "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
    "trusted_translator_sha256": Path(paths["translator"]),
    "candidate_prompt_sha256": Path(paths["candidate"]) / "prompt.py",
    "candidate_translator_sha256": Path(paths["candidate"]) / "py2mpy.py",
    "run_manifest_sha256": Path(paths["run_manifest"]),
    "task_manifest_sha256": Path(paths["task_manifest"]),
    "stage1_result_sha256": Path(paths["stage1_result"]),
    "stage1_invocation_sha256": Path(paths["generation_manifest"]),
    "generation_metrics_sha256": Path(paths["generation_metrics"]),
    "generation_usage_sha256": Path(paths["generation_root"]) / "usage.json",
    "generation_codex_last_sha256": Path(paths["generation_last"]),
    "generation_codex_output_sha256": Path(paths["generation_output"]),
    "generation_prompt_sha256": Path(paths["generation_root"]) / "prompt.txt",
}

all_files_match = True
for key, path in file_checks.items():
    actual = sha256_file(path)
    expected = hashes[key]
    match = actual == expected and real_regular(path)
    all_files_match &= match
    print(f"{key}: expected={expected} actual={actual} real_regular={real_regular(path)} match={match}")

candidate_tree = sha256_tree(Path(paths["candidate"]))
trace_tree = sha256_tree(Path(paths["generation_trace"]))
generation_result = json.loads(Path(paths["stage1_result"]).read_text())
usage = json.loads((Path(paths["generation_root"]) / "usage.json").read_text())
print(
    "launcher_recorded_candidate_tree_sha256="
    f"{hashes['candidate_tree_sha256']}"
)
print(
    "launcher_recorded_generation_codex_trace_sha256="
    f"{hashes['generation_codex_trace_sha256']}"
)
print(
    "pipeline_contract_candidate_tree_sha256:"
    f" generation_result={generation_result['outputs']['workspace_sha256']}"
    f" mounted={candidate_tree}"
    f" match={candidate_tree == generation_result['outputs']['workspace_sha256']}"
)
print(
    "pipeline_contract_trace_tree_sha256:"
    f" usage={usage['source_trace_sha256']} mounted={trace_tree}"
    f" match={trace_tree == usage['source_trace_sha256']}"
)

required = [
    Path(paths["run_manifest"]),
    Path(paths["task_manifest"]),
    Path(paths["stage1_result"]),
    Path(paths["generation_manifest"]),
    Path(paths["generation_metrics"]),
    Path(paths["generation_last"]),
    Path(paths["generation_output"]),
    Path(paths["generation_root"]) / "prompt.txt",
]
print(f"required_layout_records_real_regular={all(real_regular(path) for path in required)}")
print(f"reference_semantics_absent={not Path('/reference/reference-semantics').exists()}")
print(
    "candidate_prompt_byte_equal_trusted="
    f"{(Path(paths['candidate']) / 'prompt.py').read_bytes() == Path(paths['trusted_prompt']).read_bytes()}"
)
print(
    "candidate_translator_byte_equal_trusted="
    f"{(Path(paths['candidate']) / 'py2mpy.py').read_bytes() == Path(paths['translator']).read_bytes()}"
)

trace_files = sorted(Path(paths["generation_trace"]).rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
trace_type_counts: Counter[str] = Counter()
trace_payload_type_counts: Counter[str] = Counter()
trace_lines = 0
for trace_file in trace_files:
    with trace_file.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            trace_lines += 1
            trace_type_counts[event.get("type", "<missing>")] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                trace_payload_type_counts[str(payload.get("type", "<missing>"))] += 1
print(f"trace_files={[str(path.relative_to(Path(paths['generation_trace']))) for path in trace_files]}")
print(f"trace_json_lines_parsed={trace_lines}")
print(f"trace_event_types={dict(sorted(trace_type_counts.items()))}")
print(f"trace_payload_types={dict(sorted(trace_payload_type_counts.items()))}")

output_path = Path(paths["generation_output"])
output_bytes = output_path.read_bytes()
output_text = output_bytes.decode("utf-8")
print(f"codex_output_bytes_read={len(output_bytes)}")
print(f"codex_output_lines_read={len(output_text.splitlines())}")
print(f"codex_output_top_markers={output_text.count('#Top')}")
print(f"codex_output_stuck_markers={output_text.count('WarnStuckClaimState')}")
print(f"all_recorded_file_hashes_match={all_files_match}")
