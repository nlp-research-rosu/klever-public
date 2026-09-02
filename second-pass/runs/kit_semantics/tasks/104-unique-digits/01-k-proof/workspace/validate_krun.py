"""Check the concrete K run's three returned heap objects."""

from pathlib import Path


compact = "".join(Path("concrete.krun").read_text(encoding="utf-8").split())
expected_fragments = [
    '"case1"|->ref(2)',
    '"case2"|->ref(5)',
    '"case3"|->ref(8)',
    "2|->list(vCons(1,vCons(15,vCons(33,.ValSeq))))",
    "5|->list(.ValSeq)",
    "8|->list(vCons(7,vCons(111,vCons(97531,.ValSeq))))",
    "<exit-code>0</exit-code>",
]

missing = [fragment for fragment in expected_fragments if fragment not in compact]
print(
    f"krun expected-fragments={len(expected_fragments)} "
    f"missing={len(missing)}"
)
if missing:
    for fragment in missing:
        print(f"missing: {fragment}")
    raise SystemExit(1)
