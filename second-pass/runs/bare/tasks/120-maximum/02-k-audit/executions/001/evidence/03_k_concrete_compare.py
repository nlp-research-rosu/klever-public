#!/usr/bin/env python3
"""Execute the freshly rebuilt generated K semantics and compare with Python."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def k_list(values):
    if not values:
        return ".List"
    return " ".join(f"ListItem({value})" for value in values)


def k_args(arr, k):
    return f"ListItem(listVal({k_list(arr)})) ListItem(intVal({k}))"


def parse_out(pretty_output):
    match = re.search(r"<out>\s*(.*?)\s*</out>", pretty_output, flags=re.DOTALL)
    if match is None:
        raise ValueError("missing <out> cell")
    content = match.group(1)
    if "listVal" not in content:
        raise ValueError(f"unexpected <out>: {content}")
    return [int(value) for value in re.findall(r"ListItem\s*\(\s*(-?\d+)\s*\)", content)]


def result_summary(values):
    if len(values) <= 20:
        return values
    return {
        "length": len(values),
        "first_5": values[:5],
        "last_5": values[-5:],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--definition", type=Path, required=True)
    parser.add_argument("--program", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--results-json", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_module(args.canonical, "trusted_canonical_for_k_compare")
    generated = load_module(args.generated, "generated_python_for_k_compare")

    cases = [
        ("example-1", [-3, -4, 5], 3),
        ("example-2", [4, -4, 4], 2),
        ("example-3", [-3, 2, 1, 2, -1, -2, 1], 1),
        ("empty-k0-outside-prompt-length-domain", [], 0),
        ("single-min-k0", [-1000], 0),
        ("single-min-k1", [-1000], 1),
        ("value-extremes-k1", [-1000, 1000], 1),
        ("value-extremes-kn", [-1000, 1000], 2),
        ("duplicates", [4, 4, -4, 4], 3),
        ("representative-length-100-k0", [0] * 100, 0),
        ("representative-length-100-kn", [0] * 100, 100),
    ]

    records = []
    mismatch_count = 0
    for label, arr, k in cases:
        argv = [
            "krun",
            str(args.program),
            "--definition",
            str(args.definition),
            f"-cARGS={k_args(arr, k)}",
        ]
        completed = subprocess.run(argv, text=True, capture_output=True, check=False)
        parsed = None
        parse_error = None
        if completed.returncode == 0:
            try:
                parsed = parse_out(completed.stdout)
            except ValueError as err:
                parse_error = str(err)

        canonical_arg = list(arr)
        generated_arg = list(arr)
        canonical_result = canonical.maximum(canonical_arg, k)
        generated_result = generated.maximum(generated_arg, k)
        equal = (
            completed.returncode == 0
            and parse_error is None
            and parsed == canonical_result
            and parsed == generated_result
        )
        mismatch_count += int(not equal)
        raw_output = completed.stdout + completed.stderr
        records.append(
            {
                "label": label,
                "arr": arr,
                "k": k,
                "krun_argv": argv,
                "krun_exit_status": completed.returncode,
                "raw_output_sha256": hashlib.sha256(raw_output.encode()).hexdigest(),
                "raw_output_bytes": len(raw_output.encode()),
                "parse_error": parse_error,
                "k_result": parsed,
                "trusted_canonical_result": canonical_result,
                "generated_python_result": generated_result,
                "all_results_equal": equal,
            }
        )
        print(
            json.dumps(
                {
                    "label": label,
                    "arr_length": len(arr),
                    "k": k,
                    "krun_exit_status": completed.returncode,
                    "raw_output_sha256": records[-1]["raw_output_sha256"],
                    "k_result": result_summary(parsed) if parsed is not None else None,
                    "canonical_result": result_summary(canonical_result),
                    "generated_result": result_summary(generated_result),
                    "all_results_equal": equal,
                    "parse_error": parse_error,
                },
                sort_keys=True,
            )
        )
        if completed.returncode != 0:
            print(completed.stderr[-2000:])

    args.results_json.write_text(json.dumps(records, indent=2, sort_keys=True))
    print(f"total_cases={len(records)}")
    print(f"mismatch_count={mismatch_count}")
    print(f"results_json={args.results_json}")
    return 0 if mismatch_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
