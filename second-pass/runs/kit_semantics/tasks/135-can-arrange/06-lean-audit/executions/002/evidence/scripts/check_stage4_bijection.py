import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory
from tools import pipeline_contract


domain_id = "rule-2fd1883e1dbbdfd9717b1321447ac996a4962a56a877371e6e1bee92b5b19050"
inventory = k_rule_inventory.inventory_verification(Path("/reference/k-proof"))
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
generation = Path("/reference/klean-generation")
obligation_path = generation / "generated/obligation-map.json"
obligation_map = json.loads(obligation_path.read_text())
manifest = json.loads((generation / "generator-manifest.json").read_text())

domain_rules = [rule for rule in discovery["rules"] if rule["classification"] == "DOMAIN_LEMMA"]
source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
independent_domain_ids = [domain_id]
discovery_domain_ids = [rule["source_rule_id"] for rule in domain_rules]
source_ids = [rule["source_rule_id"] for rule in source_rules]
obligation_ids = [rule["source_rule_id"] for rule in obligations]

canonical_by_id = {rule["source_rule_id"]: rule for rule in inventory["rules"]}
bound_ids = [
    source_id
    for parameter in manifest["target"]["parameters"]
    for source_id in parameter["source_rule_ids"]
]

print(f"independently classified domain ids={independent_domain_ids}")
print(f"discovery domain ids={discovery_domain_ids}")
print(f"obligation-map source ids={source_ids}")
print(f"obligation ids={obligation_ids}")
print(
    "independent/discovery/source/obligation ordered identity lists equal="
    f"{independent_domain_ids == discovery_domain_ids == source_ids == obligation_ids}"
)
print(f"source-rule ids unique={len(source_ids) == len(set(source_ids))}")
print(f"obligation ids unique={len(obligation_ids) == len(set(obligation_ids))}")
print(f"manifest obligation_count={manifest['obligation_count']}")
print(f"actual obligation_count={len(obligations)}")
print(
    "obligation-map hash match="
    f"{pipeline_contract.sha256_file(obligation_path) == manifest['obligation_map_sha256']}"
)

obligation = obligations[0]
source = source_rules[0]
canonical = canonical_by_id[domain_id]
print(f"source span canonical={canonical['start_line']}-{canonical['end_line']}")
print(f"source span map={source['start_line']}-{source['end_line']}")
print(f"obligation span={obligation['source_span']['start_line']}-{obligation['source_span']['end_line']}")
print(f"normalized hash canonical={canonical['normalized_sha256']}")
print(f"normalized hash source map={source['normalized_sha256']}")
print(f"normalized hash obligation={obligation['normalized_sha256']}")
print(
    "lean conjunct hash match="
    f"{hashlib.sha256(obligation['lean_conjunct'].encode()).hexdigest() == obligation['lean_conjunct_sha256']}"
)
print(f"target parameter bound ids={bound_ids}")
print(f"each target parameter bound to sole domain rule={bound_ids == [domain_id, domain_id, domain_id]}")
print(f"generated obligation={obligation['lean_conjunct']}")

source_solution = Path("/reference/k-proof/solution.py").read_text().splitlines()
print(f"source program comparison={source_solution[7].strip()}")
print(f"frozen dynamic bridge={canonical['text']}")

sorts = Path(
    "/reference/klean-generation/generated/Klean135CanArrange/Sorts.lean"
).read_text()
empty_sort_str = "inductive SortStr : Type\n\n" in sorts
print(f"generated SortStr is constructor-free={empty_sort_str}")
