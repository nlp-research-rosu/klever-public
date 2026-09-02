#!/usr/bin/env python3
import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


def load_function(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


canonical = load_function("trusted_canonical", "/tmp/audit-work/trusted/canonical.py")
generated = load_function("generated_solution", "/tmp/audit-work/work/solution.py")


def prompt_contract(value):
    if not value:
        return False
    keys = value.keys()
    return all(isinstance(key, str) and key.islower() for key in keys) or all(
        isinstance(key, str) and key.isupper() for key in keys
    )

documented = [
    {"a": "apple", "b": "banana"},
    {"a": "apple", "A": "banana", "B": "banana"},
    {"a": "apple", 8: "banana"},
    {"Name": "John", "Age": "36", "City": "Houston"},
    {"STATE": "NC", "ZIP": "12345"},
]
boundaries = [
    {},
    {"a": 0},
    {"A": 0},
    {"Aa": 0},
    {"123": 0},
    {"!": 0},
    {"a1": 0},
    {"A1": 0},
    {"é": 0},
    {"É": 0},
    {0: 0},
    {None: 0},
    {False: 0},
    {("a",): 0},
    {"a": 0, "b": 1, "z9": 2},
    {"A": 0, "B": 1, "Z9": 2},
    {"a": 0, "A": 1},
    {"a": 0, 9: 1},
    {9: 0, "A": 1},
]
pool = ["a", "b2", "A", "B2", "Aa", "123", "", "!", "é", "É", 0, 1, None, False, ("x",)]
exhaustive = []
for length in range(0, 5):
    for keys in itertools.combinations(pool, length):
        exhaustive.append(dict((key, index) for index, key in enumerate(keys)))

rng = random.Random(950026)
randomized = []
ascii_alphabet = "abAB09_-"
for index in range(2000):
    keys = []
    for _ in range(rng.randrange(0, 9)):
        key_kind = rng.randrange(5)
        if key_kind == 0:
            key = rng.randrange(-5, 6)
        elif key_kind == 1:
            key = None
        elif key_kind == 2:
            key = tuple(rng.randrange(3) for _ in range(rng.randrange(3)))
        else:
            key = "".join(
                rng.choice(ascii_alphabet) for _ in range(rng.randrange(0, 7))
            )
        keys.append(key)
    randomized.append(dict((key, index) for key in keys))

groups = [
    ("documented", documented),
    ("boundaries", boundaries),
    ("exhaustive_combinations", exhaustive),
    ("deterministic_random", randomized),
]
records = []
canonical_mismatches = []
contract_mismatches = []
for group_name, cases in groups:
    for index, case in enumerate(cases):
        expected = canonical(case)
        actual = generated(case)
        contract = prompt_contract(case)
        record = {
            "group": group_name,
            "index": index,
            "dict_repr": repr(case),
            "canonical": expected,
            "prompt_contract": contract,
            "generated": actual,
        }
        records.append(record)
        if type(expected) is not type(actual) or expected != actual:
            canonical_mismatches.append(record)
        if type(contract) is not type(actual) or contract != actual:
            contract_mismatches.append(record)

output_path = Path("/audit-output/evidence/differential_cases.json")
output_path.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n")
digest = hashlib.sha256(output_path.read_bytes()).hexdigest()
print("ORACLE: trusted /reference/canonical.py copied to scratch and imported independently")
print("SUBJECT: candidate solution.py copied to scratch and imported independently")
print("DOCUMENTED_CASES:", len(documented))
print("BOUNDARY_CASES:", len(boundaries))
print("EXHAUSTIVE_SCOPE: all key subsets of sizes 0..4 from", repr(pool))
print("EXHAUSTIVE_CASES:", len(exhaustive))
print("RANDOM_SCOPE: seed=950026, 2000 dictionaries, 0..8 generated keys")
print("RANDOM_CASES:", len(randomized))
print("TOTAL_CASES:", len(records))
print("CASES_SHA256:", digest)
print("CANONICAL_MISMATCHES:", len(canonical_mismatches))
print("PROMPT_CONTRACT_MISMATCHES:", len(contract_mismatches))
if canonical_mismatches:
    print("FIRST_CANONICAL_MISMATCHES:")
    print(json.dumps(canonical_mismatches[:20], indent=2, sort_keys=True))
if contract_mismatches:
    print("FIRST_PROMPT_CONTRACT_MISMATCHES:")
    print(json.dumps(contract_mismatches[:20], indent=2, sort_keys=True))
if canonical_mismatches or contract_mismatches:
    sys.exit(1)
