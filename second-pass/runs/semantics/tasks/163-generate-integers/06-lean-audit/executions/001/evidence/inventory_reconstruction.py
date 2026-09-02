import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
source = (workspace / "verification.k").read_text()
lines = source.splitlines()
inventory = inventory_verification(workspace)
manifest = json.loads(Path("/reference/lemma-discovery.json").read_text())
manifest_ids = [entry["source_rule_id"] for entry in manifest["rules"]]
inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]

print("verification_module", inventory["verification_module"])
print("verification_modules", inventory["verification_modules"])
print("verification_sha256", inventory["verification_sha256"])
print("rule_count", len(inventory["rules"]))
for index, rule in enumerate(inventory["rules"], 1):
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    exact_span = (
        "\n".join(lines[rule["start_line"] - 1 : rule["end_line"]])
        == rule["text"]
    )
    print(
        index,
        rule["start_line"],
        rule["end_line"],
        rule["module"],
        rule["attributes"],
        digest,
        rule["source_rule_id"],
        "normalized_match=" + str(digest == rule["normalized_sha256"]),
        "id_match=" + str(rule["source_rule_id"] == "rule-" + digest),
        "span_match=" + str(exact_span),
    )
canonical = hashlib.sha256(
    json.dumps(
        inventory["rules"],
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
).hexdigest()
print("inventory_sha256_recomputed", canonical)
print(
    "inventory_hash_match",
    canonical
    == inventory["inventory_sha256"]
    == manifest["inventory_sha256"],
)
print("manifest_order_bijection", manifest_ids == inventory_ids)
print("manifest_unique", len(manifest_ids) == len(set(manifest_ids)))
print("omitted_ids", sorted(set(inventory_ids) - set(manifest_ids)))
print("extra_ids", sorted(set(manifest_ids) - set(inventory_ids)))
