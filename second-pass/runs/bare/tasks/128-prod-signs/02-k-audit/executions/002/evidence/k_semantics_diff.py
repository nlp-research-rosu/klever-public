#!/usr/bin/env python3
"""Compare freshly rebuilt K execution with the trusted Python implementation."""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/fresh")


def load_canonical():
    path = Path("/tmp/audit-work/reference/canonical.py")
    spec = importlib.util.spec_from_file_location("trusted_canonical_for_k", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.prod_signs


def find_cell(term, label_name: str):
    if isinstance(term, dict):
        label = term.get("label")
        if isinstance(label, dict) and label.get("name") == label_name:
            return term
        for value in term.values():
            found = find_cell(value, label_name)
            if found is not None:
                return found
    elif isinstance(term, list):
        for value in term:
            found = find_cell(value, label_name)
            if found is not None:
                return found
    return None


def decode_result(kast):
    cell = find_cell(kast["term"], "<result>")
    assert cell is not None and len(cell["args"]) == 1
    wrapper = cell["args"][0]
    label = wrapper["label"]["name"]
    assert label.startswith("result("), label
    value = wrapper["args"][0]
    if value.get("node") == "KToken":
        assert value["sort"]["name"] == "Int"
        return int(value["token"])
    value_label = value["label"]["name"]
    if value_label.startswith("none_") or value_label == "none":
        return None
    raise AssertionError(f"unknown result term: {value}")


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/k_semantics_diff.py")
    print(
        "KRUN TEMPLATE: krun solution.mpy --definition semantics-kompiled "
        "-cARGS=input(...) --output json"
    )
    canonical = load_canonical()
    cases = [
        [],
        [-1],
        [0],
        [1],
        [1, 2, 2, -4],
        [0, 1],
        [-1, -2],
        [-1, -2, -3],
        [0, -7],
        [-7, 0],
        [10**30, -(10**35), 1],
        [-5, 4, 0, -3, 2],
    ]
    mismatches = []
    for values in cases:
        args = "input(" + ",".join(str(value) for value in values) + ")"
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            "semantics-kompiled",
            f"-cARGS={args}",
            "--output",
            "json",
        ]
        completed = subprocess.run(
            command,
            cwd=WORK,
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, (
            values,
            completed.returncode,
            completed.stdout,
            completed.stderr,
        )
        observed = decode_result(json.loads(completed.stdout))
        expected = canonical(list(values))
        print(
            f"input={values!r} python={expected!r} k={observed!r} "
            f"krun_exit={completed.returncode}"
        )
        if observed != expected:
            mismatches.append((values, expected, observed))
    print(f"cases={len(cases)} mismatches={len(mismatches)}")
    if mismatches:
        print(f"MISMATCHES={mismatches!r}")
        raise SystemExit(1)
    print("STATUS: PASS")


if __name__ == "__main__":
    main()
