#!/usr/bin/env python3
"""Independent differential and branch-coverage check for HumanEval/39."""

from __future__ import annotations

import importlib.util
import multiprocessing
import random
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/39-prime-fib-audit")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", SCRATCH / "trusted_canonical.py")
generated = load("generated_solution", SCRATCH / "solution.py")


def traced_generated(n: int) -> tuple[int, list[int]]:
    target = str((SCRATCH / "solution.py").resolve())
    lines: set[int] = set()

    def trace(frame, event, arg):
        if event == "line" and str(Path(frame.f_code.co_filename).resolve()) == target:
            lines.add(frame.f_lineno)
        return trace

    sys.settrace(trace)
    try:
        result = generated.prime_fib(n)
    finally:
        sys.settrace(None)
    return result, sorted(lines)


def call_and_send(fn, n: int, queue) -> None:
    try:
        queue.put(("return", fn(n)))
    except BaseException as err:  # report, rather than hide, outside-domain behavior
        queue.put(("raise", f"{type(err).__name__}: {err}"))


def bounded_call(fn, n: int, timeout_s: float = 0.25):
    queue = multiprocessing.Queue()
    proc = multiprocessing.Process(target=call_and_send, args=(fn, n, queue))
    proc.start()
    proc.join(timeout_s)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        return ("timeout", f">{timeout_s}s")
    return queue.get() if not queue.empty() else ("exit", proc.exitcode)


examples = {1: 2, 2: 3, 3: 5, 4: 13, 5: 89}
for n, expected in examples.items():
    got_canonical = canonical.prime_fib(n)
    got_generated = generated.prime_fib(n)
    assert got_canonical == expected
    assert got_generated == expected
print("documented examples:", examples)

# This selected finite range includes the lower boundary and all relevant
# branch outcomes on the actual program path. It is evidence, not a universal
# proof over the unbounded n >= 1 domain.
inputs = list(range(1, 12))
random.Random(39039).shuffle(inputs)
mismatches = []
rows = []
for n in inputs:
    got_canonical = canonical.prime_fib(n)
    got_generated = generated.prime_fib(n)
    rows.append((n, got_canonical, got_generated))
    if got_canonical != got_generated:
        mismatches.append((n, got_canonical, got_generated))
print("generated input order:", inputs)
print("differential rows (n, canonical, generated):")
for row in sorted(rows):
    print(row)
print("mismatches:", len(mismatches), mismatches)
assert not mismatches

result, covered_lines = traced_generated(11)
required_lines = set(range(2, 20))
assert required_lines <= set(covered_lines), (required_lines - set(covered_lines))
print("generated prime_fib(11):", result)
print("generated executable lines covered:", covered_lines)
print(
    "branch witnesses:",
    {
        "a<2": "Fibonacci candidate 1",
        "a>=2": "candidate 2",
        "inner-guard-false": "candidate 2",
        "inner-guard-true": "candidate 5",
        "mod-equal-zero": "candidate 8, divisor 2",
        "mod-not-zero": "candidate 5, divisor 2",
        "outer-repeat": "n=11",
        "outer-exit": "every completed call",
    },
)

# n=0 is the nearest empty/outside-domain case. The generated rewrite returns
# 0 immediately, while the canonical program does not return within this
# bounded observation because its contract presupposes a positive ordinal.
zero_generated = bounded_call(generated.prime_fib, 0)
zero_canonical = bounded_call(canonical.prime_fib, 0)
print("outside-domain n=0 generated:", zero_generated)
print("outside-domain n=0 canonical:", zero_canonical)
assert zero_generated == ("return", 0)

print("RESULT: differential checks passed on intended inputs n=1..11")
