#!/usr/bin/env python3
"""Stream and structurally inspect every required legacy-selected-stage1 record."""

from __future__ import annotations

import collections
import json
from pathlib import Path


json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/legacy-metrics.json"),
    Path("/generation-evidence/legacy-run-input.json"),
]
for path in json_records:
    document = json.loads(path.read_text())
    print(
        f"JSON_OK path={path} bytes={path.stat().st_size} "
        f"top_type={type(document).__name__}"
    )

for path in [
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/prompt.txt"),
]:
    text = path.read_text()
    print(
        f"TEXT_OK path={path} bytes={len(text.encode())} "
        f"lines={len(text.splitlines())}"
    )

log_path = Path("/generation-evidence/codex-output.log")
log_lines = 0
log_markers = collections.Counter()
with log_path.open(errors="strict") as stream:
    for line in stream:
        log_lines += 1
        for marker in [
            "kompile",
            "krun",
            "kprove",
            "#Top",
            "WarnStuckClaimState",
            "RESULT: KPROVE_PASSED",
            "VFruits",
            "invokeFruit",
            "invokeString",
        ]:
            if marker in line:
                log_markers[marker] += 1
print(
    f"TEXT_OK path={log_path} bytes={log_path.stat().st_size} "
    f"lines={log_lines} marker_counts={dict(log_markers)}"
)

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
assert trace_files
for path in trace_files:
    event_types = collections.Counter()
    records = 0
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            assert isinstance(event, dict), (path, line_number)
            records += 1
            event_types[str(event.get("type", "<none>"))] += 1
    print(
        f"JSONL_OK path={path} bytes={path.stat().st_size} "
        f"records={records} event_types={dict(sorted(event_types.items()))}"
    )

print("UNTRUSTED_CLAIM_OBSERVED=result_marker KPROVE_PASSED")
print("UNTRUSTED_CLAIM_OBSERVED=final report says ./prove.sh exited 0 with #Top")
