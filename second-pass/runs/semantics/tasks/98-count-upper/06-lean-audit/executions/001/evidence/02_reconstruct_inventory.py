#!/usr/bin/env python3
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification

inventory = inventory_verification(Path("/reference/k-proof"))
output = Path("/audit-output/evidence/reconstructed-inventory.json")
output.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n")
print(json.dumps(inventory, indent=2, sort_keys=True))
