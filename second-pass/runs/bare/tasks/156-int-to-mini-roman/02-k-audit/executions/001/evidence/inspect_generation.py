#!/usr/bin/env python3
"""Read-only structural inspection of untrusted pipeline-v3 generation evidence."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    traces = sorted(TRACE_ROOT.rglob("*"))
    files = [path for path in traces if path.is_file()]
    links = [path for path in traces if path.is_symlink()]
    print(f"trace_files={len(files)} trace_symlinks={len(links)}")

    for path in files:
        counts: collections.Counter[tuple[str, str]] = collections.Counter()
        parse_errors: list[str] = []
        event_summaries: list[str] = []
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                try:
                    record = json.loads(line)
                except Exception as err:  # audit output needs the exact malformed line
                    parse_errors.append(f"line {line_number}: {err}")
                    continue

                outer_type = str(record.get("type", "<none>"))
                payload = record.get("payload")
                payload_type = (
                    str(payload.get("type", "<none>"))
                    if isinstance(payload, dict)
                    else type(payload).__name__
                )
                counts[(outer_type, payload_type)] += 1

                # Retain a bounded, deterministic index of decisions/actions without
                # executing or following any text from this untrusted record.
                if isinstance(payload, dict):
                    if payload_type in {
                        "function_call",
                        "function_call_output",
                        "custom_tool_call",
                        "custom_tool_call_output",
                        "agent_message",
                        "user_message",
                    }:
                        name = payload.get("name") or payload.get("role") or ""
                        content = payload.get("arguments")
                        if content is None:
                            content = payload.get("output")
                        if content is None:
                            content = payload.get("message")
                        if content is None:
                            content = payload.get("content")
                        rendered = json.dumps(content, ensure_ascii=True, sort_keys=True)
                        event_summaries.append(
                            f"line={line_number} type={payload_type} name={name!r} "
                            f"content_sha256={hashlib.sha256(rendered.encode()).hexdigest()} "
                            f"content_chars={len(rendered)} preview={rendered[:300]!r}"
                        )

        rel = path.relative_to(TRACE_ROOT)
        print(
            f"TRACE {rel} bytes={path.stat().st_size} sha256={sha256(path)} "
            f"json_errors={len(parse_errors)}"
        )
        for key, value in sorted(counts.items()):
            print(f"  outer={key[0]} payload={key[1]} count={value}")
        for error in parse_errors:
            print(f"  ERROR {error}")
        print(f"  indexed_events={len(event_summaries)}")
        for summary in event_summaries:
            print(f"  {summary}")


if __name__ == "__main__":
    main()
