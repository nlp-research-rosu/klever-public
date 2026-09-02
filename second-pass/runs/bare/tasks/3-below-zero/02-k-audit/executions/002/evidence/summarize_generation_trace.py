#!/usr/bin/env python3
"""Bounded structural summary of the untrusted generation trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T03-47-50-019f8902-8159-76f2-9c40-9f32993e10f1.jsonl"
)
rows = [json.loads(line) for line in trace.read_text().splitlines()]
print(f"valid_jsonl_lines={len(rows)}")
print("top_types=" + repr(dict(collections.Counter(row.get("type") for row in rows))))
print(
    "payload_types="
    + repr(dict(collections.Counter((row.get("payload") or {}).get("type") for row in rows)))
)

needles = (
    "kompile ",
    "krun ",
    "kprove ",
    "#Top",
    "WarnStuckClaimState",
    "KPROVE_PASSED",
    "Process exited",
    "Parse error",
)
for number, row in enumerate(rows, 1):
    payload = row.get("payload") or {}
    kind = payload.get("type")
    value = (
        payload.get("input")
        or payload.get("arguments")
        or payload.get("output")
        or payload.get("message")
        or payload.get("text")
        or payload.get("content")
        or ""
    )
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)
    value = str(value)
    hits = [needle for needle in needles if needle in value]
    if hits:
        bounded = value.replace("\n", "\\n")
        print(
            f"line={number} type={kind} len={len(value)} "
            f"hits={hits!r} text={bounded[:1200]}"
        )
