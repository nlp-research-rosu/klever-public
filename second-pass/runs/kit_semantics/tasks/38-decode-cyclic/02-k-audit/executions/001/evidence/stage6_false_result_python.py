import importlib.util


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical", "/reference/canonical.py")
candidate = load("candidate", "/candidate/solution.py")
source = "abcd"
false_destination = "cabx"
canonical_result = canonical.decode_cyclic(source)
candidate_result = candidate.decode_cyclic(source)
print(f"input={source!r}")
print(f"canonical_result={canonical_result!r}")
print(f"candidate_result={candidate_result!r}")
print(f"false_destination={false_destination!r}")
assert canonical_result == candidate_result == "cabd"
assert candidate_result != false_destination
