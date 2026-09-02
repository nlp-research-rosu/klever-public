#!/usr/bin/env python3
import importlib.util


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.how_many_times


canonical = load("canonical_witness", "/reference/canonical.py")
candidate = load("candidate_witness", "/tmp/audit-work/src/solution.py")


def direct_count(string, substring):
    return sum(
        string[index : index + len(substring)] == substring
        for index in range(len(string) - len(substring) + 1)
    )


for string, substring in [
    ("aaaa", "aa"),
    ("", ""),
    ("abc", "z"),
]:
    print(
        repr((string, substring)),
        f"direct_count={direct_count(string, substring)}",
        f"canonical={canonical(string, substring)}",
        f"candidate={candidate(string, substring)}",
    )
