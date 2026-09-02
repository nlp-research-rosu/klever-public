#!/usr/bin/env python3
"""Ground witnesses for every formal claim precondition and result expression."""

from __future__ import annotations

import importlib.util


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored


canonical = load("canonical", "/reference/canonical.py")
generated = load("generated", "/tmp/audit-work/source/solution.py")


def bored(codes: tuple[int, ...], count: int, state: int) -> int:
    for code in codes:
        if code in (46, 63, 33):
            state = 0
        elif state == 0:
            if code == 32 or 9 <= code <= 13:
                state = 0
            elif code == 73:
                state = 1
            else:
                state = 2
        elif state == 1:
            if code == 32:
                count += 1
            state = 2
    return count


loop_witnesses = [
    {
        "claim": "loop-state-0",
        "state": 0,
        "cs": (73, 32),
        "n": 0,
        "input_codes": (73, 32),
        "ch": "",
        "code": 0,
        "realizing_input": "I ",
    },
    {
        "claim": "loop-state-1",
        "state": 1,
        "cs": (32,),
        "n": 0,
        "input_codes": (73, 32),
        "ch": "I",
        "code": 73,
        "realizing_input": "I ",
    },
    {
        "claim": "loop-state-2",
        "state": 2,
        "cs": (46, 73, 32),
        "n": 0,
        "input_codes": (65, 46, 73, 32),
        "ch": "A",
        "code": 65,
        "realizing_input": "A.I ",
    },
]

print("LOOP CLAIM WITNESSES")
for item in loop_witnesses:
    result = bored(item["cs"], item["n"], item["state"])
    value = item["realizing_input"]
    print(
        f"{item['claim']}: GLOBAL=.Map (so ord not-in GLOBAL), "
        f"CS={item['cs']}, N={item['n']}, state={item['state']}, "
        f"INPUT={item['input_codes']}, ch={item['ch']!r}, code={item['code']}; "
        f"summary_result={result}; realizing_input={value!r}; "
        f"canonical={canonical(value)} generated={generated(value)}"
    )

entry_witnesses = [
    ("prompt-example-0", "Hello world", 0),
    (
        "prompt-example-1",
        "The sky is blue. The sun is shining. I love this weather",
        1,
    ),
]

print("\nGROUND ENTRY CLAIM WITNESSES")
for claim, value, claimed in entry_witnesses:
    print(
        f"{claim}: input={value!r} claimed={claimed} "
        f"canonical={canonical(value)} generated={generated(value)}"
    )
