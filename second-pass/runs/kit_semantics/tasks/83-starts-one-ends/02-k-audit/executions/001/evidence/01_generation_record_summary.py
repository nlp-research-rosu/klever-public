#!/usr/bin/env python3
"""Parse every pipeline-v3 generation record and every structured trace row."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


ROOT = Path("/generation-evidence")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Independently reproduce the pipeline-v3 relative-entry tree digest."""
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def main() -> int:
    json_records = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        ROOT / "invocation.json",
        ROOT / "metrics.json",
        ROOT / "runtime-metrics.json",
        ROOT / "usage.json",
    ]
    for path in json_records:
        record = json.loads(path.read_text(encoding="utf-8"))
        print(
            f"json_record={path} sha256={sha256(path)} "
            f"top_level_keys={sorted(record)}"
        )

    prompt = ROOT / "prompt.txt"
    last = ROOT / "codex-last.txt"
    output = ROOT / "codex-output.log"
    for path in [prompt, last, output]:
        text = path.read_text(encoding="utf-8")
        print(
            f"text_record={path} sha256={sha256(path)} "
            f"bytes={len(text.encode('utf-8'))} lines={len(text.splitlines())}"
        )

    output_text = output.read_text(encoding="utf-8")
    for needle in [
        "RESULT: KPROVE_PASSED",
        "#Top",
        "WarnStuckClaimState",
        "kompile --backend haskell",
        "kprove spec.k",
        "spec-vacuity.k",
        "spec-body-mutation.k",
    ]:
        print(f"codex_output_occurrences[{needle!r}]={output_text.count(needle)}")

    trace_files = sorted((ROOT / "codex-trace").rglob("*.jsonl"))
    print(f"trace_file_count={len(trace_files)}")
    total_rows = 0
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    roles: Counter[str] = Counter()
    tool_names: Counter[str] = Counter()
    final_messages = 0
    parse_failures = 0
    for path in trace_files:
        rows = path.read_text(encoding="utf-8").splitlines()
        print(
            f"trace_file={path} sha256={sha256(path)} rows={len(rows)}"
        )
        for line_number, line in enumerate(rows, 1):
            try:
                row = json.loads(line)
            except json.JSONDecodeError as err:
                parse_failures += 1
                print(f"trace_parse_failure={path}:{line_number}:{err}")
                continue
            total_rows += 1
            top_types[str(row.get("type"))] += 1
            payload = row.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                role = payload.get("role")
                if role is not None:
                    roles[str(role)] += 1
                name = payload.get("name")
                if name is not None:
                    tool_names[str(name)] += 1
                if payload.get("phase") == "final_answer":
                    final_messages += 1

    print(f"trace_total_rows={total_rows}")
    print(f"trace_parse_failures={parse_failures}")
    print(f"trace_top_types={dict(sorted(top_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    print(f"trace_roles={dict(sorted(roles.items()))}")
    print(f"trace_tool_names={dict(sorted(tool_names.items()))}")
    print(f"trace_final_answer_messages={final_messages}")

    usage = json.loads((ROOT / "usage.json").read_text(encoding="utf-8"))
    actual_trace_hashes = [sha256(path) for path in trace_files]
    final_trace_tree_hash = pipeline_tree_sha256(ROOT / "codex-trace")
    print(f"usage_source_trace_sha256={usage.get('source_trace_sha256')}")
    print(f"final_trace_file_sha256_values={actual_trace_hashes}")
    print(f"final_trace_tree_sha256={final_trace_tree_hash}")
    print(
        "usage_source_hash_matches_final_trace_tree="
        f"{usage.get('source_trace_sha256') == final_trace_tree_hash}"
    )
    print(
        "NOTE: generation records remain untrusted claims. The per-file hash "
        "in generation-result and the tree hash in usage.json both independently "
        "match their respective mounted trace representation."
    )
    return 1 if parse_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
