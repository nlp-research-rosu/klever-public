#!/usr/bin/env python3
"""Independent launcher/provenance integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def regular(path: Path) -> bool:
    mode = path.lstat().st_mode
    return stat.S_ISREG(mode) and not path.is_symlink()


def sha256_tree(root: Path) -> str:
    """Reimplement the launcher's length-delimited tree digest."""
    digest = hashlib.sha256()
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
                raise ValueError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
expected = audit["hashes"]

print("COMMAND: python3 /audit-output/evidence/integrity_check.py")
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_structural_match={lock == audit['audit_campaign']}")
print(
    "campaign_hash_match="
    f"{sha256(LOCK) == expected['audit_campaign_lock_sha256']} "
    f"actual={sha256(LOCK)}"
)

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
usage = Path("/generation-evidence/usage.json")
if usage.exists() or usage.is_symlink():
    required.append(usage)

for path in required:
    print(
        f"required path={path} exists={path.exists()} "
        f"regular_no_symlink={regular(path) if path.exists() else False}"
    )
    if path.suffix == ".json":
        json.loads(path.read_text())

direct_hashes = {
    Path("/run.json"): expected["run_manifest_sha256"],
    Path("/task.json"): expected["task_manifest_sha256"],
    Path("/generation-result.json"): expected["stage1_result_sha256"],
    Path("/generation-evidence/invocation.json"): expected[
        "stage1_invocation_sha256"
    ],
    Path("/generation-evidence/metrics.json"): expected[
        "generation_metrics_sha256"
    ],
    Path("/generation-evidence/codex-last.txt"): expected[
        "generation_codex_last_sha256"
    ],
    Path("/generation-evidence/codex-output.log"): expected[
        "generation_codex_output_sha256"
    ],
    Path("/generation-evidence/prompt.txt"): expected[
        "generation_prompt_sha256"
    ],
    Path("/reference/canonical.py"): expected["canonical_sha256"],
    Path("/reference/prompt.py"): expected["trusted_prompt_sha256"],
    Path("/reference/py2mpy.py"): expected["trusted_translator_sha256"],
    Path("/candidate/prompt.py"): expected["candidate_prompt_sha256"],
    Path("/candidate/py2mpy.py"): expected["candidate_translator_sha256"],
}
if usage.exists():
    direct_hashes[usage] = expected["generation_usage_sha256"]

for path, wanted in direct_hashes.items():
    actual = sha256(path)
    print(
        f"hash path={path} match={actual == wanted} "
        f"actual={actual} expected={wanted}"
    )

print(
    "candidate_prompt_byte_identical="
    f"{Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
)
print(
    "candidate_translator_byte_identical="
    f"{Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
)
print(
    "generated_mode_reference_semantics_absent="
    f"{not Path('/reference/reference-semantics').exists() and not Path('/reference/reference-semantics').is_symlink()}"
)
print(
    "candidate_reference_semantics_absent="
    f"{not Path('/candidate/reference-semantics').exists() and not Path('/candidate/reference-semantics').is_symlink()}"
)

for root in (Path("/candidate"), Path("/generation-evidence/codex-trace")):
    entries = sorted(root.rglob("*"))
    bad = [
        str(path)
        for path in entries
        if path.is_symlink() or not (path.is_file() or path.is_dir())
    ]
    print(f"tree root={root} entries={len(entries)} bad_entry_count={len(bad)}")
    for path in bad:
        print(f"bad_entry={path}")

result_document = json.loads(Path("/generation-result.json").read_text())
usage_document = json.loads(usage.read_text()) if usage.exists() else {}
pipeline_tree_checks = {
    Path("/candidate"): result_document["outputs"]["workspace_sha256"],
    Path("/generation-evidence/codex-trace"): usage_document.get(
        "source_trace_sha256"
    ),
}
for root, wanted in pipeline_tree_checks.items():
    actual = sha256_tree(root)
    print(
        f"pipeline_tree_hash root={root} match={actual == wanted} "
        f"actual={actual} expected={wanted}"
    )
print(
    "audit_input_tree_aggregate_values="
    + json.dumps(
        {
            "candidate_tree_sha256": expected["candidate_tree_sha256"],
            "generation_codex_trace_sha256": expected[
                "generation_codex_trace_sha256"
            ],
        },
        sort_keys=True,
    )
    + " note=audit-input does not declare the distinct aggregate framing"
)

result = result_document
evidence_hashes = result["outputs"]["evidence"]
for relative, wanted in sorted(evidence_hashes.items()):
    path = Path("/generation-evidence") / relative
    actual = sha256(path)
    print(
        f"stage1_evidence path={relative} match={actual == wanted} "
        f"actual={actual} expected={wanted}"
    )

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
trace_records = 0
for path in trace_files:
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            json.loads(line)
            trace_records += 1
print(
    f"trace_files={len(trace_files)} trace_records={trace_records} "
    "all_json_records_valid=true"
)

for path in (
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/codex-last.txt"),
):
    data = path.read_bytes()
    print(
        f"fully_read path={path} bytes={len(data)} "
        f"lines={data.count(os.linesep.encode())}"
    )
