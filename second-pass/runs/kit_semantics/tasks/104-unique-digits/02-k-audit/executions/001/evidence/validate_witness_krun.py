#!/usr/bin/env python3
"""Check result objects in the fresh LLVM witness execution."""

from pathlib import Path


text = Path("/audit-output/evidence/stage4-witness-krun.log").read_text(
    encoding="utf-8"
)
compact = "".join(text.split())

# Allocation sequence: each call allocates input, accumulator, and returned sort.
expected = [
    '"empty"|->ref(2)',
    '"smallest_keep"|->ref(5)',
    '"smallest_drop"|->ref(8)',
    '"prompt_one"|->ref(11)',
    '"prompt_two"|->ref(14)',
    '"duplicates"|->ref(17)',
    "2|->list(.ValSeq)",
    "5|->list(vCons(1,.ValSeq))",
    "8|->list(.ValSeq)",
    "11|->list(vCons(1,vCons(15,vCons(33,.ValSeq))))",
    "14|->list(.ValSeq)",
    "17|->list(vCons(1,vCons(1,vCons(15,vCons(33,vCons(97531,.ValSeq))))))",
    "<exit-code>0</exit-code>",
    "EXIT_STATUS:0",
]
missing = [fragment for fragment in expected if fragment not in compact]
print(f"expected-fragments={len(expected)} missing={len(missing)}")
for fragment in missing:
    print("MISSING:", fragment)
raise SystemExit(1 if missing else 0)
