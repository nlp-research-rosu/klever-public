#!/usr/bin/env python3
import importlib.util
import json


def load(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


def valid_date_10(value):
    if len(value) != 10 or value[2] != "-" or value[5] != "-":
        return False
    if not all(value[i] in "0123456789" for i in (0, 1, 3, 4, 6, 7, 8, 9)):
        return False
    month = int(value[:2])
    day = int(value[3:5])
    if month < 1 or month > 12 or day < 1:
        return False
    if month == 2:
        return day <= 29
    if month in (4, 6, 9, 11):
        return day <= 30
    return day <= 31


canonical = load("audit_canonical", "/reference/canonical.py")
generated = load("audit_generated", "/tmp/audit-work/124-valid-date/solution.py")

for value in ("", "03-11-2000", "03-31-2000", "02-30-2000", "04-31-2000"):
    print(json.dumps({
        "input": value,
        "invalid_length_precondition": len(value) != 10,
        "length_ten_precondition": len(value) == 10,
        "formal_result": False if len(value) != 10 else valid_date_10(value),
        "generated": generated(value),
        "canonical": canonical(value),
    }, sort_keys=True))
