import hashlib
import json
import os
import stat
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification


root = Path("/reference/k-proof")
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
recorded = audit["stage1_source_hashes"]
missing = []
mismatched = []
bad_type = []
for relative, expected in recorded.items():
    path = root / relative
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        missing.append(relative)
        continue
    if not stat.S_ISREG(mode):
        bad_type.append(relative)
        continue
    observed = hashlib.sha256(path.read_bytes()).hexdigest()
    if observed != expected:
        mismatched.append((relative, expected, observed))

actual = []
symlinks = []
special = []
for base, dirs, files in os.walk(root, followlinks=False):
    for name in dirs + files:
        path = Path(base) / name
        mode = path.lstat().st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISREG(mode):
            actual.append(relative)
        elif stat.S_ISLNK(mode):
            symlinks.append(relative)
        elif not stat.S_ISDIR(mode):
            special.append(relative)
unrecorded = sorted(set(actual) - set(recorded))
print("stage1_recorded_file_count", len(recorded))
print("stage1_actual_regular_file_count", len(actual))
print("stage1_missing_count", len(missing), missing)
print("stage1_bad_type_count", len(bad_type), bad_type)
print("stage1_mismatch_count", len(mismatched), mismatched)
print("stage1_unrecorded_regular_count", len(unrecorded), unrecorded)
print("stage1_symlink_count", len(symlinks), symlinks)
print("stage1_special_count", len(special), special)

checks = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(root),
    "stage1_export_sha256": klean_export.tree_digest(root),
    "discovery_manifest_sha256": hashlib.sha256(
        Path("/reference/lemma-discovery.json").read_bytes()
    ).hexdigest(),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
}
for key, observed in checks.items():
    print(
        f"{key}_match",
        observed == audit["hashes"][key],
        observed,
        audit["hashes"][key],
    )

input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
export_result = json.loads(
    Path("/reference/klean-generation/export-result.json").read_text()
)
obligation_map = json.loads(
    Path(
        "/reference/klean-generation/generated/obligation-map.json"
    ).read_text()
)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
inventory = inventory_verification(root)
sidecars = {
    name: hashlib.sha256(
        Path("/reference/klean-generation", name).read_bytes()
    ).hexdigest()
    for name in [
        "input-manifest.json",
        "generator-manifest.json",
        "trust-inventory.json",
        "export-result.json",
    ]
}
obligation_hash = hashlib.sha256(
    Path(
        "/reference/klean-generation/generated/obligation-map.json"
    ).read_bytes()
).hexdigest()
expected_definitions = [
    {
        **rule,
        "classification": classified["classification"],
        "rationale": classified["rationale"],
    }
    for rule, classified in zip(
        inventory["rules"], discovery["rules"], strict=True
    )
]
print(
    "input_inventory_hash_match",
    input_manifest["inventory_sha256"] == inventory["inventory_sha256"],
)
print(
    "generator_inventory_hash_match",
    generator_manifest["provenance"]["inventory_sha256"]
    == inventory["inventory_sha256"],
)
print(
    "input_verification_hash_match",
    input_manifest["verification_sha256"]
    == inventory["verification_sha256"],
)
print(
    "input_definitions_exact_match",
    input_manifest["definitions"] == expected_definitions,
)
print("input_source_rules", input_manifest["source_rules"])
print("obligation_map_source_rules", obligation_map["source_rules"])
print("obligation_map_obligations", obligation_map["obligations"])
print("obligation_map_trust_parameters", obligation_map["trust_parameters"])
print(
    "obligation_map_hash_match",
    obligation_hash == generator_manifest["obligation_map_sha256"],
    obligation_hash,
    generator_manifest["obligation_map_sha256"],
)
print(
    "export_trust_inventory_hash_match",
    sidecars["trust-inventory.json"]
    == export_result["trust_inventory_sha256"],
    sidecars["trust-inventory.json"],
    export_result["trust_inventory_sha256"],
)
print(
    "generator_toolchain_lock_match",
    generator_manifest["toolchain"]
    == json.loads(Path("/reference/klean-toolchain.lock.json").read_text()),
)
print("generator_target", generator_manifest["target"])
print("audit_input_target", audit.get("target"))
print(
    "trusted_target_statement",
    klean_export.target_statement(
        Path("/reference/klean-generation/generated")
    ),
)
print(
    "candidate_exists",
    Path("/candidate").exists() or Path("/candidate").is_symlink(),
)
print("audit_lean_workspace", audit.get("lean_workspace"))
print("audit_lean_invocation", audit.get("lean_invocation"))
print(
    "audit_lean_hashes",
    audit["hashes"]["lean_workspace_sha256"],
    audit["hashes"]["lean_invocation_sha256"],
)
print("sidecar_sha256", json.dumps(sidecars, sort_keys=True))
