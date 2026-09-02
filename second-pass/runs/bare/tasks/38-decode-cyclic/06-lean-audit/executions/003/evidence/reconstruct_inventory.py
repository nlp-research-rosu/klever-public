#!/usr/bin/env python3
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


inventory = inventory_verification(Path("/reference/k-proof"))
print(json.dumps(inventory, indent=2, sort_keys=True))

validated = validate_trust_boundary(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
)
print(
    json.dumps(
        {
            "bijection": "PASS",
            "definitions": len(validated["definitions"]),
            "operational_rules": len(validated["operational_rules"]),
            "proved_derived_lemmas": len(
                validated["proved_derived_lemmas"]
            ),
            "domain_lemmas": len(validated["domain_lemmas"]),
        },
        indent=2,
        sort_keys=True,
    )
)
