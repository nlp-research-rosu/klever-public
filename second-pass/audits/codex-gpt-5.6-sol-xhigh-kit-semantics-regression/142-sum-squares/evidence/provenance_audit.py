#!/usr/bin/env python3
"""Read and summarize all untrusted generation/provenance claims."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path

CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")

REQUIRED_FILES = (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def describe(path: Path) -> str:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return "MISSING"
    if stat.S_ISLNK(mode):
        return f"SYMLINK->{os.readlink(path)}"
    if stat.S_ISREG(mode):
        return f"REGULAR bytes={path.stat().st_size} sha256={sha(path)}"
    if stat.S_ISDIR(mode):
        return "DIRECTORY"
    return f"OTHER mode={oct(mode)}"


def main() -> int:
    failures = []
    print("REQUIRED CANDIDATE ARTIFACT TYPES")
    for relative in REQUIRED_FILES:
        path = CANDIDATE / relative
        description = describe(path)
        print(f"{relative}: {description}")
        if not description.startswith("REGULAR"):
            failures.append(f"{relative}: {description}")

    print(f"reference-semantics: {describe(CANDIDATE / 'reference-semantics')}")
    if describe(CANDIDATE / "reference-semantics") != "DIRECTORY":
        failures.append("reference-semantics is not a directory")

    symlinks = sorted(str(p) for p in CANDIDATE.rglob("*") if p.is_symlink())
    print(f"CANDIDATE_SYMLINKS={json.dumps(symlinks)}")
    if symlinks:
        failures.extend(f"symlink:{path}" for path in symlinks)

    run_input = json.loads((CANDIDATE / "run-input.json").read_text())
    metrics = json.loads((CANDIDATE / "metrics.json").read_text())
    last = (CANDIDATE / "codex-last.txt").read_text()
    output = (CANDIDATE / "codex-output.log").read_text(errors="replace")

    print("UNTRUSTED_RUN_INPUT=" + json.dumps(run_input, sort_keys=True))
    print("UNTRUSTED_METRICS=" + json.dumps(metrics, sort_keys=True))
    print("UNTRUSTED_CODEX_LAST=" + json.dumps(last))
    print(
        "UNTRUSTED_CODEX_OUTPUT_SUMMARY="
        + json.dumps(
            {
                "characters": len(output),
                "lines": output.count("\n"),
                "sha256": sha(CANDIDATE / "codex-output.log"),
                "mentions_top": output.count("#Top"),
                "mentions_warn_stuck": output.count("WarnStuckClaimState"),
                "head": output[:500],
                "tail": output[-1000:],
            },
            sort_keys=True,
        )
    )

    traces = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
    print(f"STRUCTURED_TRACE_FILES={len(traces)}")
    for trace in traces:
        counts: Counter[str] = Counter()
        roles: Counter[str] = Counter()
        malformed = 0
        lines = 0
        characters = 0
        first_timestamp = None
        last_timestamp = None
        final_messages = []
        with trace.open(encoding="utf-8", errors="replace") as stream:
            for raw in stream:
                lines += 1
                characters += len(raw)
                try:
                    event = json.loads(raw)
                except json.JSONDecodeError:
                    malformed += 1
                    continue
                event_type = str(event.get("type"))
                counts[event_type] += 1
                timestamp = event.get("timestamp")
                if timestamp is not None:
                    first_timestamp = first_timestamp or timestamp
                    last_timestamp = timestamp
                payload = event.get("payload", {})
                if isinstance(payload, dict):
                    role = payload.get("role")
                    if role is not None:
                        roles[str(role)] += 1
                    if (
                        payload.get("type") == "message"
                        and payload.get("phase") == "final_answer"
                    ):
                        final_messages.append(payload)
        print(
            "TRACE_SUMMARY="
            + json.dumps(
                {
                    "path": str(trace),
                    "sha256": sha(trace),
                    "lines": lines,
                    "characters": characters,
                    "malformed_json_lines": malformed,
                    "event_types": counts,
                    "roles": roles,
                    "first_timestamp": first_timestamp,
                    "last_timestamp": last_timestamp,
                    "final_message_count": len(final_messages),
                    "final_message_tail": str(final_messages[-1])[-1000:]
                    if final_messages
                    else None,
                },
                sort_keys=True,
                default=dict,
            )
        )

    print(
        "TRUSTED_HASHES="
        + json.dumps(
            {
                "prompt.py": sha(REFERENCE / "prompt.py"),
                "py2mpy.py": sha(REFERENCE / "py2mpy.py"),
                "canonical.py": sha(REFERENCE / "canonical.py"),
            },
            sort_keys=True,
        )
    )
    print(f"ARTIFACT_TYPE_FAILURES={json.dumps(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
