#!/usr/bin/env python3
"""Read and summarize all required untrusted provenance artifacts."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")
TRACE_FILES = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
PLAIN_FILES = [
    CANDIDATE / "run-input.json",
    CANDIDATE / "metrics.json",
    CANDIDATE / "codex-last.txt",
    CANDIDATE / "codex-output.log",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


for path in PLAIN_FILES:
    data = path.read_bytes()
    text = data.decode("utf-8")
    print(f"FILE {path}")
    print(f"  bytes={len(data)} lines={len(text.splitlines())} sha256={sha256(data)}")
    print(f"  utf8=valid")
    if path.suffix == ".json":
        document = json.loads(text)
        print(f"  json=valid keys={sorted(document)}")
    print(f"  count_#Top={text.count('#Top')}")
    print(f"  count_WarnStuckClaimState={text.count('WarnStuckClaimState')}")
    print(f"  count_RESULT_KPROVE_PASSED={text.count('RESULT: KPROVE_PASSED')}")
    print(f"  first_line={text.splitlines()[0] if text.splitlines() else ''!r}")
    print(f"  last_line={text.splitlines()[-1] if text.splitlines() else ''!r}")

print(f"TRACE_FILE_COUNT={len(TRACE_FILES)}")
for path in TRACE_FILES:
    data = path.read_bytes()
    text = data.decode("utf-8")
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    invalid: list[tuple[int, str]] = []
    last_object: object = None
    for line_number, line in enumerate(text.splitlines(), 1):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as err:
            invalid.append((line_number, str(err)))
            continue
        last_object = obj
        if isinstance(obj, dict):
            top_types[str(obj.get("type", "<none>"))] += 1
            payload = obj.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type", "<none>"))] += 1
    print(f"TRACE {path}")
    print(f"  bytes={len(data)} lines={len(text.splitlines())} sha256={sha256(data)}")
    print(f"  utf8=valid invalid_json_lines={len(invalid)}")
    print(f"  top_types={dict(sorted(top_types.items()))}")
    print(f"  payload_types={dict(sorted(payload_types.items()))}")
    print(f"  count_#Top={text.count('#Top')}")
    print(f"  count_WarnStuckClaimState={text.count('WarnStuckClaimState')}")
    print(f"  count_RESULT_KPROVE_PASSED={text.count('RESULT: KPROVE_PASSED')}")
    if isinstance(last_object, dict):
        print(f"  last_type={last_object.get('type')!r}")
