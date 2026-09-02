#!/usr/bin/env python3
import json
from pathlib import Path

from tools import k_rule_inventory as inventory


files = [
    Path("/reference/k-proof/verification.k"),
    Path("/reference/k-proof/connection-rule.k"),
    Path("/reference/k-proof/verification-base.k"),
]
by_module = {}
for path in files:
    text = path.read_text()
    modules = inventory._modules(inventory._mask_non_code(text))
    for module in modules:
        by_module[module.name] = (path, text, module)

pending = ["VERIFICATION"]
reached = []
while pending:
    name = pending.pop(0)
    if name in reached:
        continue
    reached.append(name)
    if name in by_module:
        pending.extend(by_module[name][2].imports)

classifications = {
    "rule-7053976245560ebde1f9c329f37f168cf403550b3226be6fd87bc25c9c187bda": (
        "PROVED_DERIVED_LEMMA"
    ),
    "rule-a125d094d70188da5ff77c740e52261fd69a2a3784be6928238fb15df19a7a19": (
        "DEFINITION"
    ),
    "rule-19e8781342762c8c476b4eea71d343b12d1e66bc89b2d271905518e733ed4682": (
        "DEFINITION"
    ),
    "rule-fb3d10bf0eb9e4f62aad18017f1ab7c5f7a7a5f5c590593e8b83ec2d9834028b": (
        "DEFINITION"
    ),
    "rule-bf30e24b24687c20941ecb863886dc67a9049d65bf68ca325559188ec68de3ae": (
        "DEFINITION"
    ),
    "rule-050c02c309a5a530a8227be9add80d806c43948fb2a4cee44e6a4d8da7a1a71d": (
        "DOMAIN_LEMMA"
    ),
    "rule-6a2681616cee874c5a1856e102a2ab5794a9175a210318f62d58e2c74647c6a2": (
        "DOMAIN_LEMMA"
    ),
    "rule-79867a7dea47e4e5f98e59d1cdcebad2e7a31d021c387d2ab8c5714ceac988b0": (
        "DEFINITION"
    ),
    "rule-9371ae3bb178a5f2d69f2338883aa1878c94170ae90c5b52f939214871d333d5": (
        "DEFINITION"
    ),
    "rule-e0a6a1010506cb6e1e4dcfbfaacc8a9fcb910826e3cf03e90b3a2d2fd022089d": (
        "DEFINITION"
    ),
}

raw_records = []
records = []
for path in files:
    text = path.read_text()
    modules = inventory._modules(inventory._mask_non_code(text))
    for module in modules:
        if module.name not in reached:
            continue
        for rule in inventory._rule_documents(text, (module,)):
            raw_records.append({"source_file": path.name, **rule})
            records.append(
                {
                    "source_file": path.name,
                    **rule,
                    "independent_classification": classifications[
                        rule["source_rule_id"]
                    ],
                }
            )

print(
    json.dumps(
        {
            "reached_modules": reached,
            "proof_local_modules": [
                name for name in reached if name in by_module
            ],
            "rule_count": len(records),
            "inventory_sha256_with_source_files": (
                inventory.canonical_json_sha256(raw_records)
            ),
            "inventory_sha256_with_source_files_and_classification": (
                inventory.canonical_json_sha256(records)
            ),
            "rules": records,
        },
        indent=2,
        sort_keys=True,
    )
)
