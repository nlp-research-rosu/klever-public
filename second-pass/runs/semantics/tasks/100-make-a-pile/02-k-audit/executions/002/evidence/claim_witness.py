#!/usr/bin/env python3
"""Ground witnesses for both entry-claim preconditions and their summaries."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.make_a_pile


canonical = load_entry("trusted_canonical_claim_witness", Path("/reference/canonical.py"))
candidate = load_entry("candidate_claim_witness", Path("/candidate/solution.py"))


def pile(n: int, i: int) -> list[int]:
    if i >= n:
        return []
    return [n + 2 * i] + pile(n, i + 1)


# Prefix claim witness. This is the concrete initial configuration prescribed
# by the fixed semantics, with N=3. Its precondition N>0 is satisfiable.
prefix_n = 3
prefix_initial_state = {
    "k": "#loadAll(pileModule) ~> Call(Name(\"make_a_pile\"), Int(3))",
    "env": 0,
    "scopes": {
        -1: "builtinsScope",
        0: "scope(.Map,parent(-1))",
    },
    "scopeLoc": 1,
    "heap": {},
    "heapLoc": 0,
    "stack": [],
    "ret": "noRet",
    "exc": "NoExc",
}
assert prefix_n > 0

# Loop claim witness reached by the prefix: N=3, I=0, VS empty. It satisfies
# N>0, 0<=I<=N. The loop summary is VS ++ pile(N,I).
loop_n, loop_i, loop_vs = 3, 0, []
assert loop_n > 0 and 0 <= loop_i <= loop_n
loop_summary = loop_vs + pile(loop_n, loop_i)

# An interior invariant witness shows the loop claim also has a satisfiable
# non-initial state: two levels have already been appended for N=4.
interior_n, interior_i, interior_vs = 4, 2, [4, 6]
assert interior_n > 0 and 0 <= interior_i <= interior_n
interior_summary = interior_vs + pile(interior_n, interior_i)

assert loop_summary == canonical(prefix_n) == candidate(prefix_n) == [3, 5, 7]
assert interior_summary == canonical(interior_n) == candidate(interior_n) == [4, 6, 8, 10]

print(f"prefix_precondition_witness_N={prefix_n}")
print(f"prefix_initial_state={prefix_initial_state}")
print(f"loop_precondition_witness=(N={loop_n}, I={loop_i}, VS={loop_vs})")
print(f"loop_claim_summary={loop_summary}")
print(
    "interior_loop_witness="
    f"(N={interior_n}, I={interior_i}, VS={interior_vs})"
)
print(f"interior_loop_summary={interior_summary}")
print(f"trusted_canonical_N3={canonical(3)}")
print(f"candidate_python_N3={candidate(3)}")
print("CLAIM_WITNESSES_OK")
