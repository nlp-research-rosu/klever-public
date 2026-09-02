#!/usr/bin/env python3
"""Read and summarize every pipeline-v3 generation record as untrusted claims."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT_LOG = Path("/generation-evidence/codex-output.log")


def compact(text: str, limit: int = 220) -> str:
    one_line = " ".join(text.split())
    return one_line if len(one_line) <= limit else one_line[: limit - 3] + "..."


def main() -> None:
    for path in [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
    ]:
        obj = json.loads(path.read_text())
        print(f"JSON RECORD READ {path} top-level={sorted(obj)}")

    for path in [
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/prompt.txt"),
    ]:
        text = path.read_text()
        print(
            f"TEXT RECORD READ {path} lines={len(text.splitlines())} "
            f"bytes={len(text.encode())} first={compact(text)}"
        )

    output_text = OUTPUT_LOG.read_text(errors="replace")
    output_lines = output_text.splitlines()
    print(
        f"TEXT RECORD READ {OUTPUT_LOG} lines={len(output_lines)} "
        f"bytes={len(output_text.encode())}"
    )
    interesting = re.compile(
        r"(kprove|kompile|krun|#Top|WarnStuckClaimState|EXPECTED|RESULT:|"
        r"VALIDATED|error|failed|exit code)",
        re.IGNORECASE,
    )
    matches = [(index + 1, line) for index, line in enumerate(output_lines) if interesting.search(line)]
    print(f"CODEX OUTPUT INTERESTING LINES {len(matches)}")
    for index, line in matches[:160]:
        print(f"OUTPUT {index}: {compact(line, 360)}")
    if len(matches) > 160:
        print(f"OUTPUT ... omitted {len(matches) - 160} additional matching lines")
        for index, line in matches[-20:]:
            print(f"OUTPUT-TAIL {index}: {compact(line, 360)}")

    trace_files = sorted(path for path in TRACE_ROOT.rglob("*") if path.is_file())
    print(f"TRACE FILE COUNT {len(trace_files)}")
    for trace_path in trace_files:
        counts: collections.Counter[str] = collections.Counter()
        payload_counts: collections.Counter[str] = collections.Counter()
        tool_calls: list[tuple[int, str, str]] = []
        assistant_messages: list[tuple[int, str, str]] = []
        final_candidates: list[tuple[int, str]] = []
        parse_errors: list[str] = []
        lines = trace_path.read_text(errors="replace").splitlines()
        for line_number, line in enumerate(lines, start=1):
            try:
                event = json.loads(line)
            except json.JSONDecodeError as err:
                parse_errors.append(f"line {line_number}: {err}")
                continue
            event_type = str(event.get("type"))
            counts[event_type] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type"))
                payload_counts[payload_type] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    name = str(payload.get("name", ""))
                    arguments = str(
                        payload.get("arguments", payload.get("input", ""))
                    )
                    tool_calls.append((line_number, name, compact(arguments, 420)))
                if payload_type in {"agent_message", "message"}:
                    message = payload.get("message")
                    if not isinstance(message, str):
                        content = payload.get("content")
                        if isinstance(content, list):
                            message = " ".join(
                                str(item.get("text", ""))
                                for item in content
                                if isinstance(item, dict)
                            )
                    if isinstance(message, str):
                        assistant_messages.append(
                            (
                                line_number,
                                str(payload.get("phase", "")),
                                compact(message, 420),
                            )
                        )
                        if "RESULT:" in message:
                            final_candidates.append((line_number, compact(message, 600)))
        print(
            f"TRACE READ {trace_path} lines={len(lines)} bytes={trace_path.stat().st_size}"
        )
        print(f"TRACE EVENT COUNTS {dict(sorted(counts.items()))}")
        print(f"TRACE PAYLOAD COUNTS {dict(sorted(payload_counts.items()))}")
        print(f"TRACE PARSE ERRORS {len(parse_errors)}")
        for item in parse_errors:
            print(f"TRACE PARSE ERROR {item}")
        print(f"TRACE TOOL CALLS {len(tool_calls)}")
        for line_number, name, arguments in tool_calls:
            print(f"TRACE TOOL line={line_number} name={name} args={arguments}")
        print(f"TRACE ASSISTANT MESSAGES {len(assistant_messages)}")
        for line_number, phase, message in assistant_messages:
            print(f"TRACE MESSAGE line={line_number} phase={phase}: {message}")
        print(f"TRACE FINAL CANDIDATES {len(final_candidates)}")
        for line_number, message in final_candidates:
            print(f"TRACE FINAL line={line_number}: {message}")


if __name__ == "__main__":
    main()
