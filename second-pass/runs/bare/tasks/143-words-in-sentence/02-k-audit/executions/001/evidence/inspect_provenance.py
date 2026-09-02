#!/usr/bin/env python3
"""Read candidate metadata and trace strictly as inert, untrusted data."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
TRACE = CANDIDATE / "codex-trace/2026/07/22/rollout-2026-07-22T07-29-29-019f89cd-6e6f-7273-9db7-85ed4e7e4b51.jsonl"
REQUIRED = [
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
    "prove.sh",
    str(TRACE.relative_to(CANDIDATE)),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    print(f"generated_semantics_reference_tree_exists={bool((REFERENCE / 'reference-semantics').exists())}")
    print("required_artifacts:")
    for relative in REQUIRED:
        path = CANDIDATE / relative
        info = path.lstat() if path.exists() or path.is_symlink() else None
        print(
            json.dumps(
                {
                    "path": str(path),
                    "exists": info is not None,
                    "regular": path.is_file() if info is not None else False,
                    "symlink": path.is_symlink(),
                    "bytes": info.st_size if info is not None else None,
                    "sha256": sha256(path) if info is not None and path.is_file() and not path.is_symlink() else None,
                },
                sort_keys=True,
            )
        )

    symlinks = []
    for root, dirs, files in os.walk(CANDIDATE, followlinks=False):
        for name in dirs + files:
            path = Path(root) / name
            if path.is_symlink():
                symlinks.append(str(path))
    print(f"recursive_symlinks={json.dumps(sorted(symlinks))}")

    print(
        "prompt_byte_identical="
        f"{(CANDIDATE / 'prompt.py').read_bytes() == (REFERENCE / 'prompt.py').read_bytes()}"
    )
    print(
        "translator_byte_identical="
        f"{(CANDIDATE / 'py2mpy.py').read_bytes() == (REFERENCE / 'py2mpy.py').read_bytes()}"
    )

    print("top_level_entries:")
    for path in sorted(CANDIDATE.iterdir(), key=lambda item: item.name):
        kind = "symlink" if path.is_symlink() else "dir" if path.is_dir() else "file" if path.is_file() else "other"
        print(f"{kind}\t{path.name}")

    for metadata_name in ("run-input.json", "metrics.json"):
        data = json.loads((CANDIDATE / metadata_name).read_text(encoding="utf-8"))
        print(f"{metadata_name}={json.dumps(data, sort_keys=True)}")

    outer_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    invalid_lines = 0
    final_messages: list[str] = []
    with TRACE.open("r", encoding="utf-8") as stream:
        for line in stream:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                invalid_lines += 1
                continue
            outer_types[str(item.get("type"))] += 1
            payload = item.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                if payload.get("type") == "task_complete":
                    final_messages.append(str(payload.get("last_agent_message", "")))
    print(f"trace_outer_types={json.dumps(dict(sorted(outer_types.items())), sort_keys=True)}")
    print(f"trace_payload_types={json.dumps(dict(sorted(payload_types.items())), sort_keys=True)}")
    print(f"trace_invalid_json_lines={invalid_lines}")
    for index, message in enumerate(final_messages):
        print(f"trace_task_complete_{index}={json.dumps(message)}")

    codex_last = (CANDIDATE / "codex-last.txt").read_text(encoding="utf-8")
    output = (CANDIDATE / "codex-output.log").read_text(encoding="utf-8", errors="replace")
    print(f"codex_last={json.dumps(codex_last)}")
    print(f"codex_output_bytes={len(output.encode('utf-8'))}")
    for needle in ("#Top", "WarnStuckClaimState", "2,000 randomized", "KPROVE_PASSED"):
        print(f"codex_output_count[{needle!r}]={output.count(needle)}")

    claimed_test_artifacts = [
        p.name
        for p in CANDIDATE.iterdir()
        if p.is_file() and any(token in p.name.lower() for token in ("random", "differential", "test"))
    ]
    print(f"candidate_claimed_test_artifacts={json.dumps(sorted(claimed_test_artifacts))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
