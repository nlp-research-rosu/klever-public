#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary


generation = Path("/reference/klean-generation")
generated = generation / "generated"
audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
discovery_hash = hashlib.sha256(
    Path("/reference/lemma-discovery.json").read_bytes()
).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


input_manifest = read_json(generation / "input-manifest.json")
generator_manifest = read_json(generation / "generator-manifest.json")
export_result = read_json(generation / "export-result.json")
recorded_preflight = read_json(generation / "preflight.json")
trust_inventory = read_json(generation / "trust-inventory.json")
obligation_map = read_json(generated / "obligation-map.json")
toolchain_lock = read_json(Path("/reference/klean-toolchain.lock.json"))
validated = validate_trust_boundary(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
)
source_rules = klean_export._domain_source_rules(validated, discovery_hash)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)
observed_target = klean_export.target_statement(generated)

checks: list[tuple[str, bool, str]] = []


def check(label: str, condition: bool, detail: str) -> None:
    checks.append((label, condition, detail))


generated_hash = klean_export.tree_digest(generated)
stage1_hash = klean_export.tree_digest(Path("/reference/k-proof"))
obligation_map_hash = hashlib.sha256(
    (generated / "obligation-map.json").read_bytes()
).hexdigest()
trust_inventory_hash = hashlib.sha256(
    (generation / "trust-inventory.json").read_bytes()
).hexdigest()

check(
    "generated tree hash: generator manifest",
    generated_hash == generator_manifest["generated_tree_sha256"],
    generated_hash,
)
check(
    "generated tree hash: audit input",
    generated_hash == resolution["hashes"]["generated_tree_sha256"],
    generated_hash,
)
check(
    "Stage 1 export hash: input manifest",
    stage1_hash == input_manifest["stage1_workspace_sha256"],
    stage1_hash,
)
check(
    "Stage 1 export hash: generator provenance",
    stage1_hash
    == generator_manifest["provenance"]["stage1_workspace_sha256"],
    stage1_hash,
)
check(
    "Stage 3 hash: input manifest",
    discovery_hash == input_manifest["stage3_discovery_manifest_sha256"],
    discovery_hash,
)
check(
    "Stage 3 hash: generator provenance",
    discovery_hash
    == generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ],
    discovery_hash,
)
check(
    "inventory hash: input manifest",
    validated["inventory_sha256"] == input_manifest["inventory_sha256"],
    validated["inventory_sha256"],
)
check(
    "inventory hash: generator provenance",
    validated["inventory_sha256"]
    == generator_manifest["provenance"]["inventory_sha256"],
    validated["inventory_sha256"],
)
check(
    "toolchain lock",
    generator_manifest["toolchain"] == toolchain_lock,
    json.dumps(generator_manifest["toolchain"], sort_keys=True),
)
check(
    "definition bucket exact",
    input_manifest["definitions"] == validated["definitions"],
    f"count={len(input_manifest['definitions'])}",
)
check(
    "operational-rule bucket exact",
    input_manifest["operational_rules"] == validated["operational_rules"],
    f"count={len(input_manifest['operational_rules'])}",
)
check(
    "proved-derived-lemma bucket exact",
    input_manifest["proved_derived_lemmas"]
    == validated["proved_derived_lemmas"],
    f"count={len(input_manifest['proved_derived_lemmas'])}",
)
check(
    "domain source-rule list exact",
    input_manifest["source_rules"] == source_rules,
    f"ids={[item['source_rule_id'] for item in source_rules]}",
)
check(
    "obligation map source-rule list exact",
    obligation_map["source_rules"] == source_rules,
    f"count={len(obligation_map['source_rules'])}",
)

expected_ids = [rule["source_rule_id"] for rule in source_rules]
obligations = obligation_map["obligations"]
observed_ids = [obligation.get("source_rule_id") for obligation in obligations]
check(
    "obligation identity order",
    observed_ids == expected_ids,
    f"observed={observed_ids} expected={expected_ids}",
)
check(
    "obligation identity uniqueness",
    len(observed_ids) == len(set(observed_ids)),
    repr(observed_ids),
)
check(
    "obligation count: generator manifest",
    len(obligations) == generator_manifest["obligation_count"],
    str(len(obligations)),
)
check(
    "obligation count: export result",
    len(obligations) == export_result["obligation_count"],
    str(len(obligations)),
)
check(
    "obligation count: recorded preflight",
    len(obligations) == recorded_preflight["obligation_count"],
    str(len(obligations)),
)
check(
    "obligation count: audit input",
    len(obligations) == resolution["stage4_preflight"]["obligation_count"],
    str(len(obligations)),
)
check(
    "obligation-map hash",
    obligation_map_hash == generator_manifest["obligation_map_sha256"],
    obligation_map_hash,
)
check(
    "trust-inventory hash",
    trust_inventory_hash == export_result["trust_inventory_sha256"],
    trust_inventory_hash,
)
check(
    "trust parameters empty for empty domain set",
    obligation_map["trust_parameters"] == [],
    repr(obligation_map["trust_parameters"]),
)
check(
    "no expected target definition",
    expected_target_definition is None,
    repr(expected_target_definition),
)
check(
    "no observed generated target",
    observed_target is None,
    repr(observed_target),
)
check(
    "no generator-manifest target",
    generator_manifest["target"] is None,
    repr(generator_manifest["target"]),
)
check(
    "no recorded-preflight target",
    recorded_preflight["target"] is None,
    repr(recorded_preflight["target"]),
)
check(
    "no audit-input target",
    resolution["target"] is None
    and resolution["stage4_preflight"]["target"] is None,
    repr(resolution["target"]),
)
check(
    "no vacuous generated conjunct",
    all(
        obligation.get("lean_conjunct", "").strip()
        not in {"True", "(True)", "by trivial"}
        for obligation in obligations
    ),
    f"conjuncts={[item.get('lean_conjunct') for item in obligations]}",
)
check(
    "KLEAN_NO_OBLIGATIONS status: export result",
    export_result["status"] == "KLEAN_NO_OBLIGATIONS",
    export_result["status"],
)
check(
    "KLEAN_NO_OBLIGATIONS status: recorded preflight",
    recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS",
    recorded_preflight["status"],
)
check(
    "KLEAN_NO_OBLIGATIONS status: audit selection",
    resolution["selections"]["klean_generation"]["status"]
    == "KLEAN_NO_OBLIGATIONS",
    resolution["selections"]["klean_generation"]["status"],
)
check(
    "classification-only mode",
    resolution["mode"] == "CLASSIFICATION_ONLY",
    resolution["mode"],
)
check(
    "no Stage 5 candidate",
    not Path("/candidate").exists(),
    f"exists={Path('/candidate').exists()}",
)

for label, passed, detail in checks:
    print(f"{'PASS' if passed else 'FAIL'}\t{label}\t{detail}")

failures = [label for label, passed, _detail in checks if not passed]
print(f"INDEPENDENT_DOMAIN_RULE_COUNT={len(source_rules)}")
print(f"GENERATED_OBLIGATION_COUNT={len(obligations)}")
print(f"TOTAL_CHECKS={len(checks)}")
print(f"TOTAL_FAILURES={len(failures)}")
if failures:
    raise SystemExit(1)
