#!/usr/bin/env python3
"""Summarize candidate generation records strictly as untrusted claims."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path("/candidate")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    print("ALL_OUTPUT_BELOW_IS_UNTRUSTED_CANDIDATE_METADATA")
    for name in ["run-input.json", "metrics.json"]:
        path = ROOT / name
        value = json.loads(path.read_text(encoding="utf-8"))
        print(f"{name}_sha256={digest(path)}")
        print(f"{name}={json.dumps(value, sort_keys=True)}")

    for name in ["codex-last.txt", "codex-output.log"]:
        path = ROOT / name
        text = path.read_text(encoding="utf-8", errors="replace")
        print(f"{name}_sha256={digest(path)}")
        print(f"{name}_bytes={len(text.encode('utf-8'))}")
        print(f"{name}_top_token_count={text.count('#Top')}")
        print(f"{name}_stuck_token_count={text.count('WarnStuckClaimState')}")
        print(f"{name}_result_marker_count={text.count('RESULT:')}")
        if name == "codex-last.txt":
            print("codex-last.txt_content=" + repr(text))

    traces = sorted((ROOT / "codex-trace").rglob("*.jsonl"))
    print(f"trace_files={len(traces)}")
    for trace in traces:
        lines = 0
        invalid = 0
        outer_types = Counter()
        payload_types = Counter()
        task_complete = []
        with trace.open(encoding="utf-8") as stream:
            for raw in stream:
                lines += 1
                try:
                    item = json.loads(raw)
                except json.JSONDecodeError:
                    invalid += 1
                    continue
                outer_types[item.get("type", "<missing>")] += 1
                payload = item.get("payload")
                if isinstance(payload, dict):
                    payload_types[payload.get("type", "<missing>")] += 1
                    if payload.get("type") == "task_complete":
                        task_complete.append(payload)
        print(f"trace={trace}")
        print(f"trace_sha256={digest(trace)}")
        print(f"trace_lines={lines}")
        print(f"trace_invalid_json_lines={invalid}")
        print(f"trace_outer_types={dict(sorted(outer_types.items()))}")
        print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
        print(f"trace_task_complete={json.dumps(task_complete, sort_keys=True)}")


if __name__ == "__main__":
    main()
