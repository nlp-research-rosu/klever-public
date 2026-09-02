from pathlib import Path
import hashlib
import json

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary

workspace = Path("/reference/k-proof")
manifest = Path("/reference/lemma-discovery.json")
verification = (workspace / "verification.k").read_bytes()
inventory = inventory_verification(workspace)
document = json.loads(manifest.read_text())
validated = validate_trust_boundary(workspace, manifest)
print("COMMAND: inventory_verification(/reference/k-proof)")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("VERIFICATION_SHA256_RECOMPUTED:", hashlib.sha256(verification).hexdigest())
print(
    "CANONICAL_RULE_LIST_JSON:",
    json.dumps(inventory["rules"], sort_keys=True, separators=(",", ":"), ensure_ascii=False),
)
print("INVENTORY_SHA256_RECOMPUTED:", canonical_json_sha256(inventory["rules"]))
print("MANIFEST_INVENTORY_SHA256:", document["inventory_sha256"])
print(
    "INVENTORY_HASH_MATCH:",
    canonical_json_sha256(inventory["rules"]) == document["inventory_sha256"],
)
canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
classified_ids = [rule["source_rule_id"] for rule in document["rules"]]
print("CANONICAL_IDS_IN_ORDER:", canonical_ids)
print("CLASSIFIED_IDS_IN_ORDER:", classified_ids)
print("ORDERED_IDENTITY_MATCH:", canonical_ids == classified_ids)
print("UNIQUE_CANONICAL_IDS:", len(set(canonical_ids)) == len(canonical_ids))
print("UNIQUE_CLASSIFIED_IDS:", len(set(classified_ids)) == len(classified_ids))
print("EXTRA_IDS:", sorted(set(classified_ids) - set(canonical_ids)))
print("OMITTED_IDS:", sorted(set(canonical_ids) - set(classified_ids)))
print("VALIDATE_TRUST_BOUNDARY: PASS")
for name in ("definitions", "operational_rules", "proved_derived_lemmas", "domain_lemmas"):
    print(name.upper() + "_COUNT:", len(validated[name]))
