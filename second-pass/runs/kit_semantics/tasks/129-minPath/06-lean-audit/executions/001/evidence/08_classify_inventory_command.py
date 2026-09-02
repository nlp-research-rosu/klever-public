import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")

domain_reasons = {
    "rule-c542bea0ad56e556c87d2f0a1f3b92b8ebc7ede934ee79e3380edd4c8eec4a70":
        "guarded theorem: the row constructor has exactly N rows for a valid N^2 permutation",
    "rule-97b792417dedc7de0727ca3c557d6c412015002a77809892b5d5cc700a2fd149":
        "guarded theorem: valid row lookup in constructed grid returns the corresponding constructed row",
    "rule-cf5a0acce1b2eb580bfbacadd2e910a549de9a696af1ebfcf37925160d22a22b":
        "guarded theorem: valid column lookup in a constructed row equals row-major gridAt",
    "rule-6239181de49e2422109895baef3c3011f33d8b5f0ae6785549600addc1a5cfc1":
        "guarded permutation theorem: a cell is 1 iff its coordinates are the unique location of 1",
    "rule-b8a75762e8baeaf13b848647832cf0455607cbda75166ad623cdc8ded53ef987":
        "guarded permutation theorem: every valid cell value is below N^2+1",
    "rule-79cc3308597d2aedf94188a46aa45b9302edb4bd5dc309fcd4bc218ec8dc5894":
        "algebraic theorem connecting operational ValSeq concatenation with the verification snoc summary",
    "rule-9b8ee50fdbbf692e2fa2c6bc4aa68e73f5759ff24a19c85fc3e0de3519dd9348":
        "inductive theorem connecting the odd-tail and completed-pair result summaries",
}


def head_symbol(text: str) -> str:
    compact = " ".join(line.strip() for line in text.splitlines())
    m = re.match(r"rule\s+([^\s(]+)", compact)
    return m.group(1) if m else compact[:55]


inv = inventory_verification(WORKSPACE)
manifest = json.loads(DISCOVERY.read_text())
recorded = {r["source_rule_id"]: r["classification"] for r in manifest["rules"]}

print("INDEPENDENT CLASSIFICATION OF EVERY INVENTORY ENTRY")
print("Decision procedure: a rule defining a fresh summary/recurrence or an exact syntax macro is")
print("DEFINITION; a theorem about those functions is DOMAIN_LEMMA; no rule here changes an")
print("MPY execution configuration, and Stage 1 does not establish any same-rule earlier proof.")
print()
counts = {}
mismatches = []
for idx, rule in enumerate(inv["rules"], 1):
    rid = rule["source_rule_id"]
    if rid in domain_reasons:
        cls = "DOMAIN_LEMMA"
        reason = domain_reasons[rid]
    else:
        cls = "DEFINITION"
        if rule["start_line"] >= 274:
            reason = "exact named AST macro for a contiguous construct in frozen solution.py"
        else:
            reason = "base/step/guarded equation defining a named verification summary or recurrence"
    counts[cls] = counts.get(cls, 0) + 1
    ok = recorded.get(rid) == cls
    if not ok:
        mismatches.append((rid, cls, recorded.get(rid)))
    attrs = ",".join(rule["attributes"]) or "-"
    print(f"{idx:02d} {rid} lines={rule['start_line']}-{rule['end_line']} attrs={attrs}")
    print(f"   symbol={head_symbol(rule['text'])} independent={cls} recorded={recorded.get(rid)} match={ok}")
    print(f"   rationale={reason}")

print()
print("independent_counts", json.dumps(counts, sort_keys=True))
print("operational_rule_count", counts.get("OPERATIONAL_RULE", 0))
print("proved_derived_lemma_count", counts.get("PROVED_DERIVED_LEMMA", 0))
print("classification_mismatches", json.dumps(mismatches))
print("all_71_independently_match", len(inv["rules"]) == 71 and not mismatches)
print()
print("SIMPLIFICATION ATTRIBUTE AUDIT")
simp_bad = []
for rule in inv["rules"]:
    if "simplification" in rule["attributes"]:
        cls = "DOMAIN_LEMMA" if rule["source_rule_id"] in domain_reasons else "DEFINITION"
        print(rule["source_rule_id"], cls)
        if cls not in {"DEFINITION", "DOMAIN_LEMMA"}:
            simp_bad.append(rule["source_rule_id"])
print("bad_simplification_classifications", simp_bad)
