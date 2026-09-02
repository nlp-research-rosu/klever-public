#!/usr/bin/env python3
import json
from pathlib import Path

from tools import stage6_resolution_contract


document = json.loads(Path("/audit-input.json").read_text())
resolution, digest = stage6_resolution_contract.verify_audit_input(document)
assert digest == document["resolved_input_sha256"]
assert resolution == document["resolution"]
print("RESOLVED_INPUT_SHA256", digest)
print("AUDIT_INPUT_BINDING", "PASS")
