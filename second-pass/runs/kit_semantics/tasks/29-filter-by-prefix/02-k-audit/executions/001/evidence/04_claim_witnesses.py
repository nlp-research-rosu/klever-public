#!/usr/bin/env python3
"""Concrete substitutions for both entry claims and their mathematical summary."""

from pathlib import Path
import importlib.util


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_prefix


canonical = load("/reference/canonical.py", "canonical_witness")
candidate = load("/tmp/audit-work/work/solution.py", "candidate_witness")


def codes(value: str) -> list[int]:
    return [ord(character) for character in value]


def formal_summary(acc: list[str], remaining: list[str], prefix: str) -> list[str]:
    return acc + [value for value in remaining if codes(value)[: len(codes(prefix))] == codes(prefix)]


program_input = ["abc", "bcd", "", "array"]
program_prefix = "a"
program_summary = formal_summary([], program_input, program_prefix)

loop_acc = ["seed"]
loop_input = ["abc", "bcd"]
loop_prefix = "a"
loop_summary = formal_summary(loop_acc, loop_input, loop_prefix)

print("COMMAND: python3 /audit-output/evidence/04_claim_witnesses.py")
print("PROGRAM_PRECONDITION allStrings(INPUT)=true")
print("PROGRAM_INPUT", repr(program_input), "PREFIX", repr(program_prefix))
print("PROGRAM_CODES", repr([codes(item) for item in program_input]), "PREFIX_CODES", repr(codes(program_prefix)))
print("PROGRAM_FORMAL_SUMMARY", repr(program_summary))
print("PROGRAM_CANONICAL", repr(canonical(program_input, program_prefix)))
print("PROGRAM_GENERATED", repr(candidate(program_input, program_prefix)))
print("LOOP_PRECONDITION allStrings(INPUT)=true")
print("LOOP_STATE", "ACC=" + repr(loop_acc), "INPUT=" + repr(loop_input), "PREFIX=" + repr(loop_prefix))
print("LOOP_FORMAL_SUMMARY", repr(loop_summary))

assert program_summary == canonical(program_input, program_prefix)
assert program_summary == candidate(program_input, program_prefix)
assert loop_summary == ["seed", "abc"]
print("WITNESS_COMPARISON=PASS")
