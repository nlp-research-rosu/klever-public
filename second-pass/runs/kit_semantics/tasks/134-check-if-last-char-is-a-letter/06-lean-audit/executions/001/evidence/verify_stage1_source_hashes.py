#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

audit_input = json.loads(Path("/audit-input.json").read_text())
recorded = audit_input["resolution"]["stage1_source_hashes"]
root = Path("/reference/k-proof")

observed = {
    relative: hashlib.sha256((root / relative).read_bytes()).hexdigest()
    for relative in recorded
    if (root / relative).is_file()
}
actual_files = sorted(
    path.relative_to(root).as_posix()
    for path in root.rglob("*")
    if path.is_file()
)
mismatches = {
    relative: {
        "recorded": digest,
        "observed": observed.get(relative),
    }
    for relative, digest in recorded.items()
    if observed.get(relative) != digest
}
extra = [relative for relative in actual_files if relative not in recorded]

print(
    json.dumps(
        {
            "recorded_file_count": len(recorded),
            "observed_file_count": len(observed),
            "actual_file_count": len(actual_files),
            "mismatches": mismatches,
            "extra_files": extra,
            "exact_file_hash_manifest_match": (
                not mismatches
                and not extra
                and len(observed) == len(recorded)
            ),
        },
        indent=2,
        sort_keys=True,
    )
)
