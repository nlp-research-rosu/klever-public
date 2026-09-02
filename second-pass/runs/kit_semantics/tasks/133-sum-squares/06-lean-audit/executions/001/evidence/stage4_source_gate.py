import json
import re
from pathlib import Path

from tools import klean_export, klean_preflight


generated = Path("/reference/klean-generation/generated")
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)

sources = klean_preflight._lean_sources(generated)
declared = klean_preflight._trust_declarations(sources)
klean_preflight._reject_proposition_trust(generated, sources, declared)
klean_preflight._check_imports(generated, sources)

expected = {
    entry["name"]: (entry["kind"], entry["type"])
    for entry in inventory["allowlist"]
}
assert declared == expected

hits = {"sorry": [], "admit": [], "unsafe": []}
for source in sources:
    body = source.read_text()
    for token in hits:
        if re.search(rf"\b{token}\b", body):
            hits[token].append(source.relative_to(generated).as_posix())

obligation_map = json.loads((generated / "obligation-map.json").read_text())
target = klean_export.target_statement(generated)
expected_target = klean_export.expected_target_definition(obligation_map)

print(f"lean_source_count={len(sources)}")
print("lean_sources=")
for source in sources:
    print(f"  {source.relative_to(generated).as_posix()}")
print(f"trust_declaration_count={len(declared)}")
print(f"trust_allowlist_count={len(expected)}")
print(f"trust_declarations_exactly_match_allowlist={declared == expected}")
print("independent_proposition_trust_policy=PASS")
print("import_policy=PASS")
print(f"forbidden_token_hits={json.dumps(hits, sort_keys=True)}")
print(f"obligation_count={len(obligation_map['obligations'])}")
print(f"source_rule_count={len(obligation_map['source_rules'])}")
print(f"trust_parameter_count={len(obligation_map['trust_parameters'])}")
print(f"expected_target_definition={expected_target!r}")
print(f"observed_target={target!r}")
assert not any(hits.values())
assert expected_target is None
assert target is None
print("STAGE4 SOURCE/TRUST GATE PASSED")
