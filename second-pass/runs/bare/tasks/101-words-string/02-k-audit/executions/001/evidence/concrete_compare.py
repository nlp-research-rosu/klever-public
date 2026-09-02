#!/usr/bin/env python3
"""Run the rebuilt generated K semantics and compare it with two Python functions."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import subprocess
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_string


def label(node: dict) -> str:
    return node.get("label", {}).get("name", "")


def find_label(node, wanted: str):
    if isinstance(node, dict):
        if label(node) == wanted:
            return node
        for value in node.values():
            found = find_label(value, wanted)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = find_label(value, wanted)
            if found is not None:
                return found
    return None


def decode_list(node: dict) -> list[str]:
    node_label = label(node)
    if node_label == "ListItem":
        token = node["args"][0]["token"]
        # K renders non-ASCII bytes with \xHH escapes, which are valid Python
        # string-literal syntax but are not valid JSON escapes.
        return [ast.literal_eval(token)]
    if node_label == "_List_":
        return decode_list(node["args"][0]) + decode_list(node["args"][1])
    if node_label.startswith(".List"):
        return []
    raise ValueError(f"unexpected List node {node_label!r}")


def extract_result(kast: dict) -> list[str]:
    k_cell = find_label(kast["term"], "<k>")
    if k_cell is None:
        raise ValueError("no <k> cell")
    list_value = find_label(k_cell, "ListVal(_)_SEMANTIC_PyVal_List")
    if list_value is None:
        raise ValueError("no ListVal in <k> cell")
    return decode_list(list_value["args"][0])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--definition", required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical_for_k")
    candidate = load_entry(args.candidate, "scratch_candidate_for_k")
    cases = [
        "Hi, my name is John",
        "One, two, three, four, five, six",
        "",
        "a",
        " ",
        ",",
        ",,",
        "a b",
        "a,b",
        " a",
        "a ",
        ",a",
        "a,",
        "a,,b",
        "a  b",
        "a, ,b",
        "  alpha,,beta   gamma, ",
        "word-with-punctuation,naïve café",
    ]
    args.inputs_out.write_text(
        "".join(json.dumps({"index": i, "input": s}, ensure_ascii=False) + "\n"
                for i, s in enumerate(cases)),
        encoding="utf-8",
    )

    mismatches = []
    records = []
    for index, value in enumerate(cases):
        input_token = json.dumps(value, ensure_ascii=False)
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            args.definition,
            f"-cINPUT={input_token}",
            "--output",
            "json",
        ]
        completed = subprocess.run(
            command,
            cwd=args.workdir,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        k_result = None
        if completed.returncode == 0:
            k_result = extract_result(json.loads(completed.stdout))
        canonical_result = canonical(value)
        candidate_result = candidate(value)
        matches = (
            completed.returncode == 0
            and k_result == canonical_result
            and k_result == candidate_result
        )
        record = {
            "index": index,
            "input": value,
            "command": command,
            "krun_exit": completed.returncode,
            "k": k_result,
            "canonical": canonical_result,
            "candidate": candidate_result,
            "matches": matches,
            "stderr": completed.stderr[-1000:],
        }
        records.append(record)
        if not matches:
            mismatches.append(record)

    print(
        json.dumps(
            {
                "case_count": len(cases),
                "mismatch_count": len(mismatches),
                "cases": records,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
