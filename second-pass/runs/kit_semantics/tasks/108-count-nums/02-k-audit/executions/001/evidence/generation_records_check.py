#!/usr/bin/env python3
"""Parse every required pipeline-v3 record and summarize the untrusted trace."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


JSON_RECORDS = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
]


def main() -> int:
    ok = True
    for path in JSON_RECORDS:
        try:
            record = json.loads(path.read_text())
            print(
                f"JSON OK {path} type={type(record).__name__} "
                f"top_keys={sorted(record) if isinstance(record, dict) else 'n/a'}"
            )
        except Exception as err:
            ok = False
            print(f"JSON ERROR {path}: {err}")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    regular_trace_files = [path for path in trace_files if path.is_file()]
    print(f"TRACE FILE COUNT {len(regular_trace_files)}")
    for path in regular_trace_files:
        type_counts: collections.Counter[str] = collections.Counter()
        payload_type_counts: collections.Counter[str] = collections.Counter()
        invalid = 0
        lines = 0
        final_event: dict | None = None
        with path.open(errors="replace") as stream:
            for line_number, line in enumerate(stream, 1):
                lines = line_number
                try:
                    event = json.loads(line)
                except Exception:
                    invalid += 1
                    continue
                type_counts[str(event.get("type"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_type_counts[str(payload.get("type"))] += 1
                final_event = event
        print(f"TRACE {path} lines={lines} invalid_json={invalid}")
        print(f"  event_types={dict(sorted(type_counts.items()))}")
        print(f"  payload_types={dict(sorted(payload_type_counts.items()))}")
        if final_event is not None:
            print(
                "  final_event="
                + json.dumps(final_event, sort_keys=True, ensure_ascii=True)[:1000]
            )
        ok &= invalid == 0 and lines > 0

    for path in (
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/prompt.txt"),
    ):
        text = path.read_text(errors="replace")
        line_count = text.count("\n") + (not text.endswith("\n"))
        print(
            f"TEXT READ {path} chars={len(text)} lines={line_count} "
            f"nul_bytes={text.count(chr(0))}"
        )
        for needle in (
            "#Top",
            "WarnStuckClaimState",
            "VALIDATED",
            "KPROVE_PASSED",
            "apply patch",
            "kprove",
        ):
            print(f"  occurrences[{needle!r}]={text.count(needle)}")

    print(f"GENERATION_RECORDS={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
