#!/usr/bin/env python3
"""Bounded summary of untrusted generation claims and structured trace."""

from __future__ import annotations

import collections
import glob
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def text_claim_summary(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    interesting = [
        line
        for line in text.splitlines()
        if "#Top" in line
        or "RESULT:" in line
        or "KPROVE" in line
        or "kprove" in line.lower()
    ]
    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "line_count": len(text.splitlines()),
        "sha256": sha256(path),
        "bounded_status_lines": interesting[-30:],
    }


def main() -> int:
    trace_summaries = []
    for raw_path in glob.glob(str(CANDIDATE / "codex-trace" / "**" / "*.jsonl"), recursive=True):
        path = Path(raw_path)
        counts: collections.Counter[str] = collections.Counter()
        parse_errors = []
        call_names: collections.Counter[str] = collections.Counter()
        final_agent_messages = []
        with path.open(encoding="utf-8", errors="replace") as stream:
            for line_number, line in enumerate(stream, 1):
                try:
                    event = json.loads(line)
                except Exception as error:
                    parse_errors.append({"line": line_number, "error": str(error)})
                    continue
                payload = event.get("payload") or {}
                event_key = f"{event.get('type')}::{payload.get('type')}"
                counts[event_key] += 1
                if payload.get("type") in {"function_call", "custom_tool_call"}:
                    call_names[str(payload.get("name"))] += 1
                if (
                    payload.get("type") == "message"
                    and payload.get("role") == "assistant"
                ):
                    final_agent_messages.append(str(payload.get("content")))
        trace_summaries.append(
            {
                "path": str(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "event_counts": dict(sorted(counts.items())),
                "call_names": dict(sorted(call_names.items())),
                "parse_errors": parse_errors,
                "bounded_final_assistant_messages": final_agent_messages[-3:],
            }
        )

    result = {
        "run_input_untrusted_claim": json.loads(
            (CANDIDATE / "run-input.json").read_text(encoding="utf-8")
        ),
        "metrics_untrusted_claim": json.loads(
            (CANDIDATE / "metrics.json").read_text(encoding="utf-8")
        ),
        "codex_last": text_claim_summary(CANDIDATE / "codex-last.txt"),
        "codex_output": text_claim_summary(CANDIDATE / "codex-output.log"),
        "structured_traces": trace_summaries,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
