import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


inv = inventory_verification(Path("/reference/k-proof"))
disc = json.loads(Path("/reference/lemma-discovery.json").read_text())
inv_ids = [rule["source_rule_id"] for rule in inv["rules"]]
disc_ids = [rule["source_rule_id"] for rule in disc["rules"]]
print("inventory_schema_version", inv["schema_version"])
print("discovery_schema_version", disc.get("schema_version"))
print("inventory_rule_count", len(inv_ids))
print("discovery_rule_count", len(disc_ids))
print("inventory_duplicate_ids", len(inv_ids) != len(set(inv_ids)))
print("discovery_duplicate_ids", len(disc_ids) != len(set(disc_ids)))
print("ordered_ids_equal", inv_ids == disc_ids)
print("omitted_from_discovery", sorted(set(inv_ids) - set(disc_ids)))
print("extra_in_discovery", sorted(set(disc_ids) - set(inv_ids)))
print("inventory_sha256_observed", inv["inventory_sha256"])
print("inventory_sha256_recorded", disc.get("inventory_sha256"))
print(
    "inventory_sha256_match",
    inv["inventory_sha256"] == disc.get("inventory_sha256"),
)
for index, (source, classified) in enumerate(
    zip(inv["rules"], disc["rules"], strict=True), 1
):
    print(f'rule_{index}_id={source["source_rule_id"]}')
    print(
        f'rule_{index}_span={source["module"]}:'
        f'{source["start_line"]}-{source["end_line"]}'
    )
    print(
        f'rule_{index}_normalized_sha256='
        f'{source["normalized_sha256"]}'
    )
    print(
        f'rule_{index}_classification='
        f'{classified.get("classification")}'
    )
    print(
        f'rule_{index}_has_simplification='
        f'{"simplification" in source["attributes"]}'
    )
