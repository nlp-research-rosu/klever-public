#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys


AUDIT_INPUT = Path("/audit-input.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_file(path: Path, expected: str | None = None) -> bool:
    if not path.exists() or not path.is_file() or path.is_symlink():
        print(f"BAD_FILE {path}: absent, non-regular, or symlink")
        return False
    actual = digest(path)
    verdict = "OK" if expected is None or actual == expected else "MISMATCH"
    print(f"{verdict} {path} sha256={actual} expected={expected}")
    return verdict == "OK"


def scan_links(root: Path) -> bool:
    found = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in [*dirnames, *filenames]:
            path = Path(dirpath, name)
            if path.is_symlink():
                found.append(path)
    print(f"SYMLINK_SCAN {root}: {len(found)} found")
    for path in found:
        print(f"  {path} -> {os.readlink(path)}")
    return not found


def main() -> int:
    data = json.loads(AUDIT_INPUT.read_text())
    hashes = data["hashes"]
    ok = True

    required = {
        Path("/audit-campaign-lock.json"): hashes["audit_campaign_lock_sha256"],
        Path("/reference/canonical.py"): hashes["canonical_sha256"],
        Path("/reference/prompt.py"): hashes["trusted_prompt_sha256"],
        Path("/reference/py2mpy.py"): hashes["trusted_translator_sha256"],
        Path("/run.json"): hashes["run_manifest_sha256"],
        Path("/task.json"): hashes["task_manifest_sha256"],
        Path("/generation-result.json"): hashes["stage1_result_sha256"],
        Path("/generation-evidence/invocation.json"): hashes["stage1_invocation_sha256"],
        Path("/generation-evidence/metrics.json"): hashes["generation_metrics_sha256"],
        Path("/generation-evidence/usage.json"): hashes["generation_usage_sha256"],
        Path("/generation-evidence/codex-last.txt"): hashes[
            "generation_codex_last_sha256"
        ],
        Path("/generation-evidence/codex-output.log"): hashes[
            "generation_codex_output_sha256"
        ],
        Path("/generation-evidence/prompt.txt"): hashes["generation_prompt_sha256"],
    }
    for path, expected in required.items():
        ok &= check_file(path, expected)

    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    campaign_same = lock == data["audit_campaign"]
    print(f"CAMPAIGN_BLOCK_MATCH={campaign_same}")
    ok &= campaign_same

    candidate_prompt_same = (
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes()
    )
    candidate_translator_same = (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    print(f"CANDIDATE_PROMPT_BYTE_IDENTICAL={candidate_prompt_same}")
    print(f"CANDIDATE_TRANSLATOR_BYTE_IDENTICAL={candidate_translator_same}")
    ok &= candidate_prompt_same and candidate_translator_same

    trusted_semantics_absent = not Path("/reference/reference-semantics").exists()
    candidate_semantics_absent = not Path("/candidate/reference-semantics").exists()
    print(f"TRUSTED_REFERENCE_SEMANTICS_ABSENT={trusted_semantics_absent}")
    print(f"CANDIDATE_REFERENCE_SEMANTICS_ABSENT={candidate_semantics_absent}")
    ok &= trusted_semantics_absent and candidate_semantics_absent

    for root in (
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ):
        ok &= scan_links(root)

    result = json.loads(Path("/generation-result.json").read_text())
    declared_outputs = result["outputs"]["evidence"]
    for relative, expected in sorted(declared_outputs.items()):
        ok &= check_file(Path("/generation-evidence", relative), expected)

    print(f"RECORD_LAYOUT={data['record_layout']}")
    print(f"SEMANTICS_MODE={data['semantics_mode']}")
    print(f"OVERALL={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
