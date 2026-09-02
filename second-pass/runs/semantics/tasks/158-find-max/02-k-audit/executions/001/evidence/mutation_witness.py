#!/usr/bin/env python3
import importlib.util


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_max


canonical = load("/reference/canonical.py", "mutation_canonical")
candidate = load("/tmp/audit-work/reconstruction/solution.py", "mutation_candidate")
witness = ["a"]
print(
    {
        "input": witness,
        "canonical": canonical(list(witness)),
        "candidate": candidate(list(witness)),
        "mutated_required_result": "",
    }
)
