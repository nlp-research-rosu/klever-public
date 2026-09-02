#!/usr/bin/env python3
"""Compare fresh krun execution with both Python implementations."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import re
import subprocess
from pathlib import Path


RETURN_RE = re.compile(
    r"returned\s*\(\s*tupleVal\s*\(\s*"
    r"strVal\s*\(\s*(\"(?:\\.|[^\"\\])*\")\s*\)\s*,\s*"
    r"boolVal\s*\(\s*(true|false)\s*\)\s*\)\s*\)",
    re.DOTALL,
)


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.reverse_delete


def parse_k_string(token: str):
    raw = ast.literal_eval("b" + token)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--krun", required=True)
    parser.add_argument("--program", type=Path, required=True)
    parser.add_argument("--definition", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "concrete_trusted_canonical")
    candidate = load_entry(args.candidate, "concrete_scratch_candidate")
    cases = [
        {"category": "example", "s": "abcde", "c": "ae"},
        {"category": "example", "s": "abcdef", "c": "b"},
        {"category": "example", "s": "abcdedcba", "c": "ab"},
        {"category": "zero-iteration", "s": "", "c": ""},
        {"category": "empty-delete-set", "s": "abba", "c": ""},
        {"category": "all-deleted", "s": "aaaa", "c": "a"},
        {"category": "both-branches", "s": "abab", "c": "a"},
        {"category": "repeated-membership", "s": "mississippi", "c": "isp"},
        {"category": "unicode-scalar", "s": "🙂a🙂", "c": ""},
        {"category": "unicode-delete", "s": "🙂a🙂", "c": "🙂"},
        {"category": "unicode-shared-utf8-prefix", "s": "🙃", "c": "🙂"},
        {"category": "combining-codepoint", "s": "e\u0301x\u0301e", "c": "\u0301"},
    ]
    args.inputs_out.write_text(
        json.dumps(cases, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = []
    for index, case in enumerate(cases):
        command = [
            args.krun,
            str(args.program),
            "--definition",
            str(args.definition),
            f"-cS={json.dumps(case['s'], ensure_ascii=False)}",
            f"-cC={json.dumps(case['c'], ensure_ascii=False)}",
        ]
        run = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=60,
        )
        match = RETURN_RE.search(run.stdout)
        parsed = None
        if match:
            parsed = (parse_k_string(match.group(1)), match.group(2) == "true")
        canonical_result = canonical(case["s"], case["c"])
        candidate_result = candidate(case["s"], case["c"])
        ok = (
            run.returncode == 0
            and parsed == canonical_result
            and parsed == candidate_result
        )
        print(
            json.dumps(
                {
                    "index": index,
                    **case,
                    "command": command,
                    "krun_exit": run.returncode,
                    "krun_result": repr(parsed),
                    "canonical": repr(canonical_result),
                    "candidate": repr(candidate_result),
                    "match": ok,
                    "stderr": run.stderr[-1000:],
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )
        if not ok:
            failures.append(index)
    print(f"total_cases={len(cases)}")
    print(f"mismatch_count={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
