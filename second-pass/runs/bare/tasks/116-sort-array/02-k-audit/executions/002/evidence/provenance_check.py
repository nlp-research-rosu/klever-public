#!/usr/bin/env python3
"""Independent integrity checks over launcher-mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha(root: str | Path) -> str:
    """Reimplement the pipeline-v2 length-delimited workspace hash."""
    root = Path(root)
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
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
    digest = hashlib.sha256()
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


audit = load("/audit-input.json")
campaign = load("/audit-campaign-lock.json")
invocation = load("/generation-evidence/invocation.json")
usage = load("/generation-evidence/usage.json")
result = load("/generation-result.json")

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_block_exact_match={campaign == audit['audit_campaign']}")
campaign_actual = sha("/audit-campaign-lock.json")
campaign_expected = audit["hashes"]["audit_campaign_lock_sha256"]
print(f"campaign_sha256 actual={campaign_actual} expected={campaign_expected}")

required_files = [
    "/audit-input.json",
    "/audit-campaign-lock.json",
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/usage.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
    "/reference/canonical.py",
    "/reference/prompt.py",
    "/reference/py2mpy.py",
]
for value in required_files:
    path = Path(value)
    mode = path.lstat().st_mode
    print(
        f"required_file path={value} regular={stat.S_ISREG(mode)} "
        f"symlink={stat.S_ISLNK(mode)} readable={os.access(path, os.R_OK)}"
    )

required_directories = [
    "/candidate",
    "/generation-evidence",
    "/generation-evidence/codex-trace",
]
for value in required_directories:
    path = Path(value)
    mode = path.lstat().st_mode
    print(
        f"required_directory path={value} directory={stat.S_ISDIR(mode)} "
        f"symlink={stat.S_ISLNK(mode)} readable={os.access(path, os.R_OK)}"
    )

for root in (Path("/candidate"), Path("/generation-evidence/codex-trace")):
    unsupported = []
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
            unsupported.append(str(path))
    print(f"tree={root} linked_or_unsupported_entries={unsupported!r}")

file_checks = [
    ("/candidate/prompt.py", "candidate_prompt_sha256"),
    ("/candidate/py2mpy.py", "candidate_translator_sha256"),
    ("/reference/prompt.py", "trusted_prompt_sha256"),
    ("/reference/py2mpy.py", "trusted_translator_sha256"),
    ("/reference/canonical.py", "canonical_sha256"),
    ("/generation-evidence/invocation.json", "stage1_invocation_sha256"),
    ("/generation-evidence/metrics.json", "generation_metrics_sha256"),
    ("/generation-evidence/usage.json", "generation_usage_sha256"),
    ("/generation-evidence/codex-last.txt", "generation_codex_last_sha256"),
    ("/generation-evidence/codex-output.log", "generation_codex_output_sha256"),
    ("/generation-evidence/prompt.txt", "generation_prompt_sha256"),
    ("/run.json", "run_manifest_sha256"),
    ("/task.json", "task_manifest_sha256"),
    ("/generation-result.json", "stage1_result_sha256"),
]
for path, key in file_checks:
    actual = sha(path)
    expected = audit["hashes"][key]
    print(f"file_sha256 path={path} actual={actual} expected={expected} match={actual == expected}")

for relative, expected in invocation["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    actual = sha(path)
    print(
        f"invocation_evidence path={path} actual={actual} "
        f"expected={expected} match={actual == expected}"
    )

candidate_pipeline = pipeline_tree_sha("/candidate")
trace_pipeline = pipeline_tree_sha("/generation-evidence/codex-trace")
print(f"candidate_pipeline_tree_sha256={candidate_pipeline}")
print(f"invocation_workspace_sha256={invocation['inputs']['workspace_sha256']}")
print(f"result_workspace_sha256={result['outputs']['workspace_sha256']}")
print(f"audit_input_candidate_tree_sha256={audit['hashes']['candidate_tree_sha256']}")
print(f"trace_pipeline_tree_sha256={trace_pipeline}")
print(f"usage_source_trace_sha256={usage['source_trace_sha256']}")
print(f"audit_input_generation_trace_sha256={audit['hashes']['generation_codex_trace_sha256']}")

print(
    "candidate_prompt_matches_trusted_bytes="
    f"{Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
)
print(
    "candidate_translator_matches_trusted_bytes="
    f"{Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
)
reference_semantics = Path("/reference/reference-semantics")
print(
    f"generated_semantics_boundary reference_semantics_exists={reference_semantics.exists()} "
    f"reference_semantics_symlink={reference_semantics.is_symlink()}"
)
