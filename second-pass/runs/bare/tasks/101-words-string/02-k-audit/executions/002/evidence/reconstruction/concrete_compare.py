#!/usr/bin/env python3
"""Compare freshly rebuilt K execution with two Python implementations."""

from __future__ import annotations

import importlib.util
import json
import shlex
import subprocess
from pathlib import Path


PROGRAM = Path("/tmp/audit-work/candidate/solution.mpy")
DEFINITION = Path("/tmp/audit-work/build/concrete-kompiled")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_string


def prompt_oracle(text: str) -> list[str]:
    return [word for word in text.replace(",", " ").split(" ") if word]


def collect_list_items(term: object) -> list[str]:
    found: list[str] = []
    if isinstance(term, dict):
        label = term.get("label")
        if (
            term.get("node") == "KApply"
            and isinstance(label, dict)
            and label.get("name") == "ListItem"
        ):
            token = term["args"][0]["token"]
            found.append(json.loads(token))
        else:
            for value in term.values():
                found.extend(collect_list_items(value))
    elif isinstance(term, list):
        for value in term:
            found.extend(collect_list_items(value))
    return found


def main() -> None:
    candidate = load_entry(
        Path("/tmp/audit-work/candidate/solution.py"), "candidate_solution"
    )
    canonical = load_entry(
        Path("/tmp/audit-work/reference/canonical.py"), "canonical_solution"
    )
    cases = [
        "",
        "alpha",
        ",",
        " ",
        ",,,",
        "a,b",
        "a b",
        "a, b",
        " a",
        "a ",
        "  alpha,,beta   gamma, ",
        "Hi, my name is John",
        "One, two, three, four, five, six",
    ]
    for text in cases:
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cINPUT={json.dumps(text)}",
            "--output",
            "json",
        ]
        print("INNER_COMMAND:", shlex.join(command))
        result = subprocess.run(
            command,
            cwd="/tmp/audit-work/candidate",
            check=False,
            text=True,
            capture_output=True,
        )
        print(f"INNER_EXIT_STATUS: {result.returncode}")
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            raise RuntimeError("krun failed")
        k_value = collect_list_items(json.loads(result.stdout))
        candidate_value = candidate(text)
        canonical_value = canonical(text)
        oracle_value = prompt_oracle(text)
        print(
            f"INPUT={text!r} K={k_value!r} candidate={candidate_value!r} "
            f"canonical={canonical_value!r} oracle={oracle_value!r}"
        )
        assert k_value == candidate_value == canonical_value == oracle_value
    print(f"CONCRETE_CASES={len(cases)} MISMATCHES=0")
    print("CONCRETE_COMPARISON=PASS")


if __name__ == "__main__":
    main()
