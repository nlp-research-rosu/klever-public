#!/usr/bin/env python3
"""Read every line of the untrusted generation output and report bounded facts."""

from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import re


def main() -> int:
    path = pathlib.Path("/generation-evidence/codex-output.log")
    digest = hashlib.sha256()
    counts: collections.Counter[str] = collections.Counter()
    patterns = {
        "top": re.compile(r"(?m)^#Top\s*$"),
        "stuck": re.compile(r"WarnStuckClaimState"),
        "prover_error": re.compile(r"\[Error\] Prover"),
        "result_marker": re.compile(r"RESULT: KPROVE_PASSED"),
        "timeout": re.compile(r"(?i)timed out|timeout"),
    }
    first = ""
    last = ""
    line_count = 0
    with path.open("rb") as stream:
        for line_count, raw_line in enumerate(stream, 1):
            digest.update(raw_line)
            text = raw_line.decode("utf-8", errors="replace")
            if line_count == 1:
                first = text.rstrip("\n")
            last = text.rstrip("\n")
            for name, pattern in patterns.items():
                counts[name] += len(pattern.findall(text))

    usage = json.loads(pathlib.Path("/generation-evidence/usage.json").read_text())
    trace = pathlib.Path(
        "/generation-evidence/codex-trace/2026/07/23/"
        "rollout-2026-07-23T06-51-52-019f8ed1-593f-7043-8052-4f7d9771884d.jsonl"
    )
    actual_trace_hash = hashlib.sha256(trace.read_bytes()).hexdigest()
    recorded_usage_trace_hash = usage.get("source_trace_sha256")

    print(f"path={path}")
    print(f"sha256={digest.hexdigest()}")
    print(f"lines={line_count}")
    print("pattern_counts=" + json.dumps(dict(sorted(counts.items())), sort_keys=True))
    print(f"first_line={first[:500]!r}")
    print(f"last_line={last[:500]!r}")
    print(f"actual_trace_sha256={actual_trace_hash}")
    print(f"usage_source_trace_sha256={recorded_usage_trace_hash}")
    print(f"usage_trace_hash_matches={actual_trace_hash == recorded_usage_trace_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
