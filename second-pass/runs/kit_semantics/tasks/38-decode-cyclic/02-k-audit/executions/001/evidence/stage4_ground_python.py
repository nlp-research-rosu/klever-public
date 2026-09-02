import importlib.util


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical", "/reference/canonical.py")
candidate = load("candidate", "/candidate/solution.py")
source = "bca"
print(f"input={source!r}")
print(f"canonical={canonical.decode_cyclic(source)!r}")
print(f"candidate={candidate.decode_cyclic(source)!r}")
assert canonical.decode_cyclic(source) == "abc"
assert candidate.decode_cyclic(source) == "abc"
