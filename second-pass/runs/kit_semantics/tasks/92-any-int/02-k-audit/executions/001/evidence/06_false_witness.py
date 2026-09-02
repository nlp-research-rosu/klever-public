from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load(name, path):
    spec = spec_from_file_location(name, Path(path))
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.any_int


canonical = load("canonical_false_witness", "/reference/canonical.py")
candidate = load(
    "candidate_false_witness",
    "/tmp/audit-work/92-any-int-audit/solution.py",
)
args = (5, 2, 7)
print(f"args={args} canonical={canonical(*args)!r} candidate={candidate(*args)!r}")
assert canonical(*args) is True
assert candidate(*args) is True
