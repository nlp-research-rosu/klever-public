#!/usr/bin/env python3
"""Read and summarize every pipeline-v3 provenance record and trace event."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
TRACE_ROOT = Path("/generation-evidence/codex-trace")
REQUIRED = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def main() -> None:
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_lock_matches_embedded={lock == audit['audit_campaign']}")
    print(f"campaign_lock_sha256={digest(LOCK)}")
    print(f"campaign_lock_recorded={audit['hashes']['audit_campaign_lock_sha256']}")

    for path in REQUIRED:
        mode = path.lstat().st_mode
        print(
            "required "
            f"path={path} regular={stat.S_ISREG(mode)} symlink={stat.S_ISLNK(mode)} "
            f"readable={os.access(path, os.R_OK)} sha256={digest(path)}"
        )

    for label, path_text in sorted(audit["container_paths"].items()):
        path = Path(path_text)
        mode = path.lstat().st_mode
        print(
            "container_path "
            f"label={label} path={path} directory={stat.S_ISDIR(mode)} "
            f"regular={stat.S_ISREG(mode)} symlink={stat.S_ISLNK(mode)} "
            f"readable={os.access(path, os.R_OK)}"
        )

    top_counts: Counter[str] = Counter()
    payload_counts: Counter[str] = Counter()
    response_counts: Counter[str] = Counter()
    roles: Counter[str] = Counter()
    command_count = 0
    command_failures = 0
    malformed = 0
    events = 0
    first_timestamp = None
    last_timestamp = None
    trace_files = sorted(TRACE_ROOT.rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    print(f"trace_file_count={len(trace_files)}")
    for trace in trace_files:
        print(f"trace_file path={trace} sha256={digest(trace)}")
        with trace.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    malformed += 1
                    continue
                events += 1
                timestamp = event.get("timestamp")
                first_timestamp = first_timestamp or timestamp
                last_timestamp = timestamp
                top_counts[event.get("type", "<missing>")] += 1
                payload = event.get("payload", {})
                if isinstance(payload, dict):
                    payload_type = payload.get("type", "<missing>")
                    payload_counts[payload_type] += 1
                    if event.get("type") == "response_item":
                        response_counts[payload_type] += 1
                        if payload_type == "message":
                            roles[payload.get("role", "<missing>")] += 1
                        if payload_type == "function_call":
                            command_count += 1
                        if payload_type == "function_call_output":
                            output = payload.get("output", "")
                            if isinstance(output, str) and "Process exited with code 0" not in output:
                                command_failures += 1

    with Path("/generation-evidence/codex-output.log").open(
        encoding="utf-8", errors="replace"
    ) as stream:
        output_lines = sum(1 for _ in stream)
    print(f"codex_output_lines_read={output_lines}")
    print(f"trace_events={events}")
    print(f"trace_malformed_lines={malformed}")
    print(f"trace_first_timestamp={first_timestamp}")
    print(f"trace_last_timestamp={last_timestamp}")
    print(f"trace_top_types={dict(sorted(top_counts.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_counts.items()))}")
    print(f"trace_response_types={dict(sorted(response_counts.items()))}")
    print(f"trace_message_roles={dict(sorted(roles.items()))}")
    print(f"trace_function_calls={command_count}")
    print(f"trace_nonzero_or_unclassified_outputs={command_failures}")


if __name__ == "__main__":
    main()
