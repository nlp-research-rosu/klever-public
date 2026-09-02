#!/usr/bin/env python3
"""Read all untrusted generation records and print a bounded structural summary."""

from __future__ import annotations

import collections
import json
from pathlib import Path


CANDIDATE = Path("/candidate")


def main() -> int:
    for name in ("run-input.json", "metrics.json"):
        path = CANDIDATE / name
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
        print(f"{name}: valid JSON; top-level keys={sorted(value)}")
        print(json.dumps(value, sort_keys=True, indent=2))

    for name in ("codex-last.txt", "codex-output.log"):
        path = CANDIDATE / name
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        print(
            f"{name}: bytes={path.stat().st_size}; lines={len(lines)}; "
            f"kprove_mentions={text.count('kprove')}; "
            f"top_mentions={text.count('#Top')}; "
            f"stuck_mentions={text.count('WarnStuckClaimState')}"
        )
        if name == "codex-last.txt":
            print(text)
        else:
            salient = [
                line
                for line in lines
                if any(
                    marker in line
                    for marker in (
                        "RESULT:",
                        "#Top",
                        "WarnStuckClaimState",
                        "[Error]",
                        "kprove spec.k",
                    )
                )
            ]
            print("codex-output.log salient tail:")
            for line in salient[-80:]:
                print(line)

    traces = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
    print(f"structured traces: {len(traces)}")
    for trace in traces:
        type_counts: collections.Counter[str] = collections.Counter()
        payload_counts: collections.Counter[str] = collections.Counter()
        tool_names: collections.Counter[str] = collections.Counter()
        final_messages: list[str] = []
        line_count = 0
        with trace.open(encoding="utf-8") as handle:
            for line_count, line in enumerate(handle, 1):
                item = json.loads(line)
                type_counts[str(item.get("type"))] += 1
                payload = item.get("payload")
                if isinstance(payload, dict):
                    payload_counts[str(payload.get("type"))] += 1
                    name = payload.get("name")
                    if name:
                        tool_names[str(name)] += 1
                    if payload.get("type") == "message" and payload.get("role") == "assistant":
                        content = payload.get("content")
                        if isinstance(content, list):
                            texts = [
                                str(block.get("text", ""))
                                for block in content
                                if isinstance(block, dict)
                            ]
                            if texts:
                                final_messages.append("\n".join(texts))
        print(
            f"{trace}: valid JSONL; lines={line_count}; "
            f"event_types={dict(type_counts)}"
        )
        print(f"payload_types={dict(payload_counts)}")
        print(f"tool_names={dict(tool_names)}")
        if final_messages:
            print("last assistant message:")
            print(final_messages[-1][-4000:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
