#!/usr/bin/env python3
"""Ground witnesses for both candidate reachability-claim preconditions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Callable


ROOT = Path("/tmp/audit-work/29-filter-by-prefix")


def load(path: Path, name: str) -> Callable[[list[str], str], list[str]]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_prefix


canonical = load(ROOT / "trusted" / "canonical.py", "witness_canonical")
candidate = load(ROOT / "candidate-src" / "solution.py", "witness_candidate")


def mathematical_prefix_filter(prefix: str, values: list[str]) -> list[str]:
    # Independent spelling of startswith for this finite ground check.
    width = len(prefix)
    return [value for value in values if value[:width] == prefix]


entry_input = ["abc", "bcd", "array"]
entry_prefix = "a"
entry_claim_result = mathematical_prefix_filter(entry_prefix, entry_input)

loop_accumulator = ["seed"]
loop_rest = ["abc", "bcd", "array"]
loop_prefix = "a"
loop_claim_heap = loop_accumulator + mathematical_prefix_filter(loop_prefix, loop_rest)

result = {
    "entry_claim_witness": {
        "K_INPUT": 'sCons("abc", sCons("bcd", sCons("array", .StrList)))',
        "K_PREFIX": "iCons(97, .IntSeq)",
        "initial_env": 0,
        "initial_scopeLoc": 1,
        "initial_heap": ".Map",
        "initial_heapLoc": 0,
        "initial_stack": ".List",
        "initial_ret": "noRet",
        "initial_exc": "NoExc",
        "claimed_result": entry_claim_result,
        "canonical_result": canonical(entry_input, entry_prefix),
        "candidate_result": candidate(entry_input, entry_prefix),
    },
    "loop_claim_witness": {
        "L": 1,
        "H": 7,
        "SC": ".Map",
        "PREFIX": loop_prefix,
        "REST": loop_rest,
        "ORIGINAL": loop_rest,
        "CURRENT": "",
        "ACC": loop_accumulator,
        "claimed_final_heap_value": loop_claim_heap,
        "canonical_on_REST": canonical(loop_rest, loop_prefix),
        "candidate_on_REST": candidate(loop_rest, loop_prefix),
    },
}

print(json.dumps(result, indent=2, sort_keys=True))

assert result["entry_claim_witness"]["claimed_result"] == result["entry_claim_witness"]["canonical_result"]
assert result["entry_claim_witness"]["claimed_result"] == result["entry_claim_witness"]["candidate_result"]
assert loop_claim_heap == loop_accumulator + canonical(loop_rest, loop_prefix)
assert loop_claim_heap == loop_accumulator + candidate(loop_rest, loop_prefix)
